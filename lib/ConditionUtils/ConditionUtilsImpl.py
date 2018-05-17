# -*- coding: utf-8 -*-
#BEGIN_HEADER
#END_HEADER


class ConditionUtils:
    '''
    Module Name:
    ConditionUtils

    Module Description:
    A KBase module: ConditionUtils
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        #END_CONSTRUCTOR
        pass


    def get_conditions(self, ctx, params):
        """
        :param params: instance of type "GetConditionParams" (Get condition
           information in a friendly format ws_condition_set_id
           condition_set_ref list<string> conditions - Optional: Which
           conditions should be returned. defaults to all conditions in the
           set Returns {condition_label: {ontology_type(e.g. GO):
           [Factors]}}) -> structure: parameter "condition_set_ref" of type
           "ws_condition_set_id" (@id ws ConditionSet), parameter
           "conditions" of list of String
        :returns: instance of type "GetConditionOutput" -> structure:
           parameter "conditions" of mapping from String to mapping from
           String to list of type "Factor" (Internally this is used to store
           factor information (without the value term) and also a format for
           returning data in a useful form from get_conditions @optional
           unit_id unit_ont_id value) -> structure: parameter "factor_label"
           of String, parameter "factor_ont_ref" of String, parameter
           "factor_ont_id" of String, parameter "unit_id" of String,
           parameter "unit_ont_id" of String, parameter "value" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN get_conditions
        #END get_conditions

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method get_conditions return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def file_to_condition_set(self, ctx, params):
        """
        :param params: instance of type "FileToConditionSetParams"
           (input_shock_id and input_file_path - alternative input params,)
           -> structure: parameter "input_shock_id" of String, parameter
           "input_file_path" of String, parameter "output_ws_name" of String,
           parameter "output_obj_name" of String
        :returns: instance of type "FileToConditionSetOutput" -> structure:
           parameter "output_condition_set_ref" of type "ws_condition_set_id"
           (@id ws ConditionSet)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN file_to_condition_set
        #END file_to_condition_set

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method file_to_condition_set return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def condition_set_to_tsv_file(self, ctx, params):
        """
        :param params: instance of type "ConditionSetToTsvFileParams" ->
           structure: parameter "input_ref" of type "ws_condition_set_id"
           (@id ws ConditionSet), parameter "to_shock" of type "bool",
           parameter "file_path" of String
        :returns: instance of type "ConditionSetToTsvFileOutput" ->
           structure: parameter "file_path" of String, parameter "shock_id"
           of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN condition_set_to_tsv_file
        #END condition_set_to_tsv_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method condition_set_to_tsv_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def export_condition_set_tsv(self, ctx, params):
        """
        :param params: instance of type "ExportConditionSetParams" ->
           structure: parameter "input_ref" of type "ws_condition_set_id"
           (@id ws ConditionSet)
        :returns: instance of type "ExportConditionSetOutput" -> structure:
           parameter "shock_id" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN export_condition_set_tsv
        #END export_condition_set_tsv

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method export_condition_set_tsv return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def export_condition_set_excel(self, ctx, params):
        """
        :param params: instance of type "ExportConditionSetParams" ->
           structure: parameter "input_ref" of type "ws_condition_set_id"
           (@id ws ConditionSet)
        :returns: instance of type "ExportConditionSetOutput" -> structure:
           parameter "shock_id" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN export_condition_set_excel
        #END export_condition_set_excel

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method export_condition_set_excel return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
