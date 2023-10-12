from enum import Enum


schema_loc = "{http://www.w3.org/2001/XMLSchema}"

# XSD
schema_tag = f"{schema_loc}schema"
annotation_tag = f"{schema_loc}annotation"
documentation_tag = f"{schema_loc}documentation"
element_tag = f"{schema_loc}element"
enumeration_tag = f"{schema_loc}enumeration"
complexType_tag = f"{schema_loc}complexType"
group_tag = f"{schema_loc}group"
sequence_tag = f"{schema_loc}sequence"
attribute_tag = f"{schema_loc}attribute"
simple_type_tag = f"{schema_loc}simpleType"
restriction_tag = f"{schema_loc}restriction"
pattern_tag = f"{schema_loc}pattern"

# Attribute values
max_occurs_unbounded = "unbounded"

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
xs_byte= "xs:byte"
xs_boolean = "xs:boolean"
xs_decimal = "xs:decimal"
xs_integer = "xs:integer"
xs_positiveInteger = "xs:positiveInteger"
xs_string = "xs:string"
xs_token = "xs:token"

# JADN => XSD
primitives = {
    "Binary" : xs_byte,
    "Boolean" : xs_boolean,
    "Integer" : xs_integer,
    "Number" : xs_decimal,
    "String" : xs_string
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