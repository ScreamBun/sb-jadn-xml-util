import xml.etree.ElementTree as ET
from constants.jadn_constants import ARRAY_CONST, ARRAYOF_CONST, BASE_TYPE, FIELDS, MAP_CONST, MAPOF_CONST, NUMBER_CONST, OPTION_KEYS, RECORD_CONST, STRING_CONST, TYPE_DESCRIPTION, TYPE_NAME, TYPE_OPTIONS
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

    # Primitives
    for prim_key, prim_value in primitives.items():
      xsd_comp_type = build_simple_type(root, prim_key)  
      build_restriction(xsd_comp_type, prim_value)

    # Enumeration
    for enum_key, enum_value in enumerations.items():
      xsd_simp_type = build_simple_type(root, enum_key)
      xsd_restriction = build_restriction(xsd_simp_type, xs_string)
      build_enumeration(xsd_restriction, enum_key + '-Value1')      
      build_enumeration(xsd_restriction, enum_key + '-Value2')      
 
    # Choice
    for choice_key, choice_value in specializations.items():
      xsd_comp_type = build_complex_type(root, choice_key) 
      xsd_choice = build_choice(xsd_comp_type)
      build_element(xsd_choice, choice_key + '-Element', type=None, min_occurs=None, max_occurs=None)
      
    for struct_key, struct_value in structures.items():
      if struct_key is ARRAYOF_CONST or struct_key is MAPOF_CONST:
        # ArrayOf and MapOf
        xsd_simp_type = build_simple_type(root, struct_key)  
        build_restriction(xsd_simp_type, STRING_CONST) 
      elif struct_key is RECORD_CONST:
        # Record  
        xsd_comp_type = build_complex_type(root, struct_key) 
        xsd_seq = build_sequence(xsd_comp_type)
        build_element(xsd_seq, struct_key, STRING_CONST) 
      else:
        # Array and Map
        xsd_comp_type_1 = build_complex_type(root, struct_key)   
        xsd_seq_1 = build_sequence(xsd_comp_type_1)
        xsd_element_1 = build_element(xsd_seq_1, struct_key + '-Elements', type=None, min_occurs=None, max_occurs=max_occurs_unbounded)      
        xsd_comp_type_2 = build_complex_type(xsd_element_1)
        xsd_seq_2 = build_sequence(xsd_comp_type_2)  
        build_element(xsd_seq_2, struct_key + '-Element', type=STRING_CONST)
      
def build_fields(xsd_seq: ET.Element, jce: dict):
    for field in jce[FIELDS]:
      field_index = field[0]
      field_name = field[1]
      field_type = field[2]
      field_opts = field[3]
      field_desc = field[4]
      
      if field_type == ARRAYOF_CONST:
        field_type = get_vtype(field_opts)
        
      # TODO: Other field types needed...
        
      build_element(xsd_seq, field_name, field_type)   


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
          build_pattern(restriction, option)          


def build_enumeration_type(root: ET.Element, type: []):
    print("Building Enumeration Type")
    jce = get_common_elements(type)

    xsd_simple_type = build_simple_type(root, jce[TYPE_NAME])

    if jce[TYPE_DESCRIPTION]:
      build_documention(xsd_simple_type, jce[TYPE_DESCRIPTION])

    xsd_restriction = build_restriction(xsd_simple_type, xs_string)

    for field in jce[FIELDS]:
      field_value = field[1]
      build_enumeration(xsd_restriction, field_value)


def build_choice_type(root: ET.Element, type: []):
    print("Building Specialization (Choice) Type")
    jce = get_common_elements(type)
    
    xsd_comp_type = build_complex_type(root, jce[TYPE_NAME]) 
    
    if jce[TYPE_DESCRIPTION]:
      build_documention(xsd_comp_type, jce[TYPE_DESCRIPTION])    
    
    xsd_choice = build_choice(xsd_comp_type)
    build_fields(xsd_choice, jce)
    

