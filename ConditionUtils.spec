/*
A KBase module: ConditionUtils
*/

module ConditionUtils {

    typedef int bool;

    /*
        Internally this is used to store factor information (without the value term) and also a
        format for returning data in a useful form from get_conditions
        @optional unit_id unit_ont_id value
    */

    typedef structure{
        string factor_label;
        string factor_ont_ref;
        string factor_ont_id;
        string unit_id;
        string unit_ont_id;
        string value;
    } Factor;

    /*
     factors - list of supplied factors
     conditions - mapping of condition_labels to a list of factor values in the same order as the factors array
     Ontology_mapping_method - One of “User curation”, “Closest matching string”
    */
     typedef structure{
    	mapping<string, list<string>> conditions;
    	list<Factor> factors;
	string ontology_mapping_method;
     } ConditionSet;

    /* @id ws ConditionSet */
    typedef string ws_condition_set_id;

    /*
        Get condition information in a friendly format

        ws_condition_set_id condition_set_ref
        list<string> conditions - Optional: Which conditions should be returned. defaults to all conditions in the set

        Returns {condition_label: {ontology_type(e.g. GO): [Factors]}}

    */

    typedef structure {
        ws_condition_set_id condition_set_ref;
        list<string> conditions;
    } GetConditionParams;

    typedef structure {
        mapping<string, mapping<string, list<Factor>>> conditions;
    } GetConditionOutput;

    funcdef get_conditions(GetConditionParams params)
        returns (GetConditionOutput output) authentication required;

    /*
        input_shock_id and input_file_path - alternative input params,
    */
    typedef structure {
        string input_shock_id;
        string input_file_path;
        string output_ws_name;
        string output_obj_name;
    } FileToConditionSetParams;

    typedef structure {
        ws_condition_set_id output_condition_set_ref;
    } FileToConditionSetOutput;

    funcdef file_to_condition_set(FileToConditionSetParams params)
        returns (FileToConditionSetOutput) authentication required;

    typedef structure {
        ws_condition_set_id input_ref;
        bool to_shock;
        string file_path;
    } ConditionSetToTsvFileParams;

    typedef structure {
        string file_path;
        string shock_id;
    } ConditionSetToTsvFileOutput;

    funcdef condition_set_to_tsv_file(ConditionSetToTsvFileParams params)
        returns (ConditionSetToTsvFileOutput) authentication required;

    typedef structure {
        ws_condition_set_id input_ref;
    } ExportConditionSetParams;

    typedef structure {
        string shock_id;
    } ExportConditionSetOutput;

    funcdef export_condition_set_tsv(ExportConditionSetParams params)
        returns (ExportConditionSetOutput) authentication required;

    funcdef export_condition_set_excel(ExportConditionSetParams params)
        returns (ExportConditionSetOutput) authentication required;

};
