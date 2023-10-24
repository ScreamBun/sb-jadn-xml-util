

import xml.etree.ElementTree as ET
from constants.jadn_constants import *
from constants.xsd_constants import *
from helpers.jadn_helper import get_active_type_option_vals, get_type_option_vals
from logic.builder.xsd_builder import build_integer_format_opts, build_number_format_opts


def test_build_number_format_opts():
    root = ET.Element(schema_tag)
    tests = { 
                1 : ["y1", "z2", "/f16"],
                2 : ["y1", "z2", "/f32"],
                3 : ["y1"],
                4 : ["z2"],
                5 : ["y1", "z2"],
                6 : ["/f16"],
                7 : ["/f32"],
             }
    
    for test in tests.items():
        active_jadn_opts = get_active_type_option_vals(test[1], NUMBER_CONST)
        build_number_format_opts(root, active_jadn_opts, NUMBER_CONST)
    
        for child in root:
            print(child.tag, child.attrib)    
    
        assert root != None 


def test_build_integer_format_opts():
    root = ET.Element(schema_tag)
    tests = { 
                1 : ["{-12", "}2", "/duration"],
                2 : ["{1", "}2", "/i8"],
                3 : ["{1", "}2", "/i16"],
                4 : ["{1", "}2", "/i32"],
                5 : ["{1", "}2", "/u\\d+"]
             }
    
    for test in tests.items():
        active_jadn_opts = get_active_type_option_vals(test[1], INTEGER_CONST)
        build_integer_format_opts(root, active_jadn_opts, INTEGER_CONST)
    
        for child in root:
            print(child.tag, child.attrib)    
    
        assert root != None 


def test_get_active_type_option_vals():
    
    opts = ["{3", "}33", "/date-time"]
    base_type = STRING_CONST
    return_val = get_active_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "3"
    assert return_val.get("}") == "33" 
    assert return_val.get("/") == "date-time"
    assert return_val.get("%") == None 


def test_string_get_type_option_vals():
    
    opts = ["{3", "}33", "/date-time", "%zxcv"]
    base_type = STRING_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "3"
    assert return_val.get("}") == "33" 
    assert return_val.get("/") == "date-time"
    assert return_val.get("%") == "zxcv"  


def test_number_get_type_option_vals():
    
    opts = ["y1", "z21", "/f32"]
    base_type = NUMBER_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("y") == "1"
    assert return_val.get("z") == "21" 
    assert return_val.get("/") == "f32" 


def test_integer_get_type_option_vals():
    
    opts = ["{2", "}12", "/u\\d+"]
    base_type = INTEGER_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("/") == "u\\d+" 


def test_boolen_get_type_option_vals():
    
    opts = []
    base_type = BOOLEAN_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    for opt_val in return_val.values():
        assert opt_val == None
    

def test_binary_get_type_option_vals():
    
    opts = ["{1", "}11", "/eui"]
    base_type = BINARY_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "1"
    assert return_val.get("}") == "11" 
    assert return_val.get("/") == "eui" 

    
def test_arrayof_unordered_get_type_option_vals():
    
    opts = ["*Binary", "{2", "}12", "b"]
    base_type = ARRAYOF_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Binary"
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("b") == "b" 


def test_arrayof_unique_get_type_option_vals():
    
    opts = ["*Binary", "{2", "}12", "q"]
    base_type = ARRAYOF_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Binary"
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("q") == "q" 
    
    
def test_arrayof_set_get_type_option_vals():
    
    opts = ["*Binary", "{2", "}12", "s"]
    base_type = ARRAYOF_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Binary"
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("s") == "s"     


def test_mapof_get_type_option_vals():
    
    opts = ["*Boolean", "+Array", "{5", "}10"]
    base_type = MAPOF_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Boolean"
    assert return_val.get("+") == "Array"
    assert return_val.get("{") == "5"
    assert return_val.get("}") == "10" 


def test_array_get_type_option_vals():
    
    opts = ["X", "/ipv4-net", "{8", "}10"]
    base_type = ARRAY_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("X") == "X"
    assert return_val.get("/") == "ipv4-net"
    assert return_val.get("{") == "8"
    assert return_val.get("}") == "10"  


def test_choice_get_type_option_vals():
    
    opts = ["=", "X"]
    base_type = CHOICE_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("=") == "="
    assert return_val.get("X") == "X"


def test_enumerated_get_type_option_vals():
    
    opts = ["=", "#enum-test", ">enum-pointer", "X"]
    base_type = ENUMERATED_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("=") == "="
    assert return_val.get("#") == "enum-test"
    assert return_val.get(">") == "enum-pointer"
    assert return_val.get("X") == "X"
    
    
def test_record_get_type_option_vals():
    
    opts = ["X", "{1", "}2"]
    base_type = RECORD_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("X") == "X"
    assert return_val.get("{") == "1"
    assert return_val.get("}") == "2"    


def test_map_get_type_option_vals():
    
    opts = ["=", "X", "{4", "}8"]
    base_type = MAP_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("=") == "="
    assert return_val.get("X") == "X"
    assert return_val.get("{") == "4"
    assert return_val.get("}") == "8"