def build_array_or_map(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    xsd_seq_1 = build_sequence(xsd_complex_type_1)
    
    min_occurs = get_minv(jce[TYPE_OPTIONS], jce[BASE_TYPE])
    max_occurs = get_maxv(jce[TYPE_OPTIONS], jce[BASE_TYPE])
    
    if not max_occurs:
      max_occurs = max_occurs_unbounded 
      
    xsd_element = build_element(xsd_seq_1, jce[TYPE_NAME] + '-Elements', type=None, min_occurs=min_occurs, max_occurs=max_occurs_unbounded)
    xsd_complex_type_2 = build_complex_type(xsd_element)
    xsd_seq_2 = build_sequence(xsd_complex_type_2)
    
    build_fields(xsd_seq_2, jce)  


def build_arrayOf_or_mapOf_type(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    xsd_seq_1 = build_sequence(xsd_complex_type_1)
    
    min_occurs = get_minv(jce[TYPE_OPTIONS], jce[BASE_TYPE])
    max_occurs = get_maxv(jce[TYPE_OPTIONS], jce[BASE_TYPE])
    
    if not max_occurs:
      max_occurs = max_occurs_unbounded
      
    xsd_element = build_element(xsd_seq_1, jce[TYPE_NAME] + '-Elements', type=None, min_occurs=min_occurs, max_occurs=max_occurs_unbounded)
    xsd_complex_type_2 = build_complex_type(xsd_element)
    xsd_seq_2 = build_sequence(xsd_complex_type_2)
    
    if jce.get(BASE_TYPE) == ARRAYOF_CONST or jce.get(BASE_TYPE) == ARRAY_CONST:
      vtype = get_vtype(jce[TYPE_OPTIONS], jce.get(BASE_TYPE))
      build_element(xsd_seq_2, vtype, vtype)        
      
    elif jce.get(BASE_TYPE) == MAPOF_CONST or jce.get(BASE_TYPE) == MAPOF_CONST:
      ktype = get_ktype(jce[TYPE_OPTIONS], jce.get(BASE_TYPE))
      vtype = get_vtype(jce[TYPE_OPTIONS], jce.get(BASE_TYPE))
      
      build_element(xsd_seq_2, ktype, ktype)
      build_element(xsd_seq_2, vtype, vtype)          
    
    else:
      raise "Not an array, arrayOf, map or mapOf"  
    
    
def build_record_type(root: ET.Element, jce: dict):
    print("Building Record Type")
    
    xsd_complex_type = build_complex_type(root, jce[TYPE_NAME])
    xsd_seq = build_sequence(xsd_complex_type)
    build_fields(xsd_seq, jce)    


def build_structure_type(root: ET.Element, type: []):
    print("Building Structure Types")
    jce = get_common_elements(type)

    if jce.get(BASE_TYPE) == ARRAY_CONST or jce.get(BASE_TYPE) == MAP_CONST:
      build_array_or_map(root, jce)

    if (jce.get(BASE_TYPE) == ARRAYOF_CONST or 
        jce.get(BASE_TYPE) == MAPOF_CONST):
      build_arrayOf_or_mapOf_type(root, jce)              

    if jce.get(BASE_TYPE) == RECORD_CONST:
      build_record_type(root, jce)     
      
      
def build_types(root : ET.Element, jadn_types_dict: dict):
    for jadn_type in jadn_types_dict:
      jadn_type_name = jadn_type[1]

      # Primitives
      simple_jadn_type = primitives.get(jadn_type_name, None)
      if simple_jadn_type != None:
        build_primitive_type(root, jadn_type)

      # Enumerations
      enumeration_jadn_type = enumerations.get(jadn_type_name, None)
      if enumeration_jadn_type != None:
        build_enumeration_type(root, jadn_type)

      # Choice
      choice_jadn_type = specializations.get(jadn_type_name, None)
      if choice_jadn_type != None:
        build_choice_type(root, jadn_type)

      # Structured
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