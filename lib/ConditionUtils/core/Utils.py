import pandas as pd
import os
import shutil
import uuid
from xlrd.biffh import XLRDError
import logging

from DataFileUtil.DataFileUtilClient import DataFileUtil


class Utils:
    def __init__(self, config):
        self.cfg = config
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.DEFAULT_ONTOLOGY_REF = "KbaseOntologies/Custom"
        self.DEFAULT_ONTOLOGY_ID = "CustomTerm"
        self.DEFAULT_UNIT_ID = "CustomUnit"

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
        raise NotImplementedError

    def file_to_condition_set(self, params):
        """Convert a user supplied file to a compound set"""
        if 'input_file_path' in params:
            scratch_file_path = self.dfu.download_staging_file(
                {'staging_file_subdir_path': params['input_file_path']}
            ).get('copy_file_path')
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

    def _ws_obj_to_df(self, input_ref):
        """Converts a compound set reference to a dataframe"""
        res = self.dfu.get_objects({
            'object_refs': [input_ref]
        })['data'][0]
        name = res['info'][1]
        if "KBaseExperiments.ConditionSet" not in res['info'][2]:
            raise ValueError("Supplied reference is not a ConditionSet")

        factors = pd.DataFrame(res['data']['factors'])
        factors.rename(columns=lambda x: x.replace("ont", "ontology").capitalize().replace("_", " "))
        conditions = pd.DataFrame(res['data']['conditions'])
        cs_df = factors.join(conditions)

        return name, cs_df

    def _df_to_cs_obj(self, cs_df):
        """Converts a dataframe from a user file to a compound set object"""
        condition_set = {'ontology_mapping_method': "User Curation"}
        if not len(cs_df):
            raise ValueError("No factors in supplied files")
        factor_df = cs_df.filter(regex="[Uu]nit|[Ff]actor")
        condition_df = cs_df.drop(factor_df.columns, axis=1)
        if not len(condition_df.columns):
            raise ValueError("Unable to find any condition columns in supplied file")
        factor_df.rename(columns=lambda x: x.lower().strip(), inplace=True)
        if "factor" not in factor_df.columns:
            raise ValueError("Unable to find a 'Factor' column in supplied file")
        factors = factor_df.filter(items=('factor', 'unit')).to_dict('records')
        condition_set['factors'] = [self._add_ontology_info(f) for f in factors]
        condition_set['conditions'] = condition_df.to_dict('list')
        return condition_set

    def _add_ontology_info(self, factor):
        """Searches KBASE ontologies for terms matching the user supplied factors and units.
        Add the references if found"""
        if False:
            # TODO: implement ontology serch
            pass
        else:
            factor['factor_ont_ref'] = self.DEFAULT_ONTOLOGY_REF
            factor['factor_ont_id'] = self.DEFAULT_ONTOLOGY_ID
        if 'unit' in factor:
            factor['factor_unit_id'] = self.DEFAULT_UNIT_ID
        return factor

    def to_tsv(self, params):
        """Convert an compound set to TSV file"""
        files = {}

        _id, df = self._ws_obj_to_df(params['input_ref'])
        files['file_path'] = os.path.join(params['destination_dir'], _id + ".xlsx")
        df.to_csv(files['file_path'], sep="\t")

        return _id, files

    def to_excel(self, params):
        """Convert an compound set to Excel file"""
        files = {}

        _id, df = self._ws_obj_to_df(params['input_ref'])
        files['file_path'] = os.path.join(params['destination_dir'], _id + ".xlsx")

        writer = pd.ExcelWriter(files['file_path'])
        df.to_excel(writer, "Conditions")
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
