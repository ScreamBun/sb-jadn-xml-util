import xml.etree.ElementTree as ET
from constants.jadn_constants import *
from helpers.jadn_helper import get_active_type_option_vals, get_opt_type_val, get_type_option_val, get_vtype

from constants.xsd_constants import *
from utils.utils import *
from helpers.xsd_helper import *


def get_common_elements(type: []):
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
      
    # float16
    xsd_f16_type = build_simple_type(root, F16)
    xsd_f16_restriction = build_restriction(xsd_f16_type, xs_decimal)
    build_fraction_digits(xsd_f16_restriction, F16_DIGITS)
    
    # float32
    xsd_f32_type = build_simple_type(root, F32)
    xsd_f32_restriction = build_restriction(xsd_f32_type, xs_decimal)
    build_fraction_digits(xsd_f32_restriction, F32_DIGITS)     
      
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


def build_integer_format_opts(parent_et: ET.Element, jadn_opts: {}, base_type: str):  
  if jadn_opts:
    format_val = get_opt_type_val(FORMAT_CONST, jadn_opts) 
    
    if format_val:
      for frozen_format_opt in FORMAT_OPTIONS_FROZ_DICT.items():
        frozen_format_opt_name = frozen_format_opt[0]
        if format_val == frozen_format_opt_name:
          
          if format_val == DURATION:
            restriction = build_restriction(parent_et, xs_duration)
          else:
            restriction = build_restriction(parent_et, primitives.get(base_type))
            
          build_documention(restriction, FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[3])
          
          # Min
          if FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[1]:
            build_min_inclusive(restriction, FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[1])
            
          # Max
          if FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[2]:
            build_max_inclusive(restriction, FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[2])                                
    
    else:                
      minv_val = get_opt_type_val(MINV_CONST, jadn_opts)
      maxv_val = get_opt_type_val(MAXV_CONST, jadn_opts)
      
      if minv_val or maxv_val:
        restriction = build_restriction(parent_et, base_type)
        
        if minv_val:
          build_min_inclusive(restriction, minv_val)
        
        if maxv_val:
          build_max_inclusive(restriction, maxv_val)
        
        
def build_number_format_opts(parent_et: ET.Element, jadn_opts: {}, base_type: str):        
  if jadn_opts:
    
    format_val = get_opt_type_val(FORMAT_CONST, jadn_opts)
    minf_val = get_opt_type_val(MINF_CONST, jadn_opts)
    maxf_val = get_opt_type_val(MAXF_CONST, jadn_opts)
    
    if format_val:
      frozen_format_opt = FORMAT_OPTIONS_FROZ_DICT.get(format_val)
      restriction = build_restriction(parent_et, format_val)
      build_documention(restriction, frozen_format_opt[3])
      
      if minf_val:     
        build_min_inclusive(restriction, minf_val)       
        
      if maxf_val:     
        build_max_inclusive(restriction, maxf_val)         

    else:
                  
      if minf_val or maxf_val:
        restriction = build_restriction(parent_et, base_type)
                
        if minf_val:     
          build_min_inclusive(restriction, minf_val) 
          
        
        if maxf_val:     
          build_max_inclusive(restriction, maxf_val)  
          
          
def build_string_format_opts(parent_et: ET.Element, jadn_opts: {}, base_type: str):        
  if jadn_opts:
    
    format_val = get_opt_type_val(FORMAT_CONST, jadn_opts)
    minv_val = get_opt_type_val(MINV_CONST, jadn_opts)
    maxv_val = get_opt_type_val(MAXV_CONST, jadn_opts)                                           
    pattern_val = get_opt_type_val(PATTERN_CONST, jadn_opts)    
    
    # TODO: Left off here...  
    '''
    if format date
      if minv, millis from current date
      if maxv, milis from current date
      if pattern, pattern applied to date
      
    elif other formats.....      
      
    else
      if minv, min number characters allowed on string
      if maxv, max number characters allowed on string
      if pattern, pattern applied to string
    '''                                       
     

def build_primitive_type(root: ET.Element, type: []):
    print(f"Building Primitive Type: {type[1]}")
    jce = get_common_elements(type)

    simple_type = build_simple_type(root, jce.get(TYPE_NAME))

    if jce.get(TYPE_DESCRIPTION):
      build_documention(simple_type, jce.get(TYPE_DESCRIPTION))

    if jce[TYPE_OPTIONS]:
      active_jadn_opts = get_active_type_option_vals(jce[TYPE_OPTIONS], jce.get(BASE_TYPE))
      
      if active_jadn_opts:
      
        if jce.get(BASE_TYPE) == INTEGER_CONST:
          build_integer_format_opts(simple_type, active_jadn_opts, jce.get(BASE_TYPE))  
          
        if jce.get(BASE_TYPE) == NUMBER_CONST:
          build_number_format_opts(simple_type, active_jadn_opts, jce.get(BASE_TYPE))                


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
    
    min_occurs = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MINV_CONST)
    max_occurs = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MAXV_CONST)
    
    if not max_occurs:
      max_occurs = max_occurs_unbounded 
      
    xsd_element = build_element(xsd_seq_1, jce[TYPE_NAME] + '-Elements', type=None, min_occurs=min_occurs, max_occurs=max_occurs)
    xsd_complex_type_2 = build_complex_type(xsd_element)
    xsd_seq_2 = build_sequence(xsd_complex_type_2)
    
    build_fields(xsd_seq_2, jce)  


def build_arrayOf_or_mapOf_type(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    xsd_seq_1 = build_sequence(xsd_complex_type_1)
    
    minv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MINV_CONST)
    maxv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MAXV_CONST)
    vtype_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), VTYPE_CONST)
    
    if not maxv_opt:
      maxv_opt = max_occurs_unbounded
      
    xsd_element = build_element(xsd_seq_1, jce[TYPE_NAME] + '-Elements', type=None, min_occurs=minv_opt, max_occurs=maxv_opt)
    xsd_complex_type_2 = build_complex_type(xsd_element)
    xsd_seq_2 = build_sequence(xsd_complex_type_2)
    
    if jce.get(BASE_TYPE) == ARRAYOF_CONST:
      unique_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), UNIQUE_CONST)   
      set_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), SET_CONST)   
      # XSD 1.0 does not have order restrictions, also unordered is the default
      # unordered_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), UNORDERED_CONST)   
      build_element(xsd_seq_2, vtype_opt, vtype_opt, is_unique=unique_opt, is_set=set_opt)        
      
    elif jce.get(BASE_TYPE) == MAPOF_CONST:
      ktype_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), KTYPE_CONST)
      
      build_element(xsd_seq_2, ktype_opt, ktype_opt)
      build_element(xsd_seq_2, vtype_opt, vtype_opt)          
    
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
    jadn_info = None
    jadn_exports = None
    
    if jadn_dict.get('info'):
      jadn_info= jadn_dict['info']
      
      if jadn_info.get('exports'):
        jadn_exports = jadn_info['exports']
        
    jadn_types = jadn_dict['types']

    if jadn_exports:
      build_global_elements(root, jadn_exports)
      
    build_base_types(root)
    build_types(root, jadn_types)    
    
    write_to_file(root, "music_lib.xsd") 
   
   
if __name__=="__main__":    
   create_jadn_xsd()