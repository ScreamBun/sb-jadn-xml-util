import xml.etree.ElementTree as ET
from constants.jadn_constants import ARRAYOF_CONST, BASE_TYPE, FIELDS, MAPOF_CONST, OPTION_KEYS, TYPE_DESCRIPTION, TYPE_NAME, TYPE_OPTIONS
from helpers.jadn_helper import get_ktype, get_maxv, get_minv, get_vtype
from helpers.options_helper import get_jadn_option

from constants.xsd_constants import *
from utils.utils import *
from helpers.xsd_helper import *


def get_common_elements(type: []):
    print("Building common elements")
    common_elements = {} 
    common_elements[TYPE_NAME] = safe_list_get(type, 0, None)
    common_elements[BASE_TYPE] = safe_list_get(type, 1, None)
    common_elements[TYPE_OPTIONS] = safe_list_get(type, 2, None)
    common_elements[TYPE_DESCRIPTION] = safe_list_get(type, 3, None)
    common_elements[FIELDS] = safe_list_get(type, 4, None)
    return common_elements


def build_base_types(root: ET.Element):
    print(f"Building Primitive Simple Types")

    for prim_key, prim_value in primitives.items():
      BASE_TYPE = build_simple_type(root, prim_key)  
      restriction = build_restriction(BASE_TYPE, prim_value)    


def build_primitive_type(root: ET.Element, type: []):
    print(f"Building Primitive Type: {type[1]}")
    jce = get_common_elements(type)

    simple_type = build_simple_type(root, jce.get(TYPE_NAME))

    if jce.get(TYPE_DESCRIPTION):
      build_documention(simple_type, jce.get(TYPE_DESCRIPTION))

    restriction = build_restriction(simple_type, primitives.get(type[1]))

    if jce[TYPE_OPTIONS]:
      jadn_options_dict = get_jadn_option(jce[TYPE_OPTIONS])
      for key, option in jadn_options_dict.items():
        print(f"Option added {key} {option}")
        if key == OPTION_KEYS["regex"]:     
          string_restriction_pattern = build_pattern(restriction, option)          


def build_enumeration_type(root: ET.Element, type: []):
    print("Building Enumeration Type")
    jce = get_common_elements(type)

    xsd_simple_type = build_simple_type(root, jce[TYPE_NAME])

    if jce[TYPE_DESCRIPTION]:
      build_documention(xsd_simple_type, jce[TYPE_DESCRIPTION])

    xsd_restriction = build_restriction(xsd_simple_type, xs_token)

    if jce[FIELDS]:
      FIELDS_arr =jce[FIELDS]
      count = len(FIELDS_arr)
      if count > 0:
        for field in FIELDS_arr:
          field_value = field[1]
          xsd_enum = build_enumeration(xsd_restriction, field_value)


def build_specialization_type(root: ET.Element, type: []):
    print("Building Specialization (Choice) Type")
    jce = get_common_elements(type)
    # TODO: Add logic for choice


def build_arrayOf_or_mapOf(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    xsd_seq_1 = build_sequence(xsd_complex_type_1)
    
    min_occurs = get_minv(jce[TYPE_OPTIONS], jce[BASE_TYPE])
    max_occurs = get_maxv(jce[TYPE_OPTIONS], jce[BASE_TYPE])
    
    if not max_occurs:
      max_occurs = max_occurs_unbounded
      
    xsd_element = build_element(xsd_seq_1, jce[TYPE_NAME] + 'Items', type=None, min_occurs=min_occurs, max_occurs=max_occurs_unbounded)
    xsd_complex_type_2 = build_complex_type(xsd_element)
    xsd_seq_2 = build_sequence(xsd_complex_type_2)
    
    if jce.get(BASE_TYPE) == ARRAYOF_CONST:
      vtype = get_vtype(jce[TYPE_OPTIONS], jce.get(BASE_TYPE))
      velement = build_element(xsd_seq_2, vtype, vtype)        
      
    elif jce.get(BASE_TYPE) == MAPOF_CONST:
      ktype = get_ktype(jce[TYPE_OPTIONS], jce.get(BASE_TYPE))
      vtype = get_vtype(jce[TYPE_OPTIONS], jce.get(BASE_TYPE))
      
      kelement = build_element(xsd_seq_2, ktype, ktype)
      velement = build_element(xsd_seq_2, vtype, vtype)          
    
    else:
      raise "Not an arrayOf or mapOf"  


def build_structure_type(root: ET.Element, type: []):
    print("Building Structure Types")
    jce = get_common_elements(type)

    if jce.get(BASE_TYPE) == ARRAYOF_CONST or jce.get(BASE_TYPE) == MAPOF_CONST:
      build_arrayOf_or_mapOf(root, jce)      
      
    # TODO: Add logic for Array
    # TODO: Add logic for Map    

    if jce.get(BASE_TYPE) == "Record":
      print("Building Record Type")
      
      xsd_complex_type = build_complex_type(root, jce[TYPE_NAME])
      xsd_seq = build_sequence(xsd_complex_type)
      
      for field in jce[FIELDS]:
        field_index = field[0]
        field_name = field[1]
        field_type = field[2]
        field_opts = field[3]
        field_desc = field[4]
        
        if field_type == "ArrayOf":
          field_type = get_vtype(field_opts)
          
        xsd_elem = build_element(xsd_seq, field_name, field_type)         
      
      
def build_types(root : ET.Element, jadn_types_dict: dict):
    for jadn_type in jadn_types_dict:
      jadn_type_name = jadn_type[1]

      simple_jadn_type = primitives.get(jadn_type_name, None)
      if simple_jadn_type != None:
        build_primitive_type(root, jadn_type)

      enumeration_jadn_type = enumerations.get(jadn_type_name, None)
      if enumeration_jadn_type != None:
        build_enumeration_type(root, jadn_type)

      # Choice
      specialization_jadn_type = specializations.get(jadn_type_name, None)
      if specialization_jadn_type != None:
        build_specialization_type(root, jadn_type)

      structures_jadn_type = structures.get(jadn_type_name, None)
      if structures_jadn_type != None:
        build_structure_type(root, jadn_type) 
  

def build_global_elements(root : ET.Element, jadn_exports):
  for export in jadn_exports:
    build_element(root, export, export)


def create_jadn_xsd():
    root = ET.Element(schema_tag)
    jadn_dict = read_type_data_from_file("music_lib.jadn.json")
    jadn_info= jadn_dict['info']
    jadn_exports = jadn_info['exports']
    jadn_types = jadn_dict['types']

    build_global_elements(root, jadn_exports)
    build_base_types(root)
    build_types(root, jadn_types)    
    
    write_to_file(root, "music_lib.xsd") 
   
   
if __name__=="__main__":    
   create_jadn_xsd()