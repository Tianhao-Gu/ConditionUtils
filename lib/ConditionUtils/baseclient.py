############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function

import json as _json
import requests as _requests
import random as _random
import os as _os

try:
    from configparser import ConfigParser as _ConfigParser  # py 3
except ImportError:
    from ConfigParser import ConfigParser as _ConfigParser  # py 2

try:
    from urllib.parse import urlparse as _urlparse  # py3
except ImportError:
    from urlparse import urlparse as _urlparse  # py2
import time

_CT = 'content-type'
_AJ = 'application/json'
_URL_SCHEME = frozenset(['http', 'https'])


def _get_token(user_id, password, auth_svc):
    # This is bandaid helper function until we get a full
    # KBase python auth client released
    # note that currently globus usernames, and therefore kbase usernames,
    # cannot contain non-ascii characters. In python 2, quote doesn't handle
    # unicode, so if this changes this client will need to change.
    body = ('user_id=' + _requests.utils.quote(user_id) + '&password=' +
            _requests.utils.quote(password) + '&fields=token')
    ret = _requests.post(auth_svc, data=body, allow_redirects=True)
    status = ret.status_code
    if status >= 200 and status <= 299:
        tok = _json.loads(ret.text)
    elif status == 403:
        raise Exception('Authentication failed: Bad user_id/password ' +
                        'combination for user %s' % (user_id))
    else:
        raise Exception(ret.text)
    return tok['token']


def _read_inifile(file=_os.environ.get(  # @ReservedAssignment
                  'KB_DEPLOYMENT_CONFIG', _os.environ['HOME'] +
                  '/.kbase_config')):
    # Another bandaid to read in the ~/.kbase_config file if one is present
    authdata = None
    if _os.path.exists(file):
        try:
            config = _ConfigParser()
            config.read(file)
            # strip down whatever we read to only what is legit
            authdata = {x: config.get('authentication', x)
                        if config.has_option('authentication', x)
                        else None for x in ('user_id', 'token',
                                            'client_secret', 'keyfile',
                                            'keyfile_passphrase', 'password')}
        except Exception as e:
            print('Error while reading INI file {}: {}'.format(file, e))
    return authdata


class ServerError(Exception):

    def __init__(self, name, code, message, data=None, error=None):
        super(Exception, self).__init__(message)
        self.name = name
        self.code = code
        self.message = '' if message is None else message
        self.data = data or error or ''
        # data = JSON RPC 2.0, error = 1.1

    def __str__(self):
        return self.name + ': ' + str(self.code) + '. ' + self.message + \
            '\n' + self.data


class _JSONObjectEncoder(_json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, frozenset):
            return list(obj)
        return _json.JSONEncoder.default(self, obj)


