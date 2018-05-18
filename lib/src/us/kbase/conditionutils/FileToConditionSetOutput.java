
package us.kbase.conditionutils;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: FileToConditionSetOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "condition_set_ref"
})
public class FileToConditionSetOutput {

    @JsonProperty("condition_set_ref")
    private String conditionSetRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("condition_set_ref")
    public String getConditionSetRef() {
        return conditionSetRef;
    }

    @JsonProperty("condition_set_ref")
    public void setConditionSetRef(String conditionSetRef) {
        this.conditionSetRef = conditionSetRef;
    }

    public FileToConditionSetOutput withConditionSetRef(String conditionSetRef) {
        this.conditionSetRef = conditionSetRef;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("FileToConditionSetOutput"+" [conditionSetRef=")+ conditionSetRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
