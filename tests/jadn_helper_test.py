

import xml.etree.ElementTree as ET

from jadnxml.builder.xsd_builder import build_integer_type_opts, build_number_type_opts, build_string_type_opts, convert_to_xsd_from_file, convert_xsd_from_dict, get_jadn_base_types
from jadnxml.constants.jadn_constants import ARRAY_CONST, ARRAYOF_CONST, BINARY_CONST, BOOLEAN_CONST, CHOICE_CONST, ENUMERATED_CONST, INTEGER_CONST, MAP_CONST, MAPOF_CONST, NUMBER_CONST, RECORD_CONST, STRING_CONST
from jadnxml.constants.xsd_constants import schema_tag
from jadnxml.helpers.jadn_helper import get_active_type_option_vals, get_field_option_val, get_type_option_vals
from jadnxml.utils.utils import read_type_data_from_file


def test_get_jadn_base_types():
    data = get_jadn_base_types()
    
    assert data != None


def test_type_data_from_file():
    data = read_type_data_from_file("test_data.jadn")
    
    assert data != None
    

def test_convert_xsd_from_file():
    converted = convert_to_xsd_from_file("test_data.jadn")
    
    assert converted == True
    
    
def test_convert_xsd_from_dict():
    data_dict = {
                    "info": {
                        "title": "Music Library",
                        "package": "http://fake-audio.org/music-lib",
                        "version": "1.0",
                        "description": "This information model defines a library of audio tracks, organized by album",
                        "license": "CC0-1.0",
                        "exports": ["Library", "Album", "Track"]
                    },
                    "types": [
                        ["Library", "MapOf", ["+Barcode", "*Album", "{1"], "", []],
                        ["Barcode", "String", ["%\\d{12}"], "A UPC-A barcode is 12 digits", []],
                        ["Album", "Record", [], "model for the album", [
                            [1, "artist", "Artist", [], "artist associated with this album"],
                            [2, "title", "String", [], "commonly known title for this album"],
                            [3, "pub_data", "Publication-Data", [], "metadata about album publication"],
                            [4, "tracks", "ArrayOf", ["*Track", "]0"], "individual track descriptions"],
                            [5, "cover_art", "Cover-Art", [], "cover art image for this album"]
                        ]],
                        ["Artist", "Record", [], "interesting information about the performers", [
                            [1, "artist_name", "String", [], "who is this person"],
                            [2, "instruments", "ArrayOf", ["*Instrument", "]0"], "and what do they play"]
                        ]],
                        ["Instrument", "Enumerated", [], "collection of instruments (non-exhaustive)", [
                            [1, "vocals", ""],
                            [2, "guitar", ""],
                            [3, "bass", ""],
                            [4, "drums", ""],
                            [5, "keyboards", ""],
                            [6, "percussion", ""],
                            [7, "brass", ""],
                            [8, "woodwinds", ""],
                            [9, "harmonica", ""]
                        ]],
                        ["Publication-Data", "Record", [], "who and when of publication", [
                            [1, "label", "String", [], "name of record label"],
                            [2, "rel_date", "String", ["/date"], "and when did they let this drop"]
                        ]],
                        ["Track", "Record", [], "information about the individual audio tracks", [
                            [1, "t_number", "Number", [], "track sequence number"],
                            [2, "title", "String", [], "track title"],
                            [3, "length", "String", ["/time"], "length of track"],
                            [4, "featured", "ArrayOf", ["*Artist"], "important guest performers"],
                            [5, "audio", "Audio", [], "the all important content"]
                        ]],
                        ["Audio", "Record", [], "information about what gets played", [
                            [1, "a_format", "Audio-Format", [], "what type of audio file?"],
                            [2, "a_content", "Binary", [], "the audio data in the identified format"]
                        ]],
                        ["Audio-Format", "Enumerated", [], "can only be one, but can extend list", [
                            [1, "MP3", ""],
                            [2, "OGG", ""],
                            [3, "FLAC", ""]
                        ]],
                        ["Cover-Art", "Record", [], "pretty picture for the album", [
                            [1, "i_format", "Image-Format", [], "what type of image file?"],
                            [2, "i_content", "Binary", [], "the image data in the identified format"]
                        ]],
                        ["Image-Format", "Enumerated", [], "can only be one, but can extend list", [
                            [1, "PNG", ""],
                            [2, "JPG", ""]
                        ]]
                    ]
                    }
    data_converted = convert_xsd_from_dict(data_dict)
    
    assert data_converted != None


def test_get_field_option_val():
    tests = { 
                "[" : ["K", "L", "[1", "]2", "&test", "<"],
                "]" : ["K", "L", "[1", "]2", "&test", "<"],
                "&" : ["K", "L", "[1", "]2", "&test", "<"],
                "<" : ["K", "L", "[1", "]2", "&test", "<"],
                "K" : ["K", "L", "[1", "]2", "&test", "<"],
                "L" : ["K", "L", "[1", "]2", "&test", "<"]
             }
    
    for test in tests.items():
        id = test[0]
        opts = test[1]
        field_opt_val = get_field_option_val(opts, id)  

        assert field_opt_val != None
        

