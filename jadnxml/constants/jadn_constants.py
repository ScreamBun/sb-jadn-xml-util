# Core datatypesVTYPE_CONST
from jadnxml.utils.ext_dict import FrozenDict

# Type Constants
# Primitives
BINARY_CONST = "Binary"
BOOLEAN_CONST = "Boolean"
INTEGER_CONST = "Integer"
NUMBER_CONST = "Number"
STRING_CONST = "String"
# Selectors
ENUMERATED_CONST = "Enumerated"
CHOICE_CONST = "Choice"
# Structured
ARRAY_CONST = "Array"
ARRAYOF_CONST = "ArrayOf"
MAP_CONST = "Map"
MAPOF_CONST = "MapOf"
RECORD_CONST = "Record"

# Type Option Constants
ID_CONST = "id"
VTYPE_CONST = "vtype"
KTYPE_CONST = "ktype"
ENUM_CONST = "enum"
POINTER_CONST = "pointer"
FORMAT_CONST = "format"
PATTERN_CONST = "pattern"
MINF_CONST = "minf"
MAXF_CONST = "maxf"
MINV_CONST = "minv"
MAXV_CONST = "maxv"
UNIQUE_CONST = "unique"
SET_CONST = "set"
UNORDERED_CONST = "unordered"
EXTEND_CONST = "extend"
DEFAULT_CONST = "default"

# Field Option Constants
MINC_CONST = "minc"
MAXC_CONST = "maxc"
TAGID_CONST = "tagid"
DIR_CONST = "dir"
KEY_CONST = "key"
LINK_CONST = "link"

# Format Option Constants
# Dict Keys
DATE_TIME = "date-time"
DATE = "date"
TIME = "time"
DURATION = "duration"
EMAIL = "email"
IDN_EMAIL = "idn-email"
HOSTNAME = "hostname"
IDN_HOSTNAME = "idn-hostname"
EUI = "eui"
F16 = "f16"
F32 = "f32"
F64 = "f64"
F16_DIGITS = "4"
F32_DIGITS = "6"
IRI = "iri"
IRI_REFERENCE = "iri-reference"
IPV4 = "ipv4"
IPV6 = "ipv6"
IPV4_ADDR = "ipv4-addr"
IPV6_ADDR = "ipv6-addr"
IPV4_NET = "ipv4-net"
IPV6_NET = "ipv6-net"
I8 = "i8"
I16 = "i16"
I32 = "i32"
JSON_POINTER = "json-pointer"
REGEX = "regex"
REL_JSON_POINTER = "relative-json-pointer"
UNSIGNED_BITS = "u\\d+"
URI = "uri"
URI_REFERENCE = "uri-reference"
URI_TEMPLATE = "uri-template"
UUID = "uuid"

BINARY_REG_CONST = "\\\\b[01]+\\\\b"

# Patterns
#TODO: Need an offical email regex
EMAIL_REG_CONST = "[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}"
#TODO: Need an offical idn-email regex
IDN_EMAIL_REG_CONST = "[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}"
#TODO: Need an offical hostname regex
HOSTNAME_REG_CONST = "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])"
#TODO: Need idn-hostname regex
IDN_HOSTNAME_REG_CONST = "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])"
IPV4_REG_CONST = "((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|([0-9]))[.]((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|([0-9]))[.]((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|([0-9]))[.]((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|([0-9]))"
IPV6_REG_CONST = "((([0-9A-Fa-f]{1,4}:){1,6}:)|(([0-9A-Fa-f]{1,4}:){7}))([0-9A-Fa-f]{1,4})"
#TODO: Need uri regex from RFC 3986 Appendix-B
URI_REG_CONST = "(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})"
#TODO: Need uri-ref regex
URI_REF_REG_CONST = "(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})"
#TODO: Need uri-template regex
URI_TEMPLATE_REG_CONST = "(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})"
UUID4_REG_CONST = "^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
IRI_REG_CONST = "<(.*)>"
IRI_REF_REG_CONST = "<(.*)>"
# REG_REG_CONST = "\/((?![*+?])(?:[^\r\n\[/\\]|\\.|\[(?:[^\r\n\]\\]|\\.)*\])+)\/((?:g(?:im?|mi?)?|i(?:gm?|mg?)?|m(?:gi?|ig?)?)?)"
REG_REG_CONST = "\*."

