
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
 * <p>Original spec-file type: GetConditionParams</p>
 * <pre>
 * Get condition information in a friendly format
 * ws_condition_set_id condition_set_ref
 * list<string> conditions - Optional: Which conditions should be returned. defaults to all conditions in the set
 * Returns {condition_label: {ontology_type(e.g. GO): [Factors]}}
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "condition_set_ref",
    "conditions"
})
public class GetConditionParams {

    @JsonProperty("condition_set_ref")
    private java.lang.String conditionSetRef;
    @JsonProperty("conditions")
    private List<String> conditions;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("condition_set_ref")
    public java.lang.String getConditionSetRef() {
        return conditionSetRef;
    }

    @JsonProperty("condition_set_ref")
    public void setConditionSetRef(java.lang.String conditionSetRef) {
        this.conditionSetRef = conditionSetRef;
    }

    public GetConditionParams withConditionSetRef(java.lang.String conditionSetRef) {
        this.conditionSetRef = conditionSetRef;
        return this;
    }

    @JsonProperty("conditions")
    public List<String> getConditions() {
        return conditions;
    }

    @JsonProperty("conditions")
    public void setConditions(List<String> conditions) {
        this.conditions = conditions;
    }

    public GetConditionParams withConditions(List<String> conditions) {
        this.conditions = conditions;
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
        return ((((((("GetConditionParams"+" [conditionSetRef=")+ conditionSetRef)+", conditions=")+ conditions)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