def test_build_string_format_opts():
    root = ET.Element(schema_tag)
    tests = { 
                1 : ["/date-time", "%DD-MM-YYYY hh:mm:ss"],
                2 : ["/date", "%DD-MM-YYYY", "{1", "}8"],
                3 : ["/time", "%hh:mm:ss"],
                4 : ["/email", "{1", "}8"],
                5 : ["/idn-email", "{1", "}8"],
                6 : ["/hostname", "{1", "}8"],
                7 : ["/idn-hostname", "{1", "}8"],
                8 : ["/ipv4", "{1", "}8"],
                9 : ["/ipv6", "{1", "}8"],
                10 : ["/uri", "{1", "}8"],
                11 : ["/iri-reference", "{1", "}8"],
                12 : ["/json-pointer", "{1", "}8"],
                13 : ["/relative-json-pointer", "{1", "}8"],
                14 : ["/regex", "{1", "}8"]
             }
    
    for test in tests.items():
        active_jadn_opts = get_active_type_option_vals(test[1], STRING_CONST, {})
        build_string_type_opts(root, active_jadn_opts, STRING_CONST)
    
        for child in root:
            print(child.tag, child.attrib)    
    
        assert root != None 
        

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
        active_jadn_opts = get_active_type_option_vals(test[1], NUMBER_CONST, {})
        build_number_type_opts(root, active_jadn_opts, NUMBER_CONST)
    
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
        active_jadn_opts = get_active_type_option_vals(test[1], INTEGER_CONST, {})
        build_integer_type_opts(root, active_jadn_opts, INTEGER_CONST)
    
        for child in root:
            print(child.tag, child.attrib)    
    
        assert root != None 


def test_get_active_type_option_vals():
    
    opts = ["{3", "}33", "/date-time"]
    base_type = STRING_CONST
    return_val = get_active_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "3"
    assert return_val.get("}") == "33" 
    assert return_val.get("/") == "date-time"
    assert return_val.get("%") == None 


def test_string_get_type_option_vals():
    
    opts = ["{3", "}33", "/date-time", "%zxcv"]
    base_type = STRING_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "3"
    assert return_val.get("}") == "33" 
    assert return_val.get("/") == "date-time"
    assert return_val.get("%") == "zxcv"  


def test_number_get_type_option_vals():
    
    opts = ["y1", "z21", "/f32"]
    base_type = NUMBER_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("y") == "1"
    assert return_val.get("z") == "21" 
    assert return_val.get("/") == "f32" 


def test_integer_get_type_option_vals():
    
    opts = ["{2", "}12", "/u\\d+"]
    base_type = INTEGER_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("/") == "u\\d+" 


def test_boolen_get_type_option_vals():
    
    opts = []
    base_type = BOOLEAN_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    for opt_val in return_val.values():
        assert opt_val == None
    

def test_binary_get_type_option_vals():
    
    opts = ["{1", "}11", "/eui"]
    base_type = BINARY_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("{") == "1"
    assert return_val.get("}") == "11" 
    assert return_val.get("/") == "eui" 

    
def test_arrayof_unordered_get_type_option_vals():
    
    opts = ["*Binary", "{2", "}12", "b"]
    base_type = ARRAYOF_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Binary"
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("b") == "b" 


def test_arrayof_unique_get_type_option_vals():
    
    opts = ["*Binary", "{2", "}12", "q"]
    base_type = ARRAYOF_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Binary"
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("q") == "q" 
    
    
def test_arrayof_set_get_type_option_vals():
    
    opts = ["*Binary", "{2", "}12", "s"]
    base_type = ARRAYOF_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Binary"
    assert return_val.get("{") == "2"
    assert return_val.get("}") == "12" 
    assert return_val.get("s") == "s"     


def test_mapof_get_type_option_vals():
    
    opts = ["*Boolean", "+Array", "{5", "}10"]
    base_type = MAPOF_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("*") == "Boolean"
    assert return_val.get("+") == "Array"
    assert return_val.get("{") == "5"
    assert return_val.get("}") == "10" 


def test_array_get_type_option_vals():
    
    opts = ["X", "/ipv4-net", "{8", "}10"]
    base_type = ARRAY_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("X") == "X"
    assert return_val.get("/") == "ipv4-net"
    assert return_val.get("{") == "8"
    assert return_val.get("}") == "10"  


def test_choice_get_type_option_vals():
    
    opts = ["=", "X"]
    base_type = CHOICE_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("=") == "="
    assert return_val.get("X") == "X"


def test_enumerated_get_type_option_vals():
    
    opts = ["=", "#enum-test", ">enum-pointer", "X"]
    base_type = ENUMERATED_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("=") == "="
    assert return_val.get("#") == "enum-test"
    assert return_val.get(">") == "enum-pointer"
    assert return_val.get("X") == "X"
    
    
def test_record_get_type_option_vals():
    
    opts = ["X", "{1", "}2"]
    base_type = RECORD_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("X") == "X"
    assert return_val.get("{") == "1"
    assert return_val.get("}") == "2"    


def test_map_get_type_option_vals():
    
    opts = ["=", "X", "{4", "}8"]
    base_type = MAP_CONST
    return_val = get_type_option_vals(opts, base_type, {})
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("=") == "="
    assert return_val.get("X") == "X"
    assert return_val.get("{") == "4"
    assert return_val.get("}") == "8"