# Dict
#   key               type[0],        min[1],        max[2],       regex[3],               description [4]
FORMAT_OPTIONS_FROZ_DICT = FrozenDict({
    DATE_TIME:        [STRING_CONST,  "",            "",           "",                     "JSON Schema Section 7.3.1"],
    DATE:             [STRING_CONST,  "",            "",           "",                     "JSON Schema Section 7.3.1"],
    DURATION:         [INTEGER_CONST, "",            "",           "",                     "JSON Schema Section 7.3.1"],
    TIME:             [STRING_CONST,  "",            "",           "",                     "JSON Schema Section 7.3.1"],
    EMAIL:            [STRING_CONST,  "",            "",           EMAIL_REG_CONST,        "JSON Schema Section 7.3.2"],
    IDN_EMAIL:        [STRING_CONST,  "",            "",           IDN_EMAIL_REG_CONST,    "JSON Schema Section 7.3.2"],
    HOSTNAME:         [STRING_CONST,  "",            "",           HOSTNAME_REG_CONST,     "JSON Schema Section 7.3.3"],
    IDN_HOSTNAME:     [STRING_CONST,  "",            "",           IDN_HOSTNAME_REG_CONST, "JSON Schema Section 7.3.3"],    
    IPV4:             [STRING_CONST,  "",            "",           IPV4_REG_CONST,         "JSON Schema Section 7.3.4"],    
    IPV6:             [STRING_CONST,  "",            "",           IPV6_REG_CONST,         "JSON Schema Section 7.3.4"],    
    URI:              [STRING_CONST,  "",            "",           URI_REG_CONST,          "JSON Schema Section 7.3.5"],    
    URI_REFERENCE:    [STRING_CONST,  "",            "",           URI_REF_REG_CONST,      "JSON Schema Section 7.3.5"],    
    URI_TEMPLATE:     [STRING_CONST,  "",            "",           URI_TEMPLATE_REG_CONST, "JSON Schema Section 7.3.6"],     
    UUID:             [STRING_CONST,  "",            "",           UUID4_REG_CONST, "JSON Schema Section 7.3.6"],   
    IRI:              [STRING_CONST,  "",            "",           IRI_REG_CONST,          "JSON Schema Section 7.3.5"],    
    IRI_REFERENCE:    [STRING_CONST,  "",            "",           IRI_REF_REG_CONST,      "JSON Schema Section 7.3.5"],    
    JSON_POINTER:     [STRING_CONST,  "",            "",           "",                     "JSON Schema Section 7.3.7"],    
    REL_JSON_POINTER: [STRING_CONST,  "",            "",           "",                     "JSON Schema Section 7.3.7"],    
    REGEX:            [STRING_CONST,  "",            "",           REG_REG_CONST,          "JSON Schema Section 7.3.8"],
    EUI :             [BINARY_CONST,  "",            "",           "",                     "IEEE Extended Unique Identifier (MAC Address)"],
    F16 :             [NUMBER_CONST,  "",            "",           "",                     "float16: IEEE 754 Half-Precision Float (#7.25)."],
    F32 :             [NUMBER_CONST,  "",            "",           "",                     "float32: IEEE 754 Single-Precision Float (#7.26)."],
    F64 :             [NUMBER_CONST,  "",            "",           "",                     "float64: IEEE 754 Double-Precision Float (#7.27)."],
    IPV4_ADDR :       [BINARY_CONST,  "32",          "32",         BINARY_REG_CONST,       "IPv4 address as specified in RFC 791 Section 3.1"],
    IPV6_ADDR :       [BINARY_CONST,  "32",          "32",         BINARY_REG_CONST,       "IPv6 address as specified in RFC 8200 Section 3"],
    IPV4_NET :        [ARRAY_CONST,   "",            "",           "",                     "Binary IPv4 address and Integer prefix length as specified in RFC 4632 Section 3.1"],
    IPV6_NET :        [ARRAY_CONST,   "",            "",           "",                     "Binary IPv6 address and Integer prefix length as specified in RFC 4291 Section 2.3"],
    I8 :              [INTEGER_CONST, "-128",        "127",        "",                     "Signed 8 bit integer, value must be between -128 and 127."],
    I16 :             [INTEGER_CONST, "-32768",      "32767",      "",                     "Signed 16 bit integer, value must be between -32768 and 32767."],
    I32 :             [INTEGER_CONST, "-2147483648", "2147483647", "",                     "Signed 32 bit integer, value must be between -2147483648 and 2147483647."],
    UNSIGNED_BITS :   [INTEGER_CONST, "",            "",           "",                     "Unsigned integer or bit field of <n> bits, value must be between 0 and 2^<n> - 1."]  
})

