
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
    "output_condition_set_ref"
})
public class FileToConditionSetOutput {

    @JsonProperty("output_condition_set_ref")
    private String outputConditionSetRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("output_condition_set_ref")
    public String getOutputConditionSetRef() {
        return outputConditionSetRef;
    }

    @JsonProperty("output_condition_set_ref")
    public void setOutputConditionSetRef(String outputConditionSetRef) {
        this.outputConditionSetRef = outputConditionSetRef;
    }

    public FileToConditionSetOutput withOutputConditionSetRef(String outputConditionSetRef) {
        this.outputConditionSetRef = outputConditionSetRef;
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
        return ((((("FileToConditionSetOutput"+" [outputConditionSetRef=")+ outputConditionSetRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
