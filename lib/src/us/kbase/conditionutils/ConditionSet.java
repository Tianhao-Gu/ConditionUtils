
package us.kbase.conditionutils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: ConditionSet</p>
 * <pre>
 * factors - list of supplied factors
 * conditions - mapping of condition_labels to a list of factor values in the same order as the factors array
 * Ontology_mapping_method - One of ???User curation???, ???Closest matching string???
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "conditions",
    "factors",
    "ontology_mapping_method"
})
public class ConditionSet {

    @JsonProperty("conditions")
    private Map<String, List<String>> conditions;
    @JsonProperty("factors")
    private List<Factor> factors;
    @JsonProperty("ontology_mapping_method")
    private java.lang.String ontologyMappingMethod;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("conditions")
    public Map<String, List<String>> getConditions() {
        return conditions;
    }

    @JsonProperty("conditions")
    public void setConditions(Map<String, List<String>> conditions) {
        this.conditions = conditions;
    }

    public ConditionSet withConditions(Map<String, List<String>> conditions) {
        this.conditions = conditions;
        return this;
    }

    @JsonProperty("factors")
    public List<Factor> getFactors() {
        return factors;
    }

    @JsonProperty("factors")
    public void setFactors(List<Factor> factors) {
        this.factors = factors;
    }

    public ConditionSet withFactors(List<Factor> factors) {
        this.factors = factors;
        return this;
    }

    @JsonProperty("ontology_mapping_method")
    public java.lang.String getOntologyMappingMethod() {
        return ontologyMappingMethod;
    }

    @JsonProperty("ontology_mapping_method")
    public void setOntologyMappingMethod(java.lang.String ontologyMappingMethod) {
        this.ontologyMappingMethod = ontologyMappingMethod;
    }

    public ConditionSet withOntologyMappingMethod(java.lang.String ontologyMappingMethod) {
        this.ontologyMappingMethod = ontologyMappingMethod;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((("ConditionSet"+" [conditions=")+ conditions)+", factors=")+ factors)+", ontologyMappingMethod=")+ ontologyMappingMethod)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
