import copy
import logging
import os
import shutil
import uuid
from collections import defaultdict

import pandas as pd
from xlrd.biffh import XLRDError

from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseSearchEngine.KBaseSearchEngineClient import KBaseSearchEngine
from GenericsAPI.GenericsAPIClient import GenericsAPI


class Utils:
    def __init__(self, config):
        self.cfg = config
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)
        self.kbse = KBaseSearchEngine(config['search-url'])
        self.gen_api = GenericsAPI(self.callback_url)
        self.DEFAULT_ONTOLOGY_REF = "KbaseOntologies/Custom"
        self.DEFAULT_ONTOLOGY_ID = "Custom:Term"
        self.DEFAULT_UNIT_ID = "Custom:Unit"

    @staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))

    def get_conditions(self, params):
        data = self.dfu.get_objects({
            'object_refs': [params['condition_set_ref']]
        })['data'][0]['data']
        conditions = {}
        keep_keys = params.get('conditions', data['conditions'].keys())
        for key in keep_keys:
            conditions[key] = defaultdict(list)
            for factor, val in zip(data['factors'], data['conditions'][key]):
                ont_abriv = factor['factor_ont_id'].split(":")[0]
                factor['value'] = val
                conditions[key][ont_abriv].append(copy.copy(factor))
        return {"conditions": conditions}

    def file_to_condition_set(self, params):
        """Convert a user supplied file to a compound set"""
        if 'input_file_path' in params:
            scratch_file_path = params['input_file_path']
        elif 'input_shock_id' in params:
            scratch_file_path = self.dfu.shock_to_file(
                {'shock_id': params['input_shock_id'],
                 'file_path': self.scratch}
            ).get('file_path')
        else:
            raise ValueError("Must supply either a input_shock_id or input_file_path")
        try:
            df = pd.read_excel(scratch_file_path, dtype='str')
        except XLRDError:
            df = pd.read_csv(scratch_file_path, sep="\t", dtype='str')
        comp_set = self._df_to_cs_obj(df)
        info = self.dfu.save_objects({
            "id": params['output_ws_id'],
            "objects": [{
                "type": "KBaseExperiments.ConditionSet",
                "data": comp_set,
                "name": params['output_obj_name']
            }]
        })[0]
        return {"condition_set_ref": "%s/%s/%s" % (info[6], info[0], info[4])}

    def _conditionset_data_to_df(self, data):
        """
        Converts a compound set object data to a dataframe
        """

        factors = pd.DataFrame(data['factors'])
        factors.rename(columns=lambda x: x.replace("ont", "ontology").capitalize().replace("_", " "))
        conditions = pd.DataFrame(data['conditions'])
        cs_df = factors.join(conditions)

        return cs_df

    def _clusterset_data_to_df(self, data):
        """
        Converts a cluster set object data to a dataframe
        """

        original_matrix_ref = data.get('original_data')
        data_matrix = self.gen_api.fetch_data({'obj_ref': original_matrix_ref}).get('data_matrix')

        data_df = pd.read_json(data_matrix)
        clusters = data.get('clusters')

        id_name_list = [cluster.get('id_to_data_position').keys() for cluster in clusters]
        id_names = [item for sublist in id_name_list for item in sublist]

        if set(data_df.columns.tolist()) == set(id_names):  # cluster is based on condition
            data_df = data_df.T

        cluster_names = [None] * data_df.index.size

        cluster_id = 0
        for cluster in clusters:
            item_ids = cluster.get('id_to_data_position').keys()
            item_idx = [data_df.index.get_loc(item_id) for item_id in item_ids]

            for idx in item_idx:
                cluster_names[idx] = cluster_id

            cluster_id += 1

        data_df['cluster'] = cluster_names

        return data_df

    def _ws_obj_to_df(self, input_ref):
        """Converts workspace obj to a dataframe"""
        res = self.dfu.get_objects({
            'object_refs': [input_ref]
        })['data'][0]
        name = res['info'][1]

        obj_type = res['info'][2]

        if "KBaseExperiments.ConditionSet" in obj_type:
            cs_df = self._conditionset_data_to_df(res['data'])
        elif "KBaseExperiments.ClusterSet" in obj_type:
            cs_df = self._clusterset_data_to_df(res['data'])
        else:
            err_msg = 'Ooops! [{}] is not supported.\n'.format(obj_type)
            err_msg += 'Please supply KBaseExperiments.ConditionSet or KBaseExperiments.ClusterSet'
            raise ValueError("err_msg")

        return name, cs_df, obj_type

    def _df_to_cs_obj(self, cs_df):
        """Converts a dataframe from a user file to a compound set object"""
        condition_set = {'ontology_mapping_method': "User Curation"}
        cs_df.fillna('', inplace=True)
        if not len(cs_df):
            raise ValueError("No factors in supplied files")
        factor_df = cs_df.filter(regex="[Uu]nit|[Ff]actor")
        condition_df = cs_df.drop(factor_df.columns, axis=1)
        if not len(condition_df.columns):
            raise ValueError("Unable to find any condition columns in supplied file")

        factor_df.rename(columns=lambda x: x.lower().replace(" ontology ", "_ont_").strip(), inplace=True)
        if "factor" not in factor_df.columns:
            raise ValueError("Unable to find a 'Factor' column in supplied file")
        factor_fields = ('factor', 'unit', 'factor_ont_id', 'unit_ont_id')
        factors = factor_df.filter(items=factor_fields).to_dict('records')

        condition_set['factors'] = [self._add_ontology_info(f) for f in factors]
        condition_set['conditions'] = condition_df.to_dict('list')
        return condition_set

    def _search_ontologies(self, term, closest=False):
        """
        Match to an existing KBase ontology term
        :param term: Test to match
        :param closest: if false, term must exactly match an ontology ID
        :return: dict(ontology_ref, id)
        """
        params = {
            "object_types": ["OntologyTerm"],
            "match_filter": {
                "lookup_in_keys": {"id": {"value": term}}
            },
            "access_filter": {
                "with_private": 0,
                "with_public": 1
            },
            "pagination": {
                "count": 1
            },
            "post_processing": {
                "skip_data": 1
            }
        }
        if closest:
            params['match_filter'] = {"full_text_in_all": term}
        res = self.kbse.search_objects(params)
        if not res['objects']:
            return None
        term = res['objects'][0]
        return {"ontology_ref": term['guid'].split(":")[1], "id": term['key_props']['id']}

    def _add_ontology_info(self, factor):
        """Searches KBASE ontologies for terms matching the user supplied factors and units.
        Add the references if found"""
        optionals = {"unit", "unit_ont_id", "unit_ont_ref", }
        factor = {k: v for k, v in factor.items() if k not in optionals or v != ""}
        ont_info = self._search_ontologies(factor.get('factor_ont_id', "").replace("_", ":"))
        if ont_info:
            factor['factor_ont_ref'] = ont_info['ontology_ref']
            factor['factor_ont_id'] = ont_info['id']
        else:
            factor['factor_ont_ref'] = self.DEFAULT_ONTOLOGY_REF
            factor['factor_ont_id'] = self.DEFAULT_ONTOLOGY_ID

        if factor.get('unit'):
            ont_info = self._search_ontologies(factor.get('unit_ont_id', '').replace("_", ":"))
            if ont_info:
                factor['unit_ont_ref'] = ont_info['ontology_ref']
                factor['unit_ont_id'] = ont_info['id']
            else:
                factor['unit_ont_ref'] = self.DEFAULT_ONTOLOGY_REF
                factor['unit_ont_id'] = self.DEFAULT_UNIT_ID
        return factor

    def to_tsv(self, params):
        """Convert an compound set to TSV file"""
        files = {}

        _id, df, obj_type = self._ws_obj_to_df(params['input_ref'])
        files['file_path'] = os.path.join(params['destination_dir'], _id + ".tsv")
        df.to_csv(files['file_path'], sep="\t", index=False)

        return _id, files

    def to_excel(self, params):
        """Convert an compound set to Excel file"""
        files = {}

        _id, df, obj_type = self._ws_obj_to_df(params['input_ref'])
        files['file_path'] = os.path.join(params['destination_dir'], _id + ".xlsx")

        writer = pd.ExcelWriter(files['file_path'])

        if "KBaseExperiments.ConditionSet" in obj_type:
            df.to_excel(writer, "Conditions", index=False)
        elif "KBaseExperiments.ClusterSet" in obj_type:
            df.to_excel(writer, "ClusterSet", index=True)
        # else is checked in `_ws_obj_to_df`

        writer.save()

        return _id, files

    def export(self, file, name, input_ref):
        """Saves a set of files to SHOCK for export"""
        export_package_dir = os.path.join(self.scratch, name+str(uuid.uuid4()))
        os.makedirs(export_package_dir)
        shutil.move(file, os.path.join(export_package_dir, os.path.basename(file)))

        # package it up and be done
        package_details = self.dfu.package_for_download({
            'file_path': export_package_dir,
            'ws_refs': [input_ref]
        })

        return {'shock_id': package_details['shock_id']}
