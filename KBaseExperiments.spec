module KBaseExperiments {

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
};