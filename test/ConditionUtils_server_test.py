# -*- coding: utf-8 -*-
import json
import os
import shutil
import time
import unittest
from configparser import ConfigParser
import uuid
import pandas as pd

from biokbase.workspace.client import Workspace as workspaceService
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ConditionUtils.ConditionUtilsImpl import ConditionUtils
from ConditionUtils.ConditionUtilsServer import MethodContext
from ConditionUtils.authclient import KBaseAuth as _KBaseAuth
from ConditionUtils.core.Utils import Utils
from GenericsAPI.GenericsAPIClient import GenericsAPI


class ConditionUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
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
        cls.serviceUtils = Utils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.gen_api = GenericsAPI(cls.callback_url, service_ver='dev')

        suffix = int(time.time() * 1000)
        cls.wsName = "test_CompoundSetUtils_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})
        cls.wsId = ret[0]
        cls.cond_set = json.load(open('data/CS1.json'))
        info = cls.dfu.save_objects({
            "id": cls.wsId,
            "objects": [{
                "type": "KBaseExperiments.ConditionSet",
                "data": cls.cond_set,
                "name": "test_cond_set"
            }]
        })[0]
        cls.condition_set_ref = "%s/%s/%s" % (info[6], info[0], info[4])
        cls.cond_set_2 = json.load(open('data/CS2.json'))

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def loadExpressionMatrix(self):
        if hasattr(self.__class__, 'expr_matrix_ref'):
            return self.__class__.expr_matrix_ref

        matrix_file_name = 'test_import.xlsx'
        matrix_file_path = os.path.join(self.scratch, matrix_file_name)
        shutil.copy(os.path.join('data', matrix_file_name), matrix_file_path)

        obj_type = 'ExpressionMatrix'
        params = {'obj_type': obj_type,
                  'matrix_name': 'test_ExpressionMatrix',
                  'workspace_name': self.wsName,
                  'input_file_path': matrix_file_path}
        expr_matrix_ref = self.gen_api.import_matrix_from_excel(params).get('matrix_obj_ref')

        self.__class__.expr_matrix_ref = expr_matrix_ref
        print('Loaded ExpressionMatrix: ' + expr_matrix_ref)
        return expr_matrix_ref

    def loadClusterSet(self):

        if hasattr(self.__class__, 'cluster_set_ref'):
            return self.__class__.cluster_set_ref

        expr_matrix_ref = self.loadExpressionMatrix()

        # using DFU, missing ClusterSet uploader
        object_type = 'KBaseExperiments.ClusterSet'
        cluster_set_object_name = 'test_clusterset'
        cluster_set_data = {'clustering_parameters': {'dist_metric': 'cityblock',
                                                      'k_num': '2'},
                            'clusters': [{'id_to_data_position': {
                                            'WRI_RS00015_CDS_1': 1,
                                            'WRI_RS00025_CDS_1': 2}},
                                         {'id_to_data_position': {
                                            'WRI_RS00010_CDS_1': 0}}],
                            'original_data': expr_matrix_ref}

        save_object_params = {
            'id': self.wsId,
            'objects': [{'type': object_type,
                         'data': cluster_set_data,
                         'name': cluster_set_object_name}]
        }

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        cluster_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        self.__class__.cluster_set_ref = cluster_set_ref
        print('Loaded ClusterSet: ' + cluster_set_ref)
        return cluster_set_ref

    def loadConditionClusterSet(self):

        if hasattr(self.__class__, 'condition_cluster_set_ref'):
            return self.__class__.condition_cluster_set_ref

        expr_matrix_ref = self.loadExpressionMatrix()

        # using DFU, missing ClusterSet uploader
        object_type = 'KBaseExperiments.ClusterSet'
        cluster_set_object_name = 'test_clusterset'
        cluster_set_data = {'clustering_parameters': {'dist_metric': 'cityblock',
                                                      'k_num': '2'},
                            'clusters': [{'id_to_data_position': {
                                            'condition_2': 1,
                                            'condition_3': 2}},
                                         {'id_to_data_position': {
                                            'condition_1': 0,
                                            'condition_4': 3}}],
                            'original_data': expr_matrix_ref}

        save_object_params = {
            'id': self.wsId,
            'objects': [{'type': object_type,
                         'data': cluster_set_data,
                         'name': cluster_set_object_name}]
        }

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        condition_cluster_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        self.__class__.condition_cluster_set_ref = condition_cluster_set_ref
        print('Loaded Condition ClusterSet: ' + condition_cluster_set_ref)
        return condition_cluster_set_ref

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsId(self):
        return self.__class__.wsId

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_add_ontology_info(self):
        factor = {'factor': 'stalk development', "factor_ont_id": "GO:0031150", "unit": "Hour",
                  "unit_ont_id": "UO_0000032"}
        with_ref = self.serviceUtils._add_ontology_info(factor)
        self.assertEqual(with_ref.get('factor_ont_ref'), '6308/3/2')
        self.assertEqual(with_ref.get('factor_ont_id'), 'GO:0031150')
        self.assertEqual(with_ref.get('unit_ont_id'), 'UO:0000032')
        self.assertEqual(with_ref.get('unit_ont_ref'), '6308/15/6')

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
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().export_cluster_set_excel(self.getContext(), {})

    def test_get_conditions(self):
        params = {'condition_set_ref': self.condition_set_ref, 'conditions': ['S1', 'S4']}
        ret = self.getImpl().get_conditions(self.getContext(), params)[0]
        self.assertEqual(set(ret['conditions'].keys()), {"S1", "S4"})
        s1 = ret['conditions']['S1']
        self.assertIn("Custom", s1)
        self.assertEqual(len(s1['Custom']), 2)
        self.assertEqual(set(s1['Custom'][0]), {'factor_ont_id', 'unit_ont_id', 'factor',
                                                'factor_ont_ref', 'unit_ont_ref', 'unit', 'value'})
        self.assertEqual(s1['Custom'][0]['value'], "0")

    def test_tsv_import(self):
        params = {'output_ws_id': self.wsId,
                  'input_file_path': 'data/CS2.tsv',
                  'output_obj_name': 'Condition_Set'}
        ret = self.getImpl().file_to_condition_set(self.getContext(), params)[0]
        assert ret and ('condition_set_ref' in ret)
        data = self.dfu.get_objects({
            'object_refs': [ret['condition_set_ref']]
        })['data'][0]['data']
        self.assertEqual(data, self.cond_set_2)

    def test_excel_import(self):
        shock_file = '/CS1.xlsx'
        shutil.copy('/kb/module/test/data/' + shock_file, self.scratch + shock_file)
        shock_id = self.dfu.file_to_shock({'file_path': self.scratch + shock_file})['shock_id']
        params = {'output_ws_id': self.getWsId(),
                  'input_shock_id': shock_id,
                  'output_obj_name': 'CS1'}
        ret = self.getImpl().file_to_condition_set(self.getContext(), params)[0]
        assert ret and ('condition_set_ref' in ret)
        data = self.dfu.get_objects({
            'object_refs': [ret['condition_set_ref']]
        })['data'][0]['data']
        self.assertEqual(data, self.cond_set)

    def test_make_tsv(self):
        params = {'input_ref': self.condition_set_ref, 'destination_dir': self.scratch}
        ret = self.getImpl().condition_set_to_tsv_file(self.getContext(), params)[0]
        assert ret and ('file_path' in ret)

    def test_export_condition_set_tsv(self):
        params = {'input_ref': self.condition_set_ref}
        ret = self.getImpl().export_condition_set_tsv(self.getContext(), params)[0]
        assert ret and ('shock_id' in ret)

    def test_export_condition_set_excel(self):
        params = {'input_ref': self.condition_set_ref}
        ret = self.getImpl().export_condition_set_excel(self.getContext(), params)[0]
        assert ret and ('shock_id' in ret)

    def test_export_cluster_set_excel(self):
        self.loadClusterSet()

        params = {'input_ref': self.cluster_set_ref}
        ret = self.getImpl().export_condition_set_excel(self.getContext(), params)[0]
        assert ret and ('shock_id' in ret)

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        os.makedirs(output_directory)

        self.dfu.shock_to_file({'shock_id': ret['shock_id'],
                                'file_path': output_directory,
                                'unpack': 'unpack'})

        xl_files = [file for file in os.listdir(output_directory) if file.endswith('.xlsx')]
        self.assertEqual(len(xl_files), 1)

        xl = pd.ExcelFile(os.path.join(output_directory, xl_files[0]))
        expected_sheet_names = ['ClusterSet']
        self.assertCountEqual(xl.sheet_names, expected_sheet_names)

        df = xl.parse("ClusterSet")
        expected_index = ['WRI_RS00010_CDS_1', 'WRI_RS00015_CDS_1', 'WRI_RS00025_CDS_1']
        expected_col = ['condition_1', 'condition_2', 'condition_3', 'condition_4', 'cluster']
        self.assertCountEqual(df.index.tolist(), expected_index)
        self.assertCountEqual(df.columns.tolist(), expected_col)

    def test_export_condition_cluster_set_excel(self):
        self.loadConditionClusterSet()

        params = {'input_ref': self.condition_cluster_set_ref}
        ret = self.getImpl().export_condition_set_excel(self.getContext(), params)[0]
        assert ret and ('shock_id' in ret)

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        os.makedirs(output_directory)

        self.dfu.shock_to_file({'shock_id': ret['shock_id'],
                                'file_path': output_directory,
                                'unpack': 'unpack'})

        xl_files = [file for file in os.listdir(output_directory) if file.endswith('.xlsx')]
        self.assertEqual(len(xl_files), 1)

        xl = pd.ExcelFile(os.path.join(output_directory, xl_files[0]))
        expected_sheet_names = ['ClusterSet']
        self.assertCountEqual(xl.sheet_names, expected_sheet_names)

        df = xl.parse("ClusterSet")
        expected_index = ['condition_1', 'condition_2', 'condition_3', 'condition_4']
        expected_col = ['WRI_RS00010_CDS_1', 'WRI_RS00015_CDS_1', 'WRI_RS00025_CDS_1', 'cluster']
        self.assertCountEqual(df.index.tolist(), expected_index)
        self.assertCountEqual(df.columns.tolist(), expected_col)
