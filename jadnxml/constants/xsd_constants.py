from enum import Enum


schema_loc = "{http://www.w3.org/2001/XMLSchema}"
# jadn_namespace = "http://docs.oasis-open.org/openc2/ns/jadn/v1.0"
jadn_prefix = "jadn:"
jadn_namespace = "jadn_base_types"
# jadn_base_type_file_loc = "../_data/xsd/jadn_base_types.xsd"
#jadn_base_type_file_loc = "https://raw.githubusercontent.com/ScreamBun/sb-jadn-xml-util/refs/heads/main/_data/xsd/jadn_base_types.xsd"
jadn_base_type_file_loc = "./_data/xsd/jadn_base_types.xsd"

# XSD
schema_tag = f"{schema_loc}schema"
annotation_tag = f"{schema_loc}annotation"
attribute_tag = f"{schema_loc}attribute"
documentation_tag = f"{schema_loc}documentation"
element_tag = f"{schema_loc}element"
choice_tag = f"{schema_loc}choice"
complexType_tag = f"{schema_loc}complexType"
enumeration_tag = f"{schema_loc}enumeration"
field_tag = f"{schema_loc}field"
fraction_digits_tag = f"{schema_loc}fractionDigits"
group_tag = f"{schema_loc}group"
import_tag = f"{schema_loc}import"
max_length_tag = f"{schema_loc}maxLength"
min_length_tag = f"{schema_loc}minLength"
max_inclusive_tag = f"{schema_loc}maxInclusive"
min_inclusive_tag = f"{schema_loc}minInclusive"
pattern_tag = f"{schema_loc}pattern"
restriction_tag = f"{schema_loc}restriction"
selector_tag = f"{schema_loc}selector"
sequence_tag = f"{schema_loc}sequence"
simple_type_tag = f"{schema_loc}simpleType"
unique_tag = f"{schema_loc}unique"

# Attribute values
max_occurs_unbounded = "unbounded"

# REF: https://www.w3.org/TR/xmlschema-2/#built-in-primitive-datatypes
# binary?
xs_float = "xs:float"
xs_double = "xs:double"
# duration?
xs_date = "xs:date"
xs_time = "xs:time"
xs_dateTime = "xs:dateTime"
# gYearMonth?
xs_gYearMonth = "xs:gYearMonth"
# gYear?
xs_gYear = "xs:gYear"
xs_gMonthDay = "xs:gMonthDay"
xs_duration = "xs:duration"
xs_dayTimeDuration = "xs:dayTimeDuration"
xs_yearMonthDuration = "xs:yearMonthDuration"
# gDay?
# gMonth?
# anyURI?
# QName?
# NOTATION?
xs_byte= "xs:byte"
xs_hexBinary= "xs:hexBinary"
xs_b64= "xs:base64Binary"
xs_choice= "xs:choice"
xs_boolean = "xs:boolean"
xs_decimal = "xs:decimal"
xs_enumeration = "xs:enumeration"
xs_fractionDigits = "xs:fractionDigits"
xs_integer = "xs:integer"
xs_positiveInteger = "xs:positiveInteger"
xs_nonNegativeInteger = "xs:nonNegativeInteger"
xs_string = "xs:string"
xs_token = "xs:token"
xs_normalizedString = "xs:normalizedString"
xs_language = "xs:language"
xs_name = "xs:name"
xs_QName = "xs:QName"
xs_anyURI = "xs:anyURI"
xs_notation = "xs:NOTATION"

# JADN => XSD
primitives = {
    "Binary" : xs_byte,
    "Boolean" : xs_boolean,
    "Integer" : xs_integer,
    "Number" : xs_decimal,
    "String" : xs_string
    }

enumerations = {
    "Enumerated" : xs_enumeration
}

specializations = {
    "Choice" : xs_choice
}

structures = {
    "ArrayOf" : "tbd",
    "MapOf" : "tbd",    
    "Array" : "tbd",    
    "Map" : "tbd",
    "Record" : "tbd"
}