PRIMITIVE_TYPES = (BINARY_CONST, BOOLEAN_CONST, INTEGER_CONST, NUMBER_CONST, STRING_CONST)
SELECTOR_TYPES = (ENUMERATED_CONST, CHOICE_CONST)
STRUCTURED_TYPES = (ARRAY_CONST, ARRAYOF_CONST, MAP_CONST, MAPOF_CONST, RECORD_CONST)
FIELD_TYPES = (ENUMERATED_CONST, CHOICE_CONST, ARRAY_CONST, MAP_CONST, RECORD_CONST)  # Types that have defined fields
CORE_TYPES = PRIMITIVE_TYPES + SELECTOR_TYPES + STRUCTURED_TYPES
ALL_TYPES = PRIMITIVE_TYPES + SELECTOR_TYPES + STRUCTURED_TYPES + FIELD_TYPES

# Option Tags/Keys
#   JADN TypeOptions and FieldOptions contain a list of strings, each of which is an option.
#   The first character of an option string is the type ID; the remaining characters are the value.
#   The option string is converted into a Name: Value pair before use.
#   The tables list the unicode codepoint of the ID and the corresponding Name and value type.
TYPE_OPTIONS_ALT = FrozenDict({        # Option ID: (name, value type, canonical order) # ASCII ID
    61: (ID_CONST, lambda x: True, 1),          # "=", Enumerated type and Choice/Map/Record keys are ID not Name
    42: (VTYPE_CONST, lambda x: x, 2),          # "*", Value type for ArrayOf and MapOf
    43: (KTYPE_CONST, lambda x: x, 3),          # "+", Key type for MapOf
    35: (ENUM_CONST, lambda x: x, 4),           # "#", enumeration derived from Array/Choice/Map/Record type
    62: (POINTER_CONST, lambda x: x, 5),        # ">", enumeration of pointers derived from Array/Choice/Map/Record type
    47: (FORMAT_CONST, lambda x: x, 6),         # "/", semantic validation keyword, may affect serialization
    37: (PATTERN_CONST, lambda x: x, 7),        # "%", regular expression that a string must match
    121: (MINF_CONST, float, 8),                # "y", minimum Number value
    122: (MAXF_CONST, float, 9),                # "z", maximum Number value
    123: (MINV_CONST, int, 10),                 # "{", minimum byte or text string length, Integer value, element count
    125: (MAXV_CONST, int, 11),                 # "}", maximum byte or text string length, Integer value, element count
    113: (UNIQUE_CONST, lambda x: True, 12),    # "q", ArrayOf instance must not contain duplicates
    115: (SET_CONST, lambda x: True, 13),       # "s", ArrayOf instance is unordered and unique
    98: (UNORDERED_CONST, lambda x: True, 14),  # "b", ArrayOf instance is unordered and not unique (bag)
    88: (EXTEND_CONST, lambda x: True, 15),     # "X", Type has an extension point where fields may be appended
    33: (DEFAULT_CONST, lambda x: x, 16),       # "!", Default or constant value of instances of this type
})

TYPE_OPTIONS_FROZ_DICT = FrozenDict({
    ID_CONST:"=",        # Enumerated type and Choice/Map/Record keys are ID not Name
    VTYPE_CONST:"*",     # Value type for ArrayOf and MapOf
    KTYPE_CONST:"+",     # Key type for MapOf
    ENUM_CONST:"#",      # Enumeration derived from Array/Choice/Map/Record type
    POINTER_CONST:">",   # Enumeration of pointers derived from Array/Choice/Map/Record type
    FORMAT_CONST:"/",    # Semantic validation keyword, may affect serialization
    PATTERN_CONST:"%",   # Regular expression that a string must match
    MINF_CONST:"y",      # Minimum Number value
    MAXF_CONST:"z",      # Maximum Number value
    MINV_CONST:"{",      # Minimum byte or text string length, Integer value, element count
    MAXV_CONST:"}",      # Maximum byte or text string length, Integer value, element count
    UNIQUE_CONST:"q",    # ArrayOf instance must not contain duplicates
    SET_CONST:"s",       # ArrayOf instance is unordered and unique
    UNORDERED_CONST:"b", # ArrayOf instance is unordered and not unique (bag)
    EXTEND_CONST:"X",    # Type has an extension point where fields may be appended
    DEFAULT_CONST:"!"    # Default or constant value of instances of this type
})

