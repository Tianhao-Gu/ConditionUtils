
package us.kbase.kbaseexperiments;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: Factor</p>
 * <pre>
 * Internally this is used to store factor information (without the value term) and also a
 * format for returning data in a useful form from get_conditions
 * @optional unit unit_ont_id unit_ont_ref value
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "factor",
    "factor_ont_ref",
    "factor_ont_id",
    "unit",
    "unit_ont_ref",
    "unit_ont_id",
    "value"
})
public class Factor {

    @JsonProperty("factor")
    private String factor;
    @JsonProperty("factor_ont_ref")
    private String factorOntRef;
    @JsonProperty("factor_ont_id")
    private String factorOntId;
    @JsonProperty("unit")
    private String unit;
    @JsonProperty("unit_ont_ref")
    private String unitOntRef;
    @JsonProperty("unit_ont_id")
    private String unitOntId;
    @JsonProperty("value")
    private String value;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("factor")
    public String getFactor() {
        return factor;
    }

    @JsonProperty("factor")
    public void setFactor(String factor) {
        this.factor = factor;
    }

    public Factor withFactor(String factor) {
        this.factor = factor;
        return this;
    }

    @JsonProperty("factor_ont_ref")
    public String getFactorOntRef() {
        return factorOntRef;
    }

    @JsonProperty("factor_ont_ref")
    public void setFactorOntRef(String factorOntRef) {
        this.factorOntRef = factorOntRef;
    }

    public Factor withFactorOntRef(String factorOntRef) {
        this.factorOntRef = factorOntRef;
        return this;
    }

    @JsonProperty("factor_ont_id")
    public String getFactorOntId() {
        return factorOntId;
    }

    @JsonProperty("factor_ont_id")
    public void setFactorOntId(String factorOntId) {
        this.factorOntId = factorOntId;
    }

    public Factor withFactorOntId(String factorOntId) {
        this.factorOntId = factorOntId;
        return this;
    }

    @JsonProperty("unit")
    public String getUnit() {
        return unit;
    }

    @JsonProperty("unit")
    public void setUnit(String unit) {
        this.unit = unit;
    }

    public Factor withUnit(String unit) {
        this.unit = unit;
        return this;
    }

    @JsonProperty("unit_ont_ref")
    public String getUnitOntRef() {
        return unitOntRef;
    }

    @JsonProperty("unit_ont_ref")
    public void setUnitOntRef(String unitOntRef) {
        this.unitOntRef = unitOntRef;
    }

    public Factor withUnitOntRef(String unitOntRef) {
        this.unitOntRef = unitOntRef;
        return this;
    }

    @JsonProperty("unit_ont_id")
    public String getUnitOntId() {
        return unitOntId;
    }

    @JsonProperty("unit_ont_id")
    public void setUnitOntId(String unitOntId) {
        this.unitOntId = unitOntId;
    }

    public Factor withUnitOntId(String unitOntId) {
        this.unitOntId = unitOntId;
        return this;
    }

    @JsonProperty("value")
    public String getValue() {
        return value;
    }

    @JsonProperty("value")
    public void setValue(String value) {
        this.value = value;
    }

    public Factor withValue(String value) {
        this.value = value;
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
        return ((((((((((((((((("Factor"+" [factor=")+ factor)+", factorOntRef=")+ factorOntRef)+", factorOntId=")+ factorOntId)+", unit=")+ unit)+", unitOntRef=")+ unitOntRef)+", unitOntId=")+ unitOntId)+", value=")+ value)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
