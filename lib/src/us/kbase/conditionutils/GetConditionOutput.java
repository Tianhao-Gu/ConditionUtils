
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
import us.kbase.kbaseexperiments.Factor;


/**
 * <p>Original spec-file type: GetConditionOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "conditions"
})
public class GetConditionOutput {

    @JsonProperty("conditions")
    private Map<String, Map<String, List<Factor>>> conditions;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("conditions")
    public Map<String, Map<String, List<Factor>>> getConditions() {
        return conditions;
    }

    @JsonProperty("conditions")
    public void setConditions(Map<String, Map<String, List<Factor>>> conditions) {
        this.conditions = conditions;
    }

    public GetConditionOutput withConditions(Map<String, Map<String, List<Factor>>> conditions) {
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
        return ((((("GetConditionOutput"+" [conditions=")+ conditions)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