FIELD_OPTIONS_FROZ_DICT = FrozenDict({
    MINC_CONST:"[",      # Minimum cardinality, default = 1, 0 = optional  
    MAXC_CONST:"]",      # Maximum cardinality, default = 1, 0 = default max, >1 = array 
    TAGID_CONST:"&",     # Field containing an explicit tag for this Choice type
    DIR_CONST:"<",       # Pointer enumeration treats field as a group of items
    KEY_CONST:"K",       # Field is a primary key for this type  
    LINK_CONST:"L",      # Field is a foreign key reference to a type instance
})

FIELD_OPTIONS = FrozenDict({
    91: (MINC_CONST, int, 19),                  # "[", minimum cardinality, default = 1, 0 = field is optional
    93: (MAXC_CONST, int, 20),                  # "]", maximum cardinality, default = 1, 0 = inherited max, not 1 = array
    38: (TAGID_CONST, int, 21),                 # "&", field that specifies the type of this field
    60: (DIR_CONST, lambda x: True, 22),        # "<", pointer enumeration treats field as a collection
    75: (KEY_CONST, lambda x: True, 23),        # "K", field is a primary key for this type
    76: (LINK_CONST, lambda x: True, 24)        # "L", field is a link (foreign key) to an instance of FieldType
})

# OPTIONS = FrozenDict({**TYPE_OPTIONS, **FIELD_OPTIONS})
# Pre-computed reverse index - MUST match TYPE_OPTIONS and FIELD_OPTIONS
# OPTION_ID = FrozenDict({v[0]: chr(k) for k, v in OPTIONS.items()})
# ID_OPTIONS = FrozenDict({v: k for k, v in OPTION_ID.items()})

# Option Keys
# TYPE_OPTION_KEYS = tuple(v[0] for v in TYPE_OPTIONS.values())
# FIELD_OPTION_KEYS = tuple(v[0] for v in FIELD_OPTIONS.values())

REQUIRED_TYPE_OPTIONS = FrozenDict(
    # Primitives
    Binary=(),
    Boolean=(),
    Integer=(),
    Number=(),
    String=(),
    # Structures
    Array=(),
    ArrayOf=(VTYPE_CONST, ),
    Choice=(),
    Enumerated=(),
    Map=(),
    MapOf=(KTYPE_CONST, VTYPE_CONST),
    Record=()
)

ALLOWED_TYPE_OPTIONS = FrozenDict(
    # Primitives
    Binary=(MINV_CONST, MAXV_CONST, FORMAT_CONST),
    Boolean=(),
    Integer=(MINV_CONST, MAXV_CONST, FORMAT_CONST),
    Number=(MINF_CONST, MAXF_CONST, FORMAT_CONST),
    String=(MINV_CONST, MAXV_CONST, FORMAT_CONST, PATTERN_CONST),
    # Structures
    Array=(EXTEND_CONST, FORMAT_CONST, MINV_CONST, MAXV_CONST),
    ArrayOf=(VTYPE_CONST, MINV_CONST, MAXV_CONST, UNIQUE_CONST, SET_CONST, UNORDERED_CONST),
    Choice=(ID_CONST, EXTEND_CONST),
    Enumerated=(ID_CONST, ENUM_CONST, POINTER_CONST, EXTEND_CONST),
    Map=(ID_CONST, EXTEND_CONST, MINV_CONST, MAXV_CONST),
    MapOf=(KTYPE_CONST, VTYPE_CONST, MINV_CONST, MAXV_CONST),
    Record=(EXTEND_CONST, MINV_CONST, MAXV_CONST)
)

EXTENSIONS = {
    "AnonymousType",            # TYPE_OPTIONS included in FieldOptions
    "Multiplicity",             # maxc other than 1, or minv other than 0 (optional) or 1 (required)
    "DerivedEnum",              # enum and pointer/dir options, create Enumerated type of fields or JSON Pointers
    "MapOfEnum",                # ktype option specifies an Enumerated type
    "Pointers",                 # TBD
    "Link"                      # key and link options
}

## element names
TYPE_NAME = 'type_name'
BASE_TYPE = 'base_type'
TYPE_OPTIONS = 'type_options'
TYPE_DESCRIPTION = 'type_description'
FIELDS = 'fields'

OPTION_KEYS = {
    "regex" : "%"
}