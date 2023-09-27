schema_loc = "{http://www.w3.org/2001/XMLSchema}"

# JADN

## JADN element names
type_name = 'type_name'
base_type = 'base_type'
type_options = 'type_options'
type_description = 'type_description'
fields = 'fields'

# XSD
schema_tag = f"{schema_loc}schema"
annotation_tag = f"{schema_loc}annotation"
documentation_tag = f"{schema_loc}documentation"
element_tag = f"{schema_loc}element"
complexType_tag = f"{schema_loc}complexType"
sequence_tag = f"{schema_loc}sequence"
attribute_tag = f"{schema_loc}attribute"
simple_type_tag = f"{schema_loc}simpleType"
restriction_tag = f"{schema_loc}restriction"
pattern_tag = f"{schema_loc}pattern"

# REF: https://www.w3.org/TR/xmlschema-2/#built-in-primitive-datatypes
# binary?
# float?
# double?
# duration?
# dataTime?
# time?
# date?
# gYearMonth?
# gYear?
# gMonthDay?
# gDay?
# gMonth?
# hexBinary?
# base64Binary?
# anyURI?
# QName?
# NOTATION?
xs_boolean = "xs:boolean"
xs_decimal = "xs:decimal"
xs_positiveInteger = "xs:positiveInteger"
xs_string = "xs:string"

options_keys = {
    "regex" : "%"
}

# JADN => XSD
primitives = {
      "String" : xs_string,
      "Number" : xs_decimal,
      "Integer" : xs_positiveInteger,
      "Boolean" : xs_boolean
    }

enumerations = {
    "Enumerated" : "tbd"
}

specializations = {
    "Choice" : "tbd"
}

structures = {
    "ArrayOf" : "tbd",
    "MapOf" : "tbd",    
    "Array" : "tbd",    
    "Map" : "tbd",
    "Record" : "tbd"
}