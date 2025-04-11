

import json
import xml.etree.ElementTree as ET
from jadnxml.builder.xml_builder import build_xml_from_json

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
    
def test_build_xml_from_json_dict():
    
    json_data = {
        "person": {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
        }
    }
    
    # filename = "output.xml"
    
    tree = build_xml_from_json(json_data)
    
    # ET.indent(tree, space="\t", level=0)
    # tree.write("./_out/" + filename,
    #           xml_declaration=True,encoding='utf-8',
    #           method="xml")  
    
    assert tree != None
    
def test_build_xml_from_json_str():
    
    json_data_dict = {
  "root": {
    "profile": {
      "uuid": "643881CB-cb02-5Ef1-AEfF-Fa5C672b3828",
      "metadata": {
        "title": "ipsum consectetur",
        "last-modified": "/7773270220:04:46.9974551244702Z/i",
        "version": "#",
        "oscal-version": "4",
        "document-ids": [
          {
            "scheme": {
              "c1": "LU9Pl:@46+X?'l{4Qw'3XQaDDv",
              "c2": "http://www.doi.org/"
            },
            "identifier": "V{$Ou*&(}u"
          },
          { "identifier": "Z" }
        ],
        "props": [
          {
            "name": "Oqf9Nz3T7VYsgNjEDn",
            "uuid": "77e7d828-7aCa-5Ca9-b90D-0E3dF6DE3Ddf",
            "ns": "om:6'\x0cJJl)OZ#",
            "value": "9",
            "class": "b_E3z2Iz4ynHmuYqk4VjXkzV.fzC4OQ",
            "remarks": "dolor quas dolor modi exercitationem magnam, molestias, sit amet veniam esse veniam veniam accusantium placeat modi modi officiis veniam reprehenderit elit. reiciendis adipisicing sit elit. ipsum odit adipisicing reprehenderit dolor ipsum adipisicing accusantium reiciendis"
          },
          {
            "name": "txHtmCPxh2Zh79P8KRMfNlbCNfAbrKc3nj7W4u5qS",
            "uuid": "8a2BAB9D-BB48-455e-9EDD-3DdFc7c44F88",
            "ns": "R1-cZ88anjtQ9CRAgbofVvwS+xt7v1ylX3Qb37UrWImpBl0s.FjxV6fIwArZxQlbu19.7kqgBBQVeqo+AlhaV7czIvvz:[%|/p#`(?Eze)=\tQ?+,i?9n@3tN8IU00h'DZdCyrC>5z+F^.e8ia$\"`Q>*v7=gV|A@o4S\r'8Xo{><=)Q",
            "value": "~%1/v_0<[,(,6<u+d:?C''BZEmr#av\\u\\x",
            "class": "K4MhHA7I48n8mHOJdeBzsRMM9H61uCq0s74NPFUyjz3GAHPqhOKlas65neoQ",
            "group": "dua5cH8kaD1bFTnjle0f-WKDZ4h2nwJC0Mq22wlMgdNmPN3jaN_hDg5CCc7W9.f6Ci5h_q2W1Z",
            "remarks": "magnam, officiis esse quas repellendus placeat dolor molestias, elit. sit possimus molestias, ipsum, dolor"
          },
          {
            "name": "J3qJcqw0OhHpYmh-EdUd8YvUW-tFUS2IZ3c1zQR70hM-SG0iVa.5R48uvWPYlNv",
            "uuid": "87ae0aF2-Fefd-4D29-AbDB-E01Ab8bBDdFC",
            "ns": "XW5FuEtKUbGPGIA-aoCrfu28+JCzET22NbyoDJMABjuhYWoe-wrAHrPocBBhbyolV97csJnR0i+WcFIIEhRheDbptLZunvoKQC6A:&C0kXv:!B!V,b,}N Uva{9]OMuOV^3e2\"NP,=v\"t<c%j|{w<D(#{K PJ@!<1=Q5Cm(D*\"Ty\x0bg&nc*Ya}>'ud\x0cN]OGpAj%",
            "value": "_K&[TYe>X\x0b,Idh![J;2HH=",
            "class": "ft6vMF40Mf4Sy.9atT6..I6kf",
            "remarks": "reprehenderit libero culpa! adipisicing reiciendis nobis repellendus adipisicing consectetur adipisicing veniam accusantium"
          }
        ],
        "locations": [
          {
            "uuid": "514e724B-39e2-5849-8fCf-42EC4d6AdA6c",
            "title": "veniam magnam, exercitationem",
            "address": {
              "addr-lines": ["I", "s:h+ST5,^:", "k"],
              "state": "G",
              "postal-code": "k",
              "country": "PNX,s\x0b6K>\\xQ9OS]^l 7@&z,zU\"#xqZ?7"
            },
            "email-addresses": [{ "c1": "s/\\kZ\x0ccR>k|yO&b]e" }],
            "urls": [
              "RZdrV4Ivzzf5zk1xSJ65gbqjNAewNTBCUKrqw89yhuxEhbRDLDYNuOl9j:(o$'j!VG!W1i%oqPCfA\x0c'_\\n*s@T*xJ?Lyrs\"&9s(TI c67\x0b~sI*k k<G--c],B,XN9?^\x0c"
            ],
            "props": [
              {
                "name": "_y2gNTuhKrjwvoKMybEElj7YKkjSz6jBW4MD3uxeiFPznmRg4EXL31WDv1NoegA4puUub5XZXWNA",
                "ns": "Ewov4Wb9pa0DvHtXdAEZvhp1cKL6yoKfWr5T:[[>]wF!mAS a#id\x0bj\tM*I'#i,  vIKjJx/\"N#y-9)gUb~o1R/'((=\\- OeUc,*z:C3dW3",
                "value": "\"",
                "class": "bzniMBei4omldu0089pOWMcNPiG5jvNNO_Xzl0KtHnfKtTQprFVpmXUy-g",
                "group": "_CgbJJc36D99-2Cy78qY877iJn1G6Ea3RueGCkrEOPt4T27KGWHouwgg_7OqwM",
                "remarks": "Hic placeat illum molestias, placeat accusantium elit."
              },
              {
                "name": "Hy.1j45AP7RGsXiJzbEVHi9Leu7oicbLSw8tjAXIeUMPKnx_zixvodSAR-0EDSb6zNZcLwKJhvBv.JWgvMi_A1kQq",
                "uuid": "04Fc8cff-453c-59CA-bBe3-DdECea5e002C",
                "value": "1",
                "class": "ZS3HK4clzCOZs3Vk6R0wFtSgq63FRPPcOTfitsd_.Si_ohIz62sMQ7ngXvP6chuCwW_fNPGzqzs5CENY1bQws",
                "remarks": "sit architecto exercitationem reiciendis exercitationem architecto placeat exercitationem accusantium Lorem architecto libero molestias, illum Hic"
              }
            ],
            "links": [
              {
                "href": "consectetur architecto reprehenderit dolor nobis nobis reiciendis reiciendis modi officiis",
                "rel": {
                  "c1": "snBlguWi1OXC0SRPB1C8mJ_NCNf_mBlHbPN8Qh7l8sNfziJkiokdY4imjh6",
                  "c2": "reference"
                },
                "media-type": "0<^IA1x\x0bA:\x0b\rzs^)*=l2Y'v=^A-1W7!",
                "text": "elit. officiis modi"
              },
              {
                "href": "libero reprehenderit adipisicing architecto reiciendis Lorem magnam, libero libero esse consectetur",
                "resource-fragment": "?",
                "text": "ipsum, placeat culpa! officiis"
              }
            ]
          }
        ],
        "parties": [
          {
            "uuid": "fe72Fe3c-bC1f-4eB5-95aF-49d9bC5D52b1",
            "type": {},
            "name": "0",
            "short-name": "s%*N5H7^_!a2x!Y@RPFO](~\x0c9mxGQ[B#G\r[d\\RBv6bB$2o9]r4*F6]kN['CTHANgV\x0c]1-j|wIy",
            "external-ids": [
              {
                "scheme": {
                  "c1": "GLSplrAeYVo:Og&f-6BuNA@>/FWIL@Kf9']uJ!yzKk\rz=eU=\x0b~S\\T:G!fr*40wdRj\x0cT\"4W%1?PKTh6\x0b~r!#/6*etE0P^ac@p|M0x%g,i[(",
                  "c2": "http://orcid.org/"
                },
                "id": "a"
              },
              {
                "scheme": {
                  "c1": "A7nzsi5-AC39LhWV4Gm-hnm:>f'%v2{gp!G#\t\t4B7v;JfS-fJ1jQ8J",
                  "c2": "http://orcid.org/"
                },
                "id": "p"
              }
            ],
            "props": [
              {
                "name": "vxxsHhiMIGLRK9Ko9Lw0BFivn",
                "uuid": "c4D676BB-59eB-43aF-860d-8aB2bF637F94",
                "value": "k",
                "class": "Cf2i1vanEq7Gvngsf66eEp8px435JQx5lnUCs3OHsBJQxLNMYaASHyQesnAP9ddtWKTmXWbCIEPHCnv57o.WAV8--GoOvsG",
                "group": "knahZK7S0RMu_dzKPMyjH8vrASvOLv.",
                "remarks": "accusantium ipsum molestias, elit. esse repellendus architecto amet modi repellendus quas Hic possimus libero reiciendis libero"
              },
              {
                "name": "p.xHMAyBtRZ7kSDSLgRSgjqXlZNjZdwcpML6XYadUPP.uO9Mk0sVMbUCg273aDs1MxV2rIU-gQEExqzbjEQpw3go",
                "ns": "PH.7bI282ygugy2mlYC-PGaH4.wEAiLIAyWcx4NQf0.Q-4Y5Q0Rtr08w3hgdviDtsIpeu1-5m6Rz3w5flBNy+cGCG28t.DloRRc9N:9T\"3IWx>1*.+f=')Z`4V%6=~o\rEE!VP|\t$l\"Oe\x0bb/-wV,bvJ(\x0c3e%'K_? 3xU`T4>_xK2r\x0c#",
                "value": "#d,~60H\x0bq+$8\x0boH;QSG^6,T@",
                "class": "dLaIScEn_QdL",
                "group": "TSZfD2aJEdiJZR-HX8WWbrDrftv_YfnVr2FeNjD-3Edf1foM5bLJDqj.rlikwxFl3kUv4bYT-"
              }
            ],
            "links": [
              {
                "href": "nobis libero libero nobis",
                "rel": { "c1": "Ud83mXf0I" },
                "resource-fragment": "#",
                "text": "illum exercitationem adipisicing ipsum, Hic"
              }
            ],
            "email-addresses": [{ "c1": "," }, { "c1": "\\" }, {}],
            "member-of-organizations": ["a2c3a2E3-aAD2-5b96-BE8D-20e1d7Ef1d2e"]
          }
        ],
        "actions": [
          {
            "uuid": "5129c845-aF75-5b78-ABdD-8BBF89B3994b",
            "type": "LL5JDx3PuxR2cUvh.qKq6l7vnInO",
            "system": "wtK.hboPtaU9se1moojPZJf-jyFtuqv-oN8z7tba.3ICSZvo+TG9aYBDr8lLR6rByKkoi-CEFLmoekW7v0mfMhEkZsqW-E:8}\\HXByQrY;nOYV>q=I\x0cw^9GCCO?|(#Ixnd",
            "links": [
              {
                "href": "possimus nobis molestias, consectetur",
                "resource-fragment": "j6\r1=ea*{ApDja3)#Mz9XE8J5LcmDyBrm(-\\!916=Mgm/+h#wB3Q=1$dGPi%@,g"
              },
              {
                "href": "reiciendis architecto Hic magnam, placeat elit. nobis repellendus reiciendis exercitationem Lorem",
                "rel": { "c2": "reference" },
                "media-type": "<",
                "resource-fragment": "c",
                "text": "consectetur dolor veniam odit molestias, esse sit accusantium officiis molestias, reprehenderit accusantium veniam amet placeat elit. modi reiciendis reprehenderit magnam,"
              }
            ],
            "responsible-parties": [
              {
                "role-id": "SMDw0MVxLpOHG",
                "party-uuids": [
                  "cDfcAe60-a68e-48e6-a5a0-0fE8Ceedbb5d",
                  "f9fbf2E7-a789-46F9-bBBE-53Ddd4d0A515",
                  "bd3DbA8F-2eE5-56Ab-B2dD-8eC4Cd43fA7B"
                ],
                "props": [
                  {
                    "name": "kd0ZLAy2M7X2ssDZqsmvXWN9xJdqJfmy09wyVwtDJRZZPioM_-ESUw7Bh26nIcT_XgAkpd",
                    "uuid": "1c0D364B-3Cfe-466d-A2aD-7e2ECACC14cB",
                    "ns": "VMNsrQM5iQz3-eec9DiumdDoy6mhMgg.Wns8CoZWU2Jz6SFjeTAb14-uvN6clO:IZJ5(gT'z#3$[|h+mr.\tc\x0b\\`nq5cI{iU#sr",
                    "value": "Z}1xHGB' fUW;V^7#Y`",
                    "group": "jtuI28-_4vM3pO5TNdFelmFYQ57CRYc0ISxrc2RCXyNeR4Wa64Eb3cY3Msskb"
                  },
                  {
                    "name": "s_ACfDruwzcyfWPYywXDXOAgdrHPLURlXWcx0NQuqjbTWbFeATHXW4ljxW-Nrix71j6d",
                    "uuid": "0c4ce4CE-d6Ef-5dCd-9d8C-6555CeD2Bfad",
                    "value": "+XTL/b 6v-<DC}gRq`vf~Rj)EB47QV3)lz[xai$h2Vl'8`^|<lA",
                    "class": "q0Ra"
                  },
                  {
                    "name": "ChNE8XXdFlqZkj2DlAQV5MGa",
                    "ns": "OYgdf:JVy\\@\"i'\x0c>A6FVOq8T{\\6\x0cb9&r0%E.1[3a\x0b'FJ`wQ\x0cD0]:^0F?HnnN|",
                    "value": "?%AF\rb0$=m^wFj7Ebdr"
                  }
                ],
                "remarks": "architecto quas Lorem nobis consectetur Lorem dolor veniam molestias, consectetur culpa! officiis ipsum, quas architecto officiis quas nobis possimus possimus reiciendis architecto libero odit magnam, molestias, illum reprehenderit esse dolor reiciendis consectetur libero odit reprehenderit ipsum, libero officiis odit ipsum,"
              },
              {
                "role-id": "AoNlj6wLGiY-SQV-..d..R8gR1oIHaBRI",
                "party-uuids": [
                  "4A8C06FD-c8Cc-5a5F-A3DF-aD3eFDDEcf51",
                  "B1d5BF69-Da1A-5ccb-AfDE-fCD6fBF7f74a"
                ],
                "props": [
                  {
                    "name": "j2LhjuyvrzK-wX9eB8F-7EI6a13S-6IYEd9yjctCSIt5FmcElsWbMw",
                    "ns": "du6NHPt3V7Wna:%U|TjO1b'MQvoZ5avq4c_Q[/[w5ij\x0cJ*\"+{Dd\r~B<(*AKg);Vg`1'wY>lmE4]<GFWOk k\x0cQapi4H\\f",
                    "value": "D",
                    "class": "cI0mLnwDHbEtlr7RqKzZ9vx3qUP.ZuhHdG0Io6RKVtlcaZAtca39Dy1eCKYXnd1YNa559VICpMNdc_gZQ90ezY",
                    "group": "xd0xLpRPiM0yc",
                    "remarks": "ipsum Lorem"
                  },
                  {
                    "name": "hgpWoYGBbD1DiUQTQN3xa6a0bjkDuJ1S99aEZbVKfJvYvmTT4wLHvGfafGpHxJ5NeZnde3PrGcEfAdhlQXXPk",
                    "uuid": "caD6CAe2-dADE-49eE-8c3f-9afF13F268f9",
                    "ns": "dOEfLQ2k2h5tu7gCAsrauJ1LEybhMRza41m7aVziIiQuxwvn.ryDmpf4mIVxbLD8as2TP6wnSr2er:E)R\x0b=3+Wi,.\\L.Pw#\x0cH#Ox~Z=Xl{q3ycIIR1!p:#<K;_c-vz%zMIiVofcO|uJTua]Pe:n <6;M,2l.E9@v0UPSUc",
                    "value": "xGt\\",
                    "class": "tQvwWwDJRoyr0qWWnLk_arvO..iy33XMk8_4NA35iYGbxIagK7BYLqqHZvlSo8iomwUrs-QBtn3Yqlm1",
                    "remarks": "architecto Hic molestias, reprehenderit amet magnam, modi sit libero possimus adipisicing repellendus"
                  },
                  {
                    "name": "V0p-.QXqcIl1fr7Ep1SNA.CqMjTFmmFnaqaHMaaEZsZvlrQbeHy2y6AGLPULkn5_TlYJ-XtAu2",
                    "uuid": "C3D15eFa-be15-57FF-97f0-ba0Dc5EEAed5",
                    "ns": "sRKdenHw7z2nt0wTPX9HSKohaSQN-pPnkU+x0AyBVwNfUoL-Aj-cVmdL8EWRwbddh.3W6BKzs0k1e:o(c9",
                    "value": "_",
                    "class": "zunFFKRQjaZkw34NzOC.z77im_T420H3G"
                  }
                ],
                "remarks": "esse dolor reprehenderit quas accusantium Hic molestias, architecto"
              }
            ],
            "remarks": "nobis modi illum adipisicing consectetur libero quas amet"
          },
          {
            "uuid": "cECBe8fA-A9b0-435C-b9b5-07d0693279A4",
            "type": "vIXxA_Y8CT8a21OhpQRm23t3zuW91.5zmPdIeoyTtgRh5n9Yf_f",
            "system": "VT1BEh0FfZASUatAJ4f-tMJ8+o:`:(ps}A=%Hj;vi@N`Uq6X'_eIBD",
            "links": [
              {
                "href": "exercitationem possimus",
                "rel": { "c2": "reference" },
                "resource-fragment": "x-{\"qtiSo3-y\x0b:H1kK;nd 9[*#[n-Q&\t3DkR5]U}vr?f-:cY*AM;Q7^X",
                "text": "modi"
              }
            ],
            "responsible-parties": [
              {
                "role-id": "YnOQclS8DOsXAA7b69io8FYVbEdLpxuRt",
                "party-uuids": [
                  "D2447B48-bF0c-5920-9c5B-B18d1ca7F185",
                  "FB25D363-CAEE-441B-b8a3-C64f018FEb6c",
                  "Fa3f3d3b-c7FA-55C8-92B3-F7f0D8Fc32ef"
                ],
                "props": [
                  {
                    "name": "tRG115g62M9fGfkiNBbNsNHd2CDWYfnAWGNpP3jEYwaXn.o5hA0gj0M3S.Gr1NmRCM0AE39hbQQ505m0VnuHfI1FpizW635ld.evq",
                    "uuid": "cAc03Cce-B8C3-5c0E-865E-56e7F8b90C4B",
                    "value": "#",
                    "class": "y1Txlw9aTNOxNpqRRMjccbSDJU",
                    "group": "UuHUYYBLVGjQDdxinn6DNWaSq_vVu_Vi.zLEygh1PFJd3mZNuRz8aFhnvXLL5m13pBekJRQe",
                    "remarks": "molestias, esse reiciendis"
                  }
                ],
                "remarks": "veniam reprehenderit placeat"
              },
              {
                "role-id": "Ad60V",
                "party-uuids": ["473a1984-cadb-4dDe-a9b8-cb8dAa89c8Ef"],
                "props": [
                  {
                    "name": "SjNSW.Ngu1vDXzWvMpylxGFfv46DdH2E8qMJHPSRuiGDoddiyP9erWtNMD",
                    "uuid": "70DC8D91-6559-4fE0-8DCf-9147ef194bEF",
                    "value": "]"
                  },
                  {
                    "name": "JL-RLgeLgErotR.0sCmJOjAvS-A5HuAuote8fKcrSdh_UFuIMxipPqM3vYearV8WWy6SqtOR",
                    "value": "7",
                    "class": "qxkp9SVQjYwRfN5fEnobCJeDm8zNQXLmmlO2qEkFwPGQwofCIkjbIUpWfo9EJe_kU",
                    "remarks": "modi Lorem ipsum, placeat reprehenderit reprehenderit magnam, odit dolor sit ipsum,"
                  },
                  {
                    "name": "IqLfaVxwn3rRjNxNqhoP_gUBCIglNH9xF407rCfrS70l",
                    "uuid": "4a8A1CD2-c3DF-49c9-bfA9-099BDe42FF4e",
                    "value": "3wn svhT).`=W\t8W0NmBC>$A^W`'BzWWvL66w(Z\trhpB>9>yS9Rt^\x0b-s+&"
                  }
                ]
              },
              {
                "role-id": "QsIl1_XrYpaBVDYW-F190St9Jn0prg2bfTRpcOphMx1b77Zy2ic4NRuOV49",
                "party-uuids": [
                  "fcbFB6bD-D56f-4d17-a8ca-d899f68ff1F8",
                  "03d33f9C-B9B7-4E6b-8D02-58Ed1f16BdC9",
                  "8cA924CB-FfFb-4F2b-B8aC-dD1BF2e4826C"
                ],
                "props": [
                  {
                    "name": "JX3yfPKrH2sp3EJWQrOJiugMKuLZlZUQLn-1J2bvmtF8Ps1Wi7H9ns7SNjO4u4iffi5Y5PP2",
                    "ns": "T1e77IWuzFyGUo.uTYqg44r89-wD5Wa2pNbtPo1y8LpLB+yYQzdFAjKpjwXm:~ HS*(h_0&E']RQo+`{;='7r\\n\r1'`nl43$\tmLgj(\"5MD%D`p!`o'es^ag^uI6s(uRo6bI_3F*jspQtVnM~",
                    "value": "uN|n6>W!0P)+pKq4^k?*F5dK@GV4-L^\tBA^iNGv\"wm5:aYb-?x\"[>gP!~%K{/9D\"\"9LE2y>:-9,Ho:#12})|WA:X",
                    "group": "YD_27xYSd5grEznrdK.Unj08JfEzSAe0Q-Z_YgsFBkFy-ayFl"
                  },
                  {
                    "name": "WzqoQh",
                    "ns": "H8ZcC+:26o&lseU6/L_*@\t]VrKXXI+P8%A}adSiYpl#z=W$(&\\B9`?<_{Z^xbyUv)N4V7\x0b0`D|NDh=YYJ^,,LusbWP\r\"eM",
                    "value": "/",
                    "class": "poKl.P6gzF0X23JcsIyw3JGRTpacXfe6vsJWnMP5_sR7S8eHPA4dcCpWib6jvEjTLV",
                    "remarks": "illum adipisicing accusantium illum culpa! quas exercitationem adipisicing"
                  },
                  {
                    "name": "aKNJ915-Y7a5UL057jBa0.wDNYvXqm7E2-qrMnm-MCVRUilpurLngl5x5RoyX60EGzi1uWX7jpn4nw_Ugs5x",
                    "ns": "FQBOy+-Bp6xYWh89Wf5tGB3PkE0YJjCLH.Ij3ZtubAlCAB8KSaPlmpFg47DKE:'Kn.\x0cr/fW\\%rD)#1\taVrO=&M\"\t.ZLF$ja<Z;WAPkv6_:,gb%y84%.|~ihdq\"I$_5Z$Vr^LJlg\ra|Uq<",
                    "value": "[7#/E^5\\@El%w;<6^mW7qrK+jqU|R=;{RZD.)v -I\\iEM{\\M#"
                  }
                ],
                "links": [
                  {
                    "href": "amet molestias, placeat veniam magnam, esse elit.",
                    "text": "Hic veniam esse placeat nobis reprehenderit reprehenderit Hic molestias, odit odit Lorem adipisicing modi consectetur molestias, veniam molestias, adipisicing magnam, repellendus reiciendis veniam odit dolor illum accusantium nobis culpa! quas elit. exercitationem elit. esse exercitationem esse odit magnam, culpa! illum dolor amet adipisicing libero libero esse placeat ipsum, adipisicing amet dolor placeat reiciendis illum"
                  },
                  {
                    "href": "adipisicing adipisicing odit reprehenderit",
                    "rel": {},
                    "resource-fragment": "_F8EL|~\rz\"@7$C}NwQ+HIh_)Rx0",
                    "text": "molestias, adipisicing magnam, ipsum, officiis repellendus nobis"
                  },
                  {
                    "href": "illum elit. reiciendis Hic ipsum modi Hic adipisicing ipsum amet",
                    "media-type": "Cj M{j5J?X<?}6$8T WkQ7}s)VZXB(e$3%L[rgLt`TblYt!Sf)JUO6o\rBMnElI",
                    "resource-fragment": "uMZ\"vv\"C>rQS\"77-D \x0b!Ng\t^A-!U7W|wQ.H:v3(n6dq_e`[\x0cJ$"
                  }
                ]
              }
            ],
            "remarks": "culpa! elit. magnam, libero consectetur exercitationem"
          },
          {
            "uuid": "9D64d753-fc18-4cfC-Af92-72e7924f8BD2",
            "date": "/310380-5728:01-23/i",
            "type": "yaP7H-.JanDaMd2rHSF.dpJnYcr2lsbVFfWVTZT.CMhV49v8Z_7hhB6OVBlJq3sPRv1B5jmNXayKHj35rryPp7Q0okdj9r2P1k",
            "system": "Pv+NMPHTWV2SEStx+Ud:}Tvxg!Q^E\\Y\tg \"\x0b%fyTz2-q\x0c~4\tgDq6J*'++a\"r$S'Zy:%ko&7RxFX`)\tsbAJsGV\x0bEtbhWg4|g=.XVVmI,#{Er-^VP%]",
            "props": [
              {
                "name": "kh3d31lriuZIMXSopua.01Q7F6LaC1HueoF_ZXS0waxYUQO",
                "value": "?",
                "class": "oRezfeoISJhRj_R6w",
                "group": "HySOol23vLNrCWbYySiCxTsFOvDsRpEy8HWPFa6S7ZySyold68iLM",
                "remarks": "odit possimus Hic reprehenderit esse elit. modi Lorem"
              },
              { "name": "knN", "value": "zw<", "remarks": "Hic" },
              {
                "name": "lnHE7pgIdQ9KACH3id-UxICw07uwXmARQ9sfWW1aAhKOI3oJIqLg9y2xQ2X3rdBL5fnP-Tilb",
                "uuid": "01BF2f45-Dc52-51B6-a180-fFede3d42aB4",
                "value": "u",
                "class": "BLkS9yUwwe_YG_.EkSWvdRs5YJzVYNDYmRHL1qtL0ya_8ZbSoOF6p1bV9oNRYqie8WPmh-zvRZla36Du0cy8x8lNYl_fveP3",
                "group": "em7XXQlAtCQh91k1W8BRTNwg"
              }
            ],
            "links": [
              {
                "href": "odit libero elit. Hic illum exercitationem",
                "rel": { "c2": "reference" },
                "resource-fragment": "+J<sv~Huv~EJSKDxj%jo\\,\x0b1SX:s5E-HvkZSZPM[9T1HBa4+",
                "text": "reprehenderit sit molestias, odit"
              }
            ]
          }
        ]
      },
      "imports": [
        {
          "href": "modi nobis repellendus",
          "include-all": {},
          "include-controls": [
            [
              {
                "with-child-controls": {
                  "c1": "DFNgtus7t2d7kHI9z_vn9avChK8P.7ERUk7zJP38gP27yK1xtU_Dfm6sBQ9fHilobS7NwV9_5VT5b61iy5Sm-yy",
                  "c2": "no"
                },
                "matching": []
              }
            ],
            [
              {
                "with-ids": [
                  [
                    "hUTQPCGi-RsY8dGr_iolca2s1icuWusPnJpkPjzJlJe-CE",
                    "OgN.Uy.wA_q5WT3gyaInF1a.DAx7xZfkA_-zv_SRiGOygPihdz2ONS.9bB.XN8aagsvUhvI45nIoygR6wVtRwf9erGkbyjEN"
                  ],
                  [
                    "AqHZCQeQ4H5L3gVy8OS",
                    "dL2Etm1KB6x081fJEophjCKH-8XTBuVMCCnasvhHr1ekYJU8TF7BE1Zwc9_fedHqjLIY10eMv",
                    "oP1zAuJKf6wADa9_s3-nb3y05y9UCRYjou17A-lJo9Xmo2ZWDSU4FDg8cO7zVGH2OqZJ6Ui99Gyz.jZsKrm0JOhCiC7mBA"
                  ],
                  [],
                  [
                    "YQ_TBjlTv4DIgpEyJzAR._VkvFI7txJiJdwAupceLyHOEWdUj8G433RYemqUJvKQI13k-pyFBiNbGXTXvLUw86"
                  ],
                  [
                    "ZCzW",
                    "m4.dPEl3V1BZg4SI.0Jc2NuX9KXR4XH.MMbF6V9FLoQJkRJjfh49cU2oPxfSmyCjr1rm1nLDnh3wqmuyDrDPAF-fJlMoKHyHHKO",
                    "AojT8MGs"
                  ]
                ]
              },
              {}
            ],
            [{}],
            [
              {
                "matching": [
                  { "pattern": "{" },
                  {
                    "pattern": "N&u}5B%m8]?1\x0b1\"\t+\rD#+w9c_m!h6Q\x0cq8UsZS9f+]`C%2!O\rHU{u?l^rDNX#q[b"
                  },
                  {
                    "pattern": "M0\x0baXTSDNeUmZ6}$j^>AmADFI[2w\rjoQy\r:wbFx(SJsqdrtGUe?hZ\rg90W.xA"
                  }
                ]
              },
              {}
            ]
          ]
        },
        {
          "href": "veniam officiis repellendus",
          "include-all": {},
          "include-controls": [
            [
              {
                "with-child-controls": {},
                "matching": [
                  {
                    "pattern": "CTp]QFO{#,uW`%nZ\\B<Xmdwg.a7e{CA\x0bhgsAi UK\tZR9m|V;o0${6+VwOeF->"
                  }
                ]
              },
              {
                "with-child-controls": { "c2": "no" },
                "with-ids": [
                  [
                    "iijJg3KOYbzKvgGCe8VCI3u8Ia07pSo647nJ2RI4oNDlYI3hZ50DG1.Z99EXZs"
                  ],
                  [
                    "duNuSA3Tef5AKOYIu5pBhPlaXmW",
                    "ygti.LVJauaR",
                    "RCsC2zo0vOVQAygzxwQT3i_YpNWbis-M-pLJv1bQRK6e_tswhMIXNk"
                  ],
                  [
                    "jas5wccS8R4UEncmz",
                    "ET.Cl3e5pVBwrXDRaSGAB.VoPqlyujwR-eI2CKop",
                    "wfHESe2Tkyzkw33N3etFf9XI8BUheew35uz0b.xz0RaCmAMSkW76972fOkK7KdFo91"
                  ],
                  [
                    "i.uv3ZTWJmDzIglm8LZsGkPqo73tHvdPylU9GCBhQ19YK3LY4UMpf9gMhByRrsM0RdjWFtAvmrKuA.T5NYXUHf492E0Yamt"
                  ],
                  []
                ],
                "matching": [{ "pattern": "4" }, {}, {}]
              },
              {
                "with-child-controls": {
                  "c1": "Iz5l-C2ugLys-GrMOm8AnadtbIxIqyfj_frLIgkOTCMya9i_JA_CLLbm"
                },
                "with-ids": [
                  [
                    "OoY.gf88pSmSjf_8-HdbOP5XJf71fu4yl",
                    "teyT08p7o58lDlXPq0",
                    "BskrRTt7J5vCoBiN_Y1VkWxWmYUiW5I0yuERlerdGJ4b_LH"
                  ]
                ]
              }
            ],
            [
              {
                "with-ids": [
                  [],
                  [
                    "Euf1Bp6tQfiGESWcoylgmRs3Zr1CB36NiPc5_s0Ee9Jh9YKf.-C9AXtnIeqBx6Ay4pPjHbCjGHKBYGphgNNV3rg6Cte-H",
                    "RHhgbOlyf6PzSG85Zj7Li17WKT7DHvHuJXGYe8zv8jrQkS2rABGjDPARd_R1T877sBdZZCXdK_x17q."
                  ],
                  []
                ],
                "matching": [{}, { "pattern": "V" }]
              },
              {
                "with-child-controls": { "c2": "yes" },
                "with-ids": [
                  [
                    "T97",
                    "coN1laim43rp_QOnLXv-WrZR7wXYhKnUpKgraFHVC02jVc2DzmKSbyAtkof0k.WUFPodxPez4yJ.raSfWKM",
                    "ItoFqQfw31iJ_LTy8ZXn-yiLHoHhfXAb"
                  ],
                  [
                    "Q4dXtaAdoMxhfYR1CPeUv50owXGAq5Uv1GSTbqdxNkV2AfP0nW.LCcC-IDclVX6l0vv3bdBc8JP8702",
                    "djxjoPsSHpmJuoroTjmf.ys8gFGkGtvHj_MYuNSy9"
                  ]
                ],
                "matching": [{}]
              }
            ],
            [],
            [],
            [
              {
                "with-ids": [
                  ["DPiPi34gYkHt9KzB2VrxLnLLsnCG-hAmEDxvOwbHFsoOCxZx"],
                  [
                    "eUPP_T6dmyam3FUoklG5oT.ZqrBb03OOMfe3ll3mPHiopQd61pOtKK1eQ",
                    "CrfQSSOVKHpnVSAAn4jBx2_kPeEYOcobpuMX_JTmGCZcneM1AS8_jfNGPTS1WgTLR7_eVpln-yUA_rU3-u3"
                  ],
                  [],
                  [
                    "ZczMS0qCikuw0OkluDJMk0r45eOUQbkxX95JjHexXYbBdT3JiILFB4foxlr5G-Q2Twa0pAUuGFUmRIVU1q_RC_0",
                    "Oy2JWTWjyYPBFp7bYWsR62L1",
                    "YvB_sCxKS3bhFGGekoMFYTZ6VmSKJj8r.Wehx55H_nt2UD_T0ot5UIggGIdqfHEX5pcwLkO_"
                  ]
                ],
                "matching": [{ "pattern": "3" }]
              }
            ]
          ],
          "exclude-controls": [
            [
              {
                "with-child-controls": { "c2": "yes" },
                "matching": [
                  {
                    "pattern": "%W:Q/o5\rJ\x0blDz}|_:Fpl %<r\"[ tfG4ZqozO#lMsbDymtL9AWq`kx\x0b~db-H]dz IY.N.\x0cXDI]G4U%e_{!{c6It}Jt4~?0j |,}+"
                  }
                ]
              }
            ],
            [
              {
                "with-ids": [
                  ["MzKrl2KwhP2kkB73RlfMjMlXix"],
                  [],
                  [
                    "DnTvSwwiYz7b9_uEAxFjcsU.Alxol909EitSsbdXhKmdyFFdj638zmcptregWEHRL8158Caf9eo62ccJr-kRBVQ6",
                    "XXwXmw6stx2nui0r7o1tfrRK6wj8Uwec4YU_"
                  ]
                ],
                "matching": []
              },
              {
                "with-child-controls": {
                  "c1": "fCLmj5F.plJAskXeRW_wL3fEmyiOdcdGTVssZ1-j8x2Ih-fTMQE1tkVpivRbLGxamsRi5vM4o6VU1WJPzZeoM6b1y7q9dt7"
                },
                "matching": [{ "pattern": "B" }, {}]
              },
              {
                "with-ids": [
                  [
                    "NEq5hKIIF222.nrFxfj94x38CsHfDrlplmbGsFEf0u",
                    "BJrv0s5yIX-uE29Za_jt2k_h"
                  ],
                  [
                    "pZEJbe4Oufz2M2OMeGcf_144HEPJErfB2tajfFiUiUT6y.vgJBbgg29Po-6MljeSzbn0-fcfweNEc34qn7Mujou8un_w4HPhN239",
                    "SYfeKBpitRAYB2T9g2uhF3W8Fa3inXGapCt_9JxLTyTzBlUzNZtrUK",
                    "QY"
                  ],
                  ["bIsJOSg"]
                ]
              }
            ],
            [
              {
                "with-ids": [
                  ["sw0_cTW", "_C94xDQCPa2SDTByw6"],
                  [
                    "PHo0nz5IlJIkT.R6grbfG3q-zRYrjkmeqdEHJ7Yl1pxEoIXKQusEwpG5.gwI",
                    "yW0WzGmwtEMtFWaBmaCINWB5Pvc07P7lsMH",
                    "y5XImdT.sOj46GtRm_fLrHFm2wNVZxOHcyJmMKt2OSpxrcJu-JBRL4FoAPr1iLKJls"
                  ],
                  ["k3jojEwpWRphtBXLRbKv4t.0k0"]
                ],
                "matching": [{}]
              },
              {
                "with-ids": [
                  [
                    "Ndpcag49gDHKC54Z-BOn85s_",
                    "taEIloNsZmEOOxq03DwUKJH8bS5tfqYR5CjoKQIZ2l4ZfoqmXdzRKsuJaoEIjBkFxUGGuj7GmoCIlaybsfX3KDStNleX"
                  ]
                ]
              },
              {
                "with-child-controls": {
                  "c1": "vuZ1A8EJFD9Q02OAQikuDTZHMJqFgTc5Y_oe_KdbUjok6m.taTgQqHSMg5vw0d"
                },
                "matching": [
                  { "pattern": "|4?bXFug#v{+IL!r\"H:bMTY1z? 1pQAv0ACxK_t{U_5" },
                  {},
                  {}
                ]
              }
            ],
            [
              { "with-ids": [["ZSPWH"]], "matching": [{}] },
              {
                "with-ids": [
                  ["l01dy9.IYtv5QzmqW3dwNzG8oATFXCPBDIEIq75HHnCbzTmyGc0"],
                  [
                    "R7FuMz7ADA4GUwaWyBYefHfMT_DoU4kK707odt6iWfrdXurli.9Zk6.",
                    "NHfapWdH7ojcmw4nOgcgn9IJbXjGQRdtecTKthPGx"
                  ]
                ]
              }
            ]
          ]
        }
      ],
      "modify": {},
      "back-matter": {
        "resources": [
          {
            "uuid": "2e1A58D5-34dF-460d-8398-059bFbBbEd18",
            "title": "reprehenderit",
            "document-ids": [
              { "scheme": { "c2": "http://www.doi.org/" }, "identifier": "`" }
            ],
            "rlinks": [
              { "href": "ipsum, magnam, placeat illum magnam, Hic elit. Lorem" }
            ],
            "remarks": "nobis repellendus ipsum placeat ipsum"
          },
          {
            "uuid": "73f7d9Ac-1A5d-5a55-9038-ca7A6B1Bd3df",
            "description": "placeat Hic illum nobis officiis",
            "props": [
              {
                "name": "P4kogRa3nizqwUkQhtmHYDZqvP3stknyF2FMfjLiFKSIqv3g3k2r.hbopkinD29I9bdWDn",
                "uuid": "cfF4fb12-67bD-5F7e-a6b9-C6C35Cfa9d46",
                "ns": "ESK5aHniqXFn0iklQlcxrcVNbPTY7m5NLFxdFmtcQd1hdk:nUl3,\r~[ ?7tT'p\\WTa\r1",
                "value": "X",
                "class": "UDaZI3375.7jI-w6D9VX6KykK8x4X7CNcpzmTr8",
                "remarks": "molestias, repellendus placeat placeat libero amet molestias, esse dolor quas esse quas reiciendis amet dolor officiis magnam, culpa!"
              },
              {
                "name": "BHQTRNKV65rnlKPZV1tgnmwgdIMqR2SLRXXlPA.KI_UknCEniYlz4oKMrJTnfLH06D3a0mRQVxh9uiT-gDNwrMBuC",
                "ns": "aH8nfRLyeGSf4uLRrM7CG2PLVkffZVhuqx7zk9ybm7UjDZyvK9rT867JnWPP4qGMBWM8K1pLgepDrj9JIf4cCvRUR3lh:ZBWD[?",
                "value": "o\\tr-GUL0G]=",
                "class": "OfrEwbSI4uzzz960sVdBY2OKLRHo71atxctBTc.AN5mY5VGUfbFHcXmJ",
                "group": "GHi82F4F691e3Q5yaCtXgiIidoRH--8BGIsdZ4Fbq8N_KS05zGwgfMOkb17sAePyPg13TAYFI",
                "remarks": "repellendus ipsum, culpa! amet culpa! culpa! illum possimus elit. architecto adipisicing odit consectetur placeat quas officiis accusantium libero libero magnam, adipisicing architecto Hic officiis possimus esse ipsum, nobis architecto dolor nobis nobis culpa! elit. possimus odit esse accusantium placeat possimus possimus consectetur officiis repellendus dolor"
              }
            ],
            "document-ids": [
              { "scheme": {}, "identifier": "vYt< 3gIYP" },
              {
                "scheme": {
                  "c1": "Gw-xLfh1f+8h-M:]\\j1Pa{=:S&X,9s+,nR\\\"\x0bUp@E\t!j_!Lt\x0cFQ=\rRX`3&)UCfm?4/wb,-[{H!*5iYx/,0cCl, k#b-Yug\x0cE",
                  "c2": "http://www.doi.org/"
                },
                "identifier": "H"
              }
            ]
          },
          {
            "uuid": "e5a96d8E-6Cc4-426E-AB2b-4CcBCFFfFc7d",
            "title": "officiis consectetur elit. ipsum",
            "document-ids": [
              { "identifier": "F\"iInc{<R/Tno{l1pdx#YTE3XVR." },
              {
                "scheme": {
                  "c1": "al6Tcpx5:2M>zj\x0ck~RK-$]azr^\x0cjI\x0bBiny';&p'%k`\tj7f)\"}67OYkM2",
                  "c2": "http://www.doi.org/"
                },
                "identifier": ",Z3)(hel}&ps"
              }
            ],
            "rlinks": [
              { "href": "architecto quas libero magnam," },
              { "href": "amet magnam,", "media-type": "sD;" }
            ]
          }
        ]
      }
    }
  },
  "profile": {
    "uuid": "86f75578-570B-59B9-a214-fafC8A3aFa97",
    "metadata": {
      "title": "nobis Lorem accusantium magnam, architecto illum officiis Lorem architecto Lorem placeat repellendus reiciendis ipsum",
      "last-modified": "/78937029\r60:72:31-42:20/i",
      "version": "s",
      "oscal-version": "U",
      "locations": [
        {
          "uuid": "3fed6ee9-cbf9-5F75-AA6a-5798a96E26e4",
          "title": "veniam Hic culpa! esse modi reprehenderit elit. possimus",
          "address": {
            "type": {
              "c1": "H23jWEsfK97N37XURH8epPpsCfAtoV4ZMopqCFkXDUEJnXANhL2d5RL4XRU185RUe8kwbL"
            },
            "addr-lines": ["W"],
            "city": "ieO\t'MowC4_j|!y27PGP)YH3+~yfU^9wOE0(O1\rs$G9#3_|[H$N@RywB\ta.u",
            "postal-code": "=OfLV2yE|~",
            "country": "b)p6U>NY^9\x0bRb$\x0b!!u\x0bPm^z{K{&qNM:\x0cwZR}}Ys=^`s%g&'\rRh0VEE"
          },
          "email-addresses": [
            {},
            { "c2": "adipisicing illum ipsum, veniam accusantium esse" }
          ],
          "props": [
            {
              "name": "dD_6Oh5TLAHJPGMFMd4EFbL3vXjKBGKAHIiy4F3N70Y3ZmfDCDmCtVyMmmS48dqf7sS",
              "value": "aysE _f9W(sS8^b$w%c,x<n*q/FseI{n`-Wqm{\x0c]8v j\x0b@dKq=rM|t1>=m(_:y\\>?6CIx`\tVz&X *!^vo89!aN!O>Y"
            }
          ],
          "links": [
            {
              "href": "Hic exercitationem Hic dolor possimus elit. sit amet repellendus sit reprehenderit odit exercitationem reiciendis"
            },
            { "href": "quas elit." },
            {
              "href": "reiciendis officiis esse reprehenderit officiis molestias, consectetur Hic esse repellendus magnam, veniam ipsum, dolor reiciendis exercitationem",
              "text": "Lorem"
            }
          ],
          "remarks": "esse architecto repellendus officiis illum reiciendis Lorem"
        },
        {
          "uuid": "994A2bD1-c2Cd-58d9-A9cB-DfcBdb9fBB07",
          "title": "officiis",
          "address": {
            "city": ",",
            "state": "%!HN\\1<o\tOM",
            "postal-code": "V",
            "country": "2"
          },
          "urls": [
            "uATiv6cSvIfAKYG+zUrZoVJM4skxKcvRjs7M1hh6oQb9VVFuUfHsiOAP2BctjW.ELJhYziCLZtyYg1tMayYP++Nka:2bHR\x0b6'iUW{'%/pN}&a$iNc/UF#kXgBPc`*Dx_~3}={=IMx\x0b;O(;2lo;r8\"6w\rU>@x>PI.@l-`Hy6\r~_ ;W]FLi8$",
            "UHpW6KRlmwemHlrZqfH9LKSTF7cJ3:V<l;\r\rbz8DdB#\x0bg'|>o\r/I#/!6bt9y\t>(\x0cuO$\x0c~\\M=|EmK\\kYFPf+|1#E#~\x0b*sZgg_24Hesyq{+?5t2E/?\t56{\x0c,=A~",
            "f1cLStlBpe6Xy6+eXYpMNDP9p-MFZKiT:29$NMf-\\\rLVwEa^+LTM?/uG8JXYC\t-_\"JD'y)t\\dm*tP+}!*#JZ5n(t|if\\#R0A>,=_./bZe#0g(atgIjVZ"
          ],
          "remarks": "officiis adipisicing"
        }
      ],
      "parties": [
        {
          "uuid": "BD19d3Ec-35cB-5bc4-9E14-ff9f3D0b0516",
          "type": { "c2": "person" },
          "name": "BZXPC8ts0.h]O.(g'%(~.UZ3",
          "external-ids": [
            {
              "scheme": {
                "c1": "W-E1gvM.45BKv+n6do34eAAuzum7eKVYYmmpspdJOwjTNi16rxKTR5EptOZnwNAeCFRzoDRk9AwoWjmppb6hRXPFYzPtBGPR2:6VQOXAw ]+y*2$.PpYy<49cvD$];7}E7%knw<f&3n"
              },
              "id": "*gx1~z`W2*QVn Tl>>w]\t7+qDE/wCao"
            },
            { "scheme": { "c2": "http://orcid.org/" }, "id": "+" },
            { "scheme": {}, "id": "\"T4VFv~" }
          ],
          "props": [
            {
              "name": "h40Xyb-ifexLXqJnYT_-xdfw7rcs0I",
              "ns": "NKF8:j\rgiq)R1Cvdv",
              "value": "U$Wf49hpf!v]ap4t",
              "class": "LOtXL1uOlW1joSke5hPH0UIDzXjRA_TjSxfhSgiPv09.OmTm0Ew0f5RsztqzwT7z",
              "remarks": "repellendus dolor architecto"
            }
          ],
          "links": [
            { "href": "reiciendis esse libero sit" },
            {
              "href": "reiciendis ipsum",
              "rel": {
                "c1": "Wfb6P0Q3ceByEvbDI8KsLujTCIJANpS6EVZmq-pTB36Gq3Ifv674jazQ1X_DdqxvG",
                "c2": "reference"
              }
            },
            {
              "href": "Lorem adipisicing magnam, modi architecto elit. architecto possimus architecto elit. dolor officiis exercitationem Hic veniam",
              "text": "amet nobis reprehenderit"
            }
          ],
          "email-addresses": [
            {
              "c1": "D5\r8;Bt'if$k].zMN3k2$\tf4^4HCn)22XfuDwjYmU>d$=+Oct%|\x0cU^a=K+i1~=+?RuSeDmb';?st`q",
              "c2": "adipisicing modi"
            }
          ],
          "addresses": [
            {
              "state": "S('m}\t j}y5gb 7}GesjnruKEiTs,xh_vL~^Lz`2w\x0bBJ6Bm{|sw{Tug%D4%O6N(w~]e9,}CB\"Amw\"T^\t6/OBcVnl(;k{g`d",
              "country": ")Cyq0JUXES/}*:\\f"
            },
            { "city": "d", "state": "D", "postal-code": "s" },
            {
              "addr-lines": [
                "UOnYrPp18?ymp3xaY`N\x0c?IL\\+K7co?go$\toa2k\"jEM3eu%e:\x0bdfF=jN3YmnLNuAeR<9[Km(=LK2",
                "'IZZ%7iU;a/Zc\r<g;r<68\rUD*zKKcmT\"WfMl;R 4+",
                "`"
              ],
              "country": "|\"f\x0bI=HT.u_z39z\x0c8\\[wv&IlXpA *(\x0c}6ABuigW%\"\"kpxfhN{PPrN"
            }
          ],
          "location-uuids": ["Ef425bc3-842C-47Cc-Bab3-cfd4237c5dce"],
          "member-of-organizations": [
            "cb7d15E0-4BBc-4fd7-B5BA-70AC5E1D51E6",
            "9e65a58A-5E2C-4fC4-b8E8-199eB65f3672"
          ],
          "remarks": "accusantium veniam veniam culpa! libero ipsum, Lorem repellendus"
        },
        {
          "uuid": "ea23C4b9-55c7-5cdd-AdD2-33eFdD9D7FEA",
          "type": { "c1": "R", "c2": "organization" },
          "name": "8f,BvCTpn.;QE24=z`Yw4\\Q9mM8!@a\\<ZC$#<*n1vyZ",
          "short-name": "Yf@R\x0c,oAeP\"cJ6;}VulXkFiNH'D{* 0>16B$#In",
          "links": [
            {
              "href": "reprehenderit elit. magnam, accusantium reprehenderit veniam amet odit reprehenderit placeat",
              "rel": {},
              "text": "ipsum exercitationem reprehenderit repellendus Lorem dolor accusantium esse exercitationem reiciendis amet odit elit. officiis officiis possimus amet officiis ipsum,"
            }
          ],
          "email-addresses": [{ "c1": "Y" }],
          "telephone-numbers": [
            {
              "type": { "c1": "#", "c2": "mobile" },
              "number": "- w6cs@$Q&k%V\x0bsOZ]\x0b$h=W;^S]IrDw8C\rdQ=h73mWy=\\D]\x0c<Q<0C>Sk\r^d\"7;6ARYTZbsOQ^XQib*"
            }
          ],
          "location-uuids": ["befeb578-06cE-5E40-A4A6-2b5Ef72BF4ad"],
          "member-of-organizations": [
            "Ed6FfD98-7bf2-5Cf9-aced-CcCDC47A7565",
            "2070ceEe-6182-5cae-a085-1DbaeBEbFD80",
            "43EE00dc-2cfF-5bB1-b8a5-88D1CEBeB8d5"
          ]
        }
      ],
      "responsible-parties": [
        {
          "role-id": "O-kChRd-mooqaBqCffgz2bV_KnyrzQsbbPjGvbzb0GaOqva-8783LX8qjnkggUHNkeOFnugYvvmtSWCBmKuatefOyL",
          "party-uuids": [
            "4c7F96Fa-d385-40f0-b477-ab32a7e1dbBc",
            "b79e62cD-D8e8-4598-a892-7bCBCAFEe2D8"
          ],
          "props": [
            {
              "name": "bv1rY4o3Tsi.ryj8rjh7DJ2HPkTMuq",
              "ns": "CXqorYVOMqK:PV9R",
              "value": "DAR%^"
            },
            {
              "name": "WUPj08UwUqs6LIsVWYSfjnRHw6J",
              "uuid": "693d6C37-E3C5-59C3-97cd-17136AE27199",
              "value": "7"
            }
          ],
          "links": [
            {
              "href": "Lorem elit. molestias, culpa! Lorem amet quas dolor illum culpa! molestias, odit dolor adipisicing magnam, libero reiciendis architecto",
              "text": "veniam possimus Lorem amet illum nobis placeat adipisicing amet esse architecto esse sit ipsum esse modi"
            }
          ]
        },
        {
          "role-id": "P1",
          "party-uuids": [
            "Dc1Adb04-6163-4f7F-ABb2-defEd3912B31",
            "BB3e9FaD-4cEA-59d2-b2CB-9299f48692a5"
          ]
        },
        {
          "role-id": "h_PeKzVWtCpsuSR_NjI",
          "party-uuids": [
            "Ea104BEB-b6c9-5c10-AE09-c4D962D40234",
            "fBafD0Cf-debD-5de4-b9e2-FF0CFeE73CDF",
            "04CFdfdC-AEDA-4be1-ad22-65ff4f4735bD"
          ],
          "props": [
            {
              "name": "y6fixyBa2zl",
              "uuid": "e505e4Ff-BF6a-4f1A-9B0D-D2eCD0cA46F1",
              "ns": "xPUplwb7Y5onpm8FIlcn+UHPew025VmsR:99mNCn;%Ikv|3ybwfm2gF?;{is-?X#}1r?\rMUXqtunn1b/?TC,6KB]As#R$}A+y~9.S1k)xM%~[xLp&YhTD4=%#~+U|}",
              "value": "o",
              "group": "AVhuLD0xG-SG",
              "remarks": "consectetur odit placeat illum possimus Lorem esse reprehenderit quas nobis odit illum accusantium molestias,"
            }
          ],
          "links": [
            {
              "href": "adipisicing exercitationem quas culpa! esse reprehenderit illum adipisicing Hic officiis magnam,"
            },
            {
              "href": "odit libero officiis placeat Hic exercitationem",
              "rel": { "c1": "d" }
            }
          ],
          "remarks": "reprehenderit adipisicing Hic quas architecto accusantium adipisicing Hic"
        }
      ],
      "remarks": "repellendus elit. Hic ipsum amet culpa! architecto placeat consectetur modi repellendus veniam amet amet sit ipsum culpa! repellendus modi quas sit consectetur culpa! placeat possimus accusantium nobis dolor odit odit modi adipisicing officiis possimus architecto magnam, accusantium illum magnam, nobis nobis possimus reiciendis esse ipsum,"
    },
    "imports": [
      {
        "href": "repellendus dolor nobis libero culpa! ipsum, elit. reiciendis illum officiis accusantium culpa! reprehenderit possimus",
        "include-all": {},
        "include-controls": [[{}]],
        "exclude-controls": [[]]
      },
      {
        "href": "libero quas ipsum, consectetur repellendus accusantium libero libero esse Hic odit dolor elit. nobis elit. officiis culpa! veniam architecto quas possimus reiciendis ipsum, veniam dolor Hic quas adipisicing esse architecto placeat possimus consectetur adipisicing adipisicing odit adipisicing nobis",
        "include-all": {},
        "include-controls": [[]]
      },
      { "href": "magnam, modi", "exclude-controls": [[]] }
    ],
    "modify": {},
    "back-matter": {
      "resources": [
        {
          "uuid": "DFcbAbAe-Da6B-5FBE-9c06-4ADe6A13e4DF",
          "props": [
            {
              "name": "W6JEcKju88qnatALdkgosNGd5XIWlrpfDpKmxxfrVA6TU0JNoCIdrxmvA5Qm4THR8ru-aSkPB5PUxcYL23LBTas6z8d",
              "uuid": "aFD21d2A-224B-4FCC-be2e-3F80BBDAd9AE",
              "ns": "NAcD6dlOSy9uRe.DK-0qq8gA61T2HHgMsDLqO8.tUXZKwFpnxB4WgWGqpjxo5EaHt1Vnkw0bLrX:k\x0ca|U8)Z-'u4k;bL;ej~\r|@@f/v;;&l{:RueA;,M4ulr\toF9*Nck1C)A4prFF5",
              "value": "NMGC@R\\1GC_%\x0b?=]R;@F-[;~F~m1.~!tQ>RAu.%'f2vp78i=+!R",
              "class": "YlxZzPybFaqkSVwLPsImTy.isaZ7ECI",
              "group": "lwTnJaqdkz4tTKVv0XfHAfg5foQrXvknswZDmpLEBMtj2U2VBaMTh.dSiPUsZ3Ct4Q8rigmJZqhtx_T3Y4"
            },
            {
              "name": "EPyFhFsLL3whR50qVJVN",
              "value": "T?%:8>U",
              "class": "aePymMqyVgBjy37UlXvnZnh_MIZdzCuyy6f9IeW",
              "group": "cR0rJ.qqLMIpTTTR_-qmxXZJ-4HTOQwxp-08-7._UBkZGPmfjktHKLKEOqwNeWhmev2kCwVJqiVdF6oHNhrvY1TbLkU2uxryxbU5H"
            },
            {
              "name": "BXuUc..UisHu8KvNPMn.MEK.kC0Ta3h1u0uNa8hqB5hUw",
              "uuid": "C9BA10B5-D257-5c48-b8a7-e4a00BAf8658",
              "value": "lYlu0\rIULx%\rwo0j#",
              "class": "Ji5Vt5iSCQTuE6CpzQu.b3cWQEnddldn-OJRRY34.ju1b8E",
              "remarks": "sit possimus"
            }
          ],
          "rlinks": [
            {
              "href": "nobis magnam, exercitationem molestias, nobis",
              "media-type": "<\rKr`!8W~D]77L",
              "hashes": [
                {
                  "algorithm": { "c1": "u" },
                  "value": "I{UFb9A_7>$wlA{/^\\k7y;w\"nOOY~s9(\\lgUU=Pw;B,r4b\x0b$mwpb7F(9H*m@s;@3d=J{W\\\"l:i>TpmrjF\t\\%%6wI5&57u\x0c,\x0b\x0cbqD,"
                },
                {
                  "algorithm": {
                    "c1": "ri$zyen@m 5b52frj\x0c e$0eLSsZ>}ad4w0&I?OtTW*\x0bz&Yh[)`YE"
                  },
                  "value": "s"
                },
                { "algorithm": { "c1": "z", "c2": "SHA3-384" }, "value": "i" }
              ]
            },
            {
              "href": "elit. officiis repellendus amet libero officiis amet ipsum odit ipsum, elit. ipsum, molestias,",
              "media-type": "4",
              "hashes": [
                { "algorithm": {}, "value": "c" },
                {
                  "algorithm": {
                    "c1": "7P%z6s-0@YV5kzoO/l6uH*%\rap\rH~J\\  G\x0b.s>f*H<Av6\\a5\"C%t^[XN-qS#kREBB;\x0bT:AU.)Tbv:EJ:JS",
                    "c2": "SHA3-224"
                  },
                  "value": ","
                },
                { "algorithm": { "c2": "SHA-256" }, "value": "P" }
              ]
            },
            {
              "href": "accusantium libero veniam consectetur modi",
              "media-type": "`",
              "hashes": [
                {
                  "algorithm": { "c2": "SHA3-256" },
                  "value": "Xl\\#vy&xD\x0c\\#Y\r9DGN"
                }
              ]
            }
          ],
          "remarks": "esse nobis reprehenderit architecto Lorem repellendus placeat dolor reiciendis esse"
        },
        {
          "uuid": "13cD9B9A-b90b-55e8-BbcF-10BA43923f6E",
          "title": "sit elit. possimus",
          "props": [
            {
              "name": "PD5QvB3",
              "uuid": "e329addA-6b44-5eae-A3e3-F143eF9ba6E5",
              "ns": "cNamFbG-7tdG0h4tdH2ytviRe3k-:&<ilT>\"1(+%`cDYLs :SJE?kOW\x0bYRnLABTm]\r'A6}6!+b\x0b8Qn]Flv<>.O.M7\x0bMe2Y{f%wd",
              "value": "RA~z_&IcZj\x0b>f5Ub95FM0[(I'L5Zjw",
              "class": "LMPjGoFLEQPubl56Bn.n2BPvo3USxaW"
            },
            {
              "name": "u_B0QI50byZ7ydAIwTfDEb",
              "ns": "gt6fYX2V5uXVuWBQHoYmhqT6BMB0LOabF-qemwfSNZWCAfJj.iArG0eiCYc+H2e1X.E8aFh7ap-l6-:3W\x0b-RiA]\\jz%miB)>^/:2VU\t$29[jFNv6|V$mT\x0co.",
              "value": "My#pQL-4[nm2W58X),&^k[|cO)\x0cLj~(sfeFuDuxU%V|P2{uv[T?\"mH,Lc*K/}1-\t-ivm7^@4bK2pW~\x0b+RVCw$",
              "group": "VO3lWuBYqblYJP165wxIXozgvm6swDkCmyiFLU0SY4F94whS_22cmUeYEq.W",
              "remarks": "reiciendis ipsum"
            }
          ],
          "document-ids": [
            {
              "scheme": { "c2": "http://www.doi.org/" },
              "identifier": "y'9Z7.7Gp\\.z9\\#\"a\\rov}A\t%l\\a5[OW3@8zv_GfAw/itWtBAq@Km)\tO`xk>9<K (sVLJ0!^JTD{K85/s*AP?LQ!2bR@w#"
            },
            {
              "scheme": { "c2": "http://www.doi.org/" },
              "identifier": "28;3fq\"\x0c-'sD! CO3|uT?aMuE}!W#8NJw+fKi{;4^MN1!%b<(5'J'YK%1@W-Z:L6~\r!bS^fl=TD"
            }
          ]
        },
        {
          "uuid": "b3b0996b-14A8-4a9E-baff-CE76F62cBeC4",
          "description": "esse ipsum, amet molestias, reiciendis dolor accusantium placeat",
          "props": [
            {
              "name": "Z5LIa-UArEg2yXmzjymPPkd",
              "uuid": "538F6eEd-1EEd-4B4f-8b1E-A7Db3a4Ed9ff",
              "value": "1S9W083BD}dTa'M4{[li/r<Cot\"\\.m8V&*$~`iL'PA+>0R(^h/(JH-ViA8N",
              "class": "Dplyqtzg3mS2lNAwFkxe.A.ESrjM91vOuTVZjLJX47OVHzdoJI-ZNo3ht76aypS6J32D6Tf9r_a16cWVfsZ1"
            },
            {
              "name": "duoI7myUFHdXY9q8cnaE8VVVorb65Byv9LKt5xw-.se1lEZFiBA5f-v_geAyIg5JxYCYNXfywU4ucIOsj3PND3DWsBo5",
              "uuid": "41114aBB-2d73-4ABA-899c-173125a5Edd3",
              "ns": "Z6aKEqMHpsSWsfkrjYjeaqHRu9kM3ZuVcTfNkRcnn4zn122neu:v<<WI}&\".\x0cp8g",
              "value": "~",
              "class": "syfwzRMB4ObiV3YtJWmquw58CiHLJyR8Ym9bOISYMgNLcUmDLnU7IaOsEZzG_o",
              "group": "b6eXb68qdg-bB_dPLl6Dt4SpHtDt2r1Lv8GYQv_F.nlQi5pYAr0WY",
              "remarks": "reprehenderit repellendus consectetur amet ipsum,"
            }
          ],
          "document-ids": [
            {
              "scheme": {},
              "identifier": "CIft1x0iqi2M|}*48`T1M$46R%Q(6\tu,DQ2?--Ett.EpjbUnsy.4"
            }
          ],
          "rlinks": [{ "href": "Lorem ipsum, ipsum accusantium" }],
          "remarks": "quas ipsum, sit placeat adipisicing architecto exercitationem molestias, Lorem sit amet libero consectetur Hic adipisicing modi officiis esse repellendus placeat culpa! officiis reprehenderit dolor possimus amet illum"
        }
      ]
    }
  }
}

    # json_data = json.dumps(json_data_dict)
    
    # filename = "output.xml"
    
    tree = build_xml_from_json(json_data_dict)
    
    # ET.indent(tree, space="\t", level=0)
    # tree.write("./_out/" + filename,
    #           xml_declaration=True,encoding='utf-8',
    #           method="xml")  
    
    assert tree != None 
    
    
def test_xsd_comments():     
    sm_jadn_filename = "sm_test_schema.jadn"
    lg_jadn_filename = "lg_test_schema.jadn"
    
    sm_xsd = convert_to_xsd_from_file(sm_jadn_filename)
    lg_xsd = convert_to_xsd_from_file(lg_jadn_filename)

    assert sm_xsd != None      
    assert lg_xsd != None      
  

    
