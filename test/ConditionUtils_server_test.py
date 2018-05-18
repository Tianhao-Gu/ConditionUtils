# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import time
from mock import patch
from os import environ
import shutil
import json
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from biokbase.workspace.client import Workspace as workspaceService
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ConditionUtils.ConditionUtilsImpl import ConditionUtils
from ConditionUtils.ConditionUtilsServer import MethodContext
from ConditionUtils.authclient import KBaseAuth as _KBaseAuth


class ConditionUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('ConditionUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'ConditionUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = ConditionUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)
        suffix = int(time.time() * 1000)
        wsName = "test_CompoundSetUtils_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': wsName})
        cls.wsId = ret[0]
        cond_set = json.load(open('data/CS1.json'))
        info = cls.dfu.save_objects({
            "id": cls.wsId,
            "objects": [{
                "type": "KBaseExperiments.ConditionSet",
                "data": cond_set,
                "name": "test_cond_set"
            }]
        })[0]
        cls.condition_set_ref = "%s/%s/%s" % (info[6], info[0], info[4])

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsId(self):
        return self.__class__.wsId

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @staticmethod
    def fake_staging_download(params):
        scratch = '/kb/module/work/tmp/'
        inpath = params['staging_file_subdir_path']
        shutil.copy('/kb/module/test/data/' + inpath, scratch + inpath)
        return {'copy_file_path': scratch + inpath}

    def test_missing_params(self):
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().get_conditions(self.getContext(), {})
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().file_to_condition_set(self.getContext(), {})
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().condition_set_to_tsv_file(self.getContext(), {})
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().export_condition_set_tsv(self.getContext(), {})
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().export_condition_set_excel(self.getContext(), {})

    @patch.object(DataFileUtil, "download_staging_file", new=fake_staging_download)
    def test_tsv_import(self):
        params = {'output_ws_id': self.getWsId(),
                  'input_file_path': 'CS1.tsv',
                  'output_obj_name': 'CS1'}
        ret = self.getImpl().file_to_condition_set(self.getContext(), params)[0]
        assert ret and ('condition_set_ref' in ret)

    def test_excel_import(self):
        shock_file = '/CS1.xlsx'
        shutil.copy('/kb/module/test/data/' + shock_file, self.scratch + shock_file)
        shock_id = self.dfu.file_to_shock({'file_path': self.scratch + shock_file})['shock_id']
        params = {'output_ws_id': self.getWsId(),
                  'input_shock_id': shock_id,
                  'output_obj_name': 'CS2'}
        ret = self.getImpl().file_to_condition_set(self.getContext(), params)[0]
        assert ret and ('condition_set_ref' in ret)

    def test_make_tsv(self):
        params = {'input_ref': self.condition_set_ref, 'destination_dir': self.scratch}
        ret = self.getImpl().condition_set_to_tsv_file(self.getContext(), params)[0]
        print(ret)
        assert ret and ('file_path' in ret)

    def test_export_tsv(self):
        params = {'input_ref': self.condition_set_ref}
        ret = self.getImpl().export_condition_set_tsv(self.getContext(), params)[0]
        assert ret and ('shock_id' in ret)

    def test_export_excel(self):
        params = {'input_ref': self.condition_set_ref}
        ret = self.getImpl().export_condition_set_excel(self.getContext(), params)[0]
        assert ret and ('shock_id' in ret)