class BaseClient(object):
    '''
    The KBase base client.
    Required initialization arguments (positional):
    url - the url of the the service to contact:
        For SDK methods: either the url of the callback service or the
            Narrative Job Service Wrapper.
        For SDK dynamic services: the url of the Service Wizard.
        For other services: the url of the service.
    Optional arguments (keywords in positional order):
    timeout - methods will fail if they take longer than this value in seconds.
        Default 1800.
    user_id - a KBase user name.
    password - the password corresponding to the user name.
    token - a KBase authentication token.
    ignore_authrc - if True, don't read auth configuration from
        ~/.kbase_config.
    trust_all_ssl_certificates - set to True to trust self-signed certificates.
        If you don't understand the implications, leave as the default, False.
    auth_svc - the url of the KBase authorization service.
    lookup_url - set to true when contacting KBase dynamic services.
    async_job_check_time_ms - the wait time between checking job state for
        asynchronous jobs run with the run_job method.
    '''
    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/auth/api/legacy/KBase/Sessions/Login',
            lookup_url=False,
            async_job_check_time_ms=100,
            async_job_check_time_scale_percent=150,
            async_job_check_max_time_ms=300000):
        if url is None:
            raise ValueError('A url is required')
        scheme, _, _, _, _, _ = _urlparse(url)
        if scheme not in _URL_SCHEME:
            raise ValueError(url + " isn't a valid http url")
        self.url = url
        self.timeout = int(timeout)
        self._headers = dict()
        self.trust_all_ssl_certificates = trust_all_ssl_certificates
        self.lookup_url = lookup_url
        self.async_job_check_time = async_job_check_time_ms / 1000.0
        self.async_job_check_time_scale_percent = (
            async_job_check_time_scale_percent)
        self.async_job_check_max_time = async_job_check_max_time_ms / 1000.0
        # token overrides user_id and password
        if token is not None:
            self._headers['AUTHORIZATION'] = token
        elif user_id is not None and password is not None:
            self._headers['AUTHORIZATION'] = _get_token(
                user_id, password, auth_svc)
        elif 'KB_AUTH_TOKEN' in _os.environ:
            self._headers['AUTHORIZATION'] = _os.environ.get('KB_AUTH_TOKEN')
        elif not ignore_authrc:
            authdata = _read_inifile()
            if authdata is not None:
                if authdata.get('token') is not None:
                    self._headers['AUTHORIZATION'] = authdata['token']
                elif(authdata.get('user_id') is not None and
                        authdata.get('password') is not None):
                    self._headers['AUTHORIZATION'] = _get_token(
                        authdata['user_id'], authdata['password'], auth_svc)
        if self.timeout < 1:
            raise ValueError('Timeout value must be at least 1 second')

    def _call(self, url, method, params, context=None):
        arg_hash = {'method': method,
                    'params': params,
                    'version': '1.1',
                    'id': str(_random.random())[2:]
                    }
        if context:
            if type(context) is not dict:
                raise ValueError('context is not type dict as required.')
            arg_hash['context'] = context

        body = _json.dumps(arg_hash, cls=_JSONObjectEncoder)
        ret = _requests.post(url, data=body, headers=self._headers,
                             timeout=self.timeout,
                             verify=not self.trust_all_ssl_certificates)
        ret.encoding = 'utf-8'
        if ret.status_code == 500:
            if ret.headers.get(_CT) == _AJ:
                err = ret.json()
                if 'error' in err:
                    raise ServerError(**err['error'])
                else:
                    raise ServerError('Unknown', 0, ret.text)
            else:
                raise ServerError('Unknown', 0, ret.text)
        if not ret.ok:
            ret.raise_for_status()
        resp = ret.json()
        if 'result' not in resp:
            raise ServerError('Unknown', 0, 'An unknown server error occurred')
        if not resp['result']:
            return
        if len(resp['result']) == 1:
            return resp['result'][0]
        return resp['result']

    def _get_service_url(self, service_method, service_version):
        if not self.lookup_url:
            return self.url
        service, _ = service_method.split('.')
        service_status_ret = self._call(
            self.url, 'ServiceWizard.get_service_status',
            [{'module_name': service, 'version': service_version}])
        return service_status_ret['url']

    def _set_up_context(self, service_ver=None, context=None):
        if service_ver:
            if not context:
                context = {}
            context['service_ver'] = service_ver
        return context

    def _check_job(self, service, job_id):
        return self._call(self.url, service + '._check_job', [job_id])

    def _submit_job(self, service_method, args, service_ver=None,
                    context=None):
        context = self._set_up_context(service_ver, context)
        mod, meth = service_method.split('.')
        return self._call(self.url, mod + '._' + meth + '_submit',
                          args, context)

    def run_job(self, service_method, args, service_ver=None, context=None):
        '''
        Run a SDK method asynchronously.
        Required arguments:
        service_method - the service and method to run, e.g. myserv.mymeth.
        args - a list of arguments to the method.
        Optional arguments:
        service_ver - the version of the service to run, e.g. a git hash
            or dev/beta/release.
        context - the rpc context dict.
        '''
        mod, _ = service_method.split('.')
        job_id = self._submit_job(service_method, args, service_ver, context)
        async_job_check_time = self.async_job_check_time
        while True:
            time.sleep(async_job_check_time)
            async_job_check_time = (async_job_check_time *
                                    self.async_job_check_time_scale_percent /
                                    100.0)
            if async_job_check_time > self.async_job_check_max_time:
                async_job_check_time = self.async_job_check_max_time
            job_state = self._check_job(mod, job_id)
            if job_state['finished']:
                if not job_state['result']:
                    return
                if len(job_state['result']) == 1:
                    return job_state['result'][0]
                return job_state['result']

    def call_method(self, service_method, args, service_ver=None,
                    context=None):
        '''
        Call a standard or dynamic service synchronously.
        Required arguments:
        service_method - the service and method to run, e.g. myserv.mymeth.
        args - a list of arguments to the method.
        Optional arguments:
        service_ver - the version of the service to run, e.g. a git hash
            or dev/beta/release.
        context - the rpc context dict.
        '''
        url = self._get_service_url(service_method, service_ver)
        context = self._set_up_context(service_ver, context)
        return self._call(url, service_method, args, context)