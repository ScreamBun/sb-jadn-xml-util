import sys
import traceback
import xml.etree.ElementTree as ET
from jadnxml.helpers.jadn_helper import get_active_type_option_vals, get_opt_type_val, get_type_option_val, get_vtype
from jadnxml.helpers.xsd_helper import add_maxoccurs_to_element, add_minoccurs_to_element, build_choice, build_complex_type, build_documention, build_element, build_element_id, build_enumeration, build_fraction_digits, build_import, build_max_inclusive, build_max_length, build_min_inclusive, build_min_length, build_pattern, build_restriction, build_sequence, build_simple_type

from jadnxml.constants.jadn_constants import ARRAY_CONST, ARRAYOF_CONST, BASE_TYPE, BINARY_CONST, BINARY_REG_CONST, DATE, DATE_TIME, DURATION, ENUM_CONST, F16, F16_DIGITS, F32, F32_DIGITS, FIELDS, FORMAT_CONST, FORMAT_OPTIONS_FROZ_DICT, INTEGER_CONST, IPV4_NET, IPV6_NET, KTYPE_CONST, MAP_CONST, MAPOF_CONST, MAXF_CONST, MAXV_CONST, MINF_CONST, MINV_CONST, NUMBER_CONST, PATTERN_CONST, POINTER_CONST, PRIMITIVE_TYPES, RECORD_CONST, SELECTOR_TYPES, SET_CONST, STRING_CONST, STRUCTURED_TYPES, TIME, TYPE_DESCRIPTION, TYPE_NAME, TYPE_OPTIONS, UNIQUE_CONST, UNSIGNED_BITS, VTYPE_CONST
from jadnxml.constants.xsd_constants import xs_string, xs_decimal, xs_date, xs_time, xs_dateTime, max_occurs_unbounded, jadn_prefix, pattern_tag, enumerations, primitives, specializations, structures, schema_tag, jadn_namespace, jadn_base_type_file_loc
from jadnxml.utils.utils import find_items_by_val, get_file_name_only, read_type_data_from_file, safe_list_get, write_to_file


jadn_types_dict: {} = {}

def get_common_elements(type: []):
    common_elements = {} 
    common_elements[TYPE_NAME] = safe_list_get(type, 0, None)
    common_elements[BASE_TYPE] = safe_list_get(type, 1, None)
    common_elements[TYPE_OPTIONS] = safe_list_get(type, 2, None)
    common_elements[TYPE_DESCRIPTION] = safe_list_get(type, 3, None)
    common_elements[FIELDS] = safe_list_get(type, 4, None)
    return common_elements
      
def build_fields(xsd_seq: ET.Element, jce: dict):
    for field in (jce.get(FIELDS) or []):
      field_index = field[0]
      field_name = field[1]
      field_type = field[2]
      field_opts = field[3]
      field_desc = field[4]
      
      if field_type == ARRAYOF_CONST:
        field_type = get_vtype(field_opts)
        
      id = build_element_id(jce[TYPE_NAME], field_name)
      field_type_et = build_element(xsd_seq, field_name, id=id, type=field_type)
      
      if field_opts:
        field_type_et = add_minoccurs_to_element(field_type_et, field_opts)
        field_type_et = add_maxoccurs_to_element(field_type_et, field_opts)       
        
        global jadn_types_dict
        active_jadn_opts = get_active_type_option_vals(field_opts, field_type, jadn_types_dict)
        
        if active_jadn_opts:
        
          if field_type == INTEGER_CONST:
            build_integer_type_opts(field_type_et, active_jadn_opts, field_type)  
            
          if field_type == NUMBER_CONST:
            build_number_type_opts(field_type_et, active_jadn_opts, field_type) 
            
          if field_type == STRING_CONST:
            build_string_type_opts(field_type_et, active_jadn_opts, field_type)         


def build_binary_type_opts(parent_et: ET.Element, jadn_opts: {}, base_type: str):  
  if jadn_opts:
    
    format_val = get_opt_type_val(FORMAT_CONST, jadn_opts) 
    minv_val = get_opt_type_val(MINV_CONST, jadn_opts)
    maxv_val = get_opt_type_val(MAXV_CONST, jadn_opts)

    if format_val:
      frozen_format_opt = FORMAT_OPTIONS_FROZ_DICT.get(format_val)
      restriction = build_restriction(parent_et, jadn_prefix + format_val)
      build_documention(restriction, frozen_format_opt[4])
      
      if minv_val:     
        build_min_length(restriction, minv_val)       
        
      if maxv_val:     
        build_max_length(restriction, maxv_val)         

    else:
                  
      if minv_val or maxv_val:
        restriction = build_restriction(parent_et, base_type)
                
        if minv_val:     
          build_min_length(restriction, minv_val)       
          
        if maxv_val:     
          build_max_length(restriction, maxv_val)   


def build_integer_type_opts(parent_et: ET.Element, jadn_opts: {}, base_type: str):  
  if jadn_opts:
    format_val = get_opt_type_val(FORMAT_CONST, jadn_opts) 
    
    if format_val:
      for frozen_format_opt in FORMAT_OPTIONS_FROZ_DICT.items():
        frozen_format_opt_name = frozen_format_opt[0]
        if format_val == frozen_format_opt_name:
          
          if format_val == DURATION:
            restriction = build_restriction(parent_et, jadn_prefix + format_val)
          else:
            restriction = build_restriction(parent_et, jadn_prefix + base_type)
            
          build_documention(restriction, FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[4])
          
          # Min
          if FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[1]:
            build_min_inclusive(restriction, FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[1])
            
          # Max
          if FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[2]:
            build_max_inclusive(restriction, FORMAT_OPTIONS_FROZ_DICT.get(frozen_format_opt_name)[2])  
            
          if format_val == UNSIGNED_BITS:
            build_pattern(restriction, BINARY_REG_CONST)                              
    
    else:                
      minv_val = get_opt_type_val(MINV_CONST, jadn_opts)
      maxv_val = get_opt_type_val(MAXV_CONST, jadn_opts)
      
      if minv_val or maxv_val:
        restriction = build_restriction(parent_et, base_type)
        
        if minv_val:
          build_min_inclusive(restriction, minv_val)
        
        if maxv_val:
          build_max_inclusive(restriction, maxv_val)
        
        
def build_number_type_opts(parent_et: ET.Element, jadn_opts: {}, base_type: str):        
  if jadn_opts:
    
    format_val = get_opt_type_val(FORMAT_CONST, jadn_opts)
    minf_val = get_opt_type_val(MINF_CONST, jadn_opts)
    maxf_val = get_opt_type_val(MAXF_CONST, jadn_opts)
    
    if format_val:
      frozen_format_opt = FORMAT_OPTIONS_FROZ_DICT.get(format_val)
      restriction = build_restriction(parent_et, jadn_prefix + format_val)
      build_documention(restriction, frozen_format_opt[4])
      
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
          
          
def build_string_type_opts(parent_et: ET.Element, jadn_opts: {}, base_type: str):        
  if jadn_opts:
    
    format_val = get_opt_type_val(FORMAT_CONST, jadn_opts)
    minv_val = get_opt_type_val(MINV_CONST, jadn_opts)
    maxv_val = get_opt_type_val(MAXV_CONST, jadn_opts)                                           
    pattern_val = get_opt_type_val(PATTERN_CONST, jadn_opts)       
    
    if format_val:
      frozen_format_opt = FORMAT_OPTIONS_FROZ_DICT.get(format_val)
      restriction = build_restriction(parent_et, jadn_prefix + format_val)           
      
      build_documention(restriction, frozen_format_opt[4])      
      
      if format_val == DATE or format_val == DATE_TIME or format_val == TIME:

        if minv_val:
          print(f'Min length is not used by xs:date, xs:dateTime or xs:time')
          
        if maxv_val:
          print(f'Max length is not used by xs:date, xs:dateTime or xs:time')  
          
      else:
        if minv_val:
          build_min_length(restriction, minv_val)
          
        if maxv_val:
          build_max_length(restriction, maxv_val)
          
      if pattern_val:
        
        for child in restriction:
          if child.attrib and child.attrib != pattern_tag:
              restriction.remove(child)
        
        build_pattern(restriction, pattern_val)               
    
    else:
                  
      if minv_val or maxv_val:
        restriction = build_restriction(parent_et, base_type)
                
        if minv_val:     
          build_min_length(restriction, minv_val) 
          
        if maxv_val:     
          build_max_length(restriction, maxv_val)
          
      if pattern_val:
        
        if 'restriction' not in locals():          
          restriction = build_restriction(parent_et, base_type)
        
        build_pattern(restriction, pattern_val)              
     

def build_primitive_type(root: ET.Element, type: []):
    print(f"Building Primitive Type: {type[1]}")
    jce = get_common_elements(type)

    simple_type = build_simple_type(root, jce.get(TYPE_NAME))

    if jce.get(TYPE_DESCRIPTION):
      build_documention(simple_type, jce.get(TYPE_DESCRIPTION))

    if jce[TYPE_OPTIONS]:
      global jadn_types_dict
      active_jadn_opts = get_active_type_option_vals(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), jadn_types_dict)
      
      if active_jadn_opts:
        
        if jce.get(BASE_TYPE) == BINARY_CONST:
          build_binary_type_opts(simple_type, active_jadn_opts, jce.get(BASE_TYPE))  
      
        if jce.get(BASE_TYPE) == INTEGER_CONST:
          build_integer_type_opts(simple_type, active_jadn_opts, jce.get(BASE_TYPE))  
          
        if jce.get(BASE_TYPE) == NUMBER_CONST:
          build_number_type_opts(simple_type, active_jadn_opts, jce.get(BASE_TYPE)) 
          
        if jce.get(BASE_TYPE) == STRING_CONST:
          build_string_type_opts(simple_type, active_jadn_opts, jce.get(BASE_TYPE))            
          
      else:
        build_restriction(simple_type, jce.get(BASE_TYPE))
          
    else:
      build_restriction(simple_type, jce.get(BASE_TYPE))


def build_enumeration_type(root: ET.Element, type: []):
    print("Building Enumeration Type")
    jce = get_common_elements(type)

    xsd_simple_type = build_simple_type(root, jce[TYPE_NAME])

    if jce[TYPE_DESCRIPTION]:
      build_documention(xsd_simple_type, jce[TYPE_DESCRIPTION])
      
    xsd_restriction = None  
    if jce[TYPE_OPTIONS]:
      global jadn_types_dict
      jadn_opts = get_active_type_option_vals(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), jadn_types_dict) 
      
      if jadn_opts:     
        enum_val = get_opt_type_val(ENUM_CONST, jadn_opts) 
        pointer_val = get_opt_type_val(POINTER_CONST, jadn_opts)
      
        if enum_val:
          xsd_restriction = build_restriction(xsd_simple_type, enum_val)   
        elif pointer_val:
          xsd_restriction = build_restriction(xsd_simple_type, pointer_val)   

    if xsd_restriction == None:
      xsd_restriction = build_restriction(xsd_simple_type, STRING_CONST)

    for field in jce[FIELDS]:
      field_index = field[0]
      field_value = field[1]
      field_description = safe_list_get(field, 2,  None)
      
      id = build_element_id(jce[TYPE_NAME], field_value)
      build_enumeration(xsd_restriction, id, field_value, field_description)


def build_choice_type(root: ET.Element, type: []):
    print("Building Specialization (Choice) Type")
    jce = get_common_elements(type)
    
    xsd_comp_type = build_complex_type(root, jce[TYPE_NAME]) 
    
    if jce[TYPE_DESCRIPTION]:
      build_documention(xsd_comp_type, jce[TYPE_DESCRIPTION])    
    
    xsd_choice = build_choice(xsd_comp_type)
    build_fields(xsd_choice, jce)
    

def build_map_type(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    minv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MINV_CONST)
    maxv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MAXV_CONST)   
    
    if not minv_opt:
      minv_opt = "0"    
    
    if not maxv_opt:
      maxv_opt = max_occurs_unbounded         

    xsd_seq = build_sequence(xsd_complex_type_1)
    
    map_el = build_element(xsd_seq, jce[TYPE_NAME], min_occurs=minv_opt, max_occurs=maxv_opt)
    map_complex_type = build_complex_type(map_el)
    map_seq = build_sequence(map_complex_type)
    build_fields(map_seq, jce)     
        

def build_array_type(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    xsd_seq_1 = build_sequence(xsd_complex_type_1)
    
    minv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MINV_CONST)
    maxv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MAXV_CONST)
    format_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), FORMAT_CONST)
    
    if not minv_opt:
      minv_opt = "0"    
    
    if not maxv_opt:
      maxv_opt = max_occurs_unbounded  
    
    if format_opt == IPV4_NET:
      id_1 = build_element_id(jce[TYPE_NAME], format_opt)
      id_1 = build_element_id(id_1, BINARY_CONST)
      build_element(parent_et_tag=xsd_seq_1, name=id_1, id=id_1, type=BINARY_CONST, min_occurs=None, max_occurs=None, is_unique=None, is_set=None)
      id_2 = build_element_id(jce[TYPE_NAME], format_opt)
      id_2 = build_element_id(id_2, INTEGER_CONST)
      build_element(parent_et_tag=xsd_seq_1, name=id_2, id=id_2, type=INTEGER_CONST, min_occurs=None, max_occurs=None, is_unique=None, is_set=None)
      
    elif format_opt == IPV6_NET:
      id_1 = build_element_id(jce[TYPE_NAME], format_opt)
      id_1 = build_element_id(id_1, BINARY_CONST)
      build_element(parent_et_tag=xsd_seq_1, name=id_1, id=id_1, type=BINARY_CONST, min_occurs=None, max_occurs=None, is_unique=None, is_set=None)
      id_2 = build_element_id(jce[TYPE_NAME], format_opt)
      id_2 = build_element_id(id_2, INTEGER_CONST)
      build_element(parent_et_tag=xsd_seq_1, name=id_2, id=id_2, type=INTEGER_CONST, min_occurs=None, max_occurs=None, is_unique=None, is_set=None)
      
    else:
      array_el = build_element(xsd_seq_1, jce[TYPE_NAME], min_occurs=minv_opt, max_occurs=maxv_opt)
      array_complex_type = build_complex_type(array_el)
      array_seq = build_sequence(array_complex_type)
      build_fields(array_seq, jce)
   

def build_mapOf_type(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    xsd_seq_1 = build_sequence(xsd_complex_type_1)
    
    minv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MINV_CONST)
    maxv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MAXV_CONST)
    
    if not minv_opt:
      minv_opt = "0"
      
    if not maxv_opt:
      maxv_opt = max_occurs_unbounded
      
    ktype_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), KTYPE_CONST)
    vtype_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), VTYPE_CONST)      
      
    map_name = build_element_id(jce[TYPE_NAME], "map")

    xsd_element_1 = build_element(parent_et_tag=xsd_seq_1, 
                  name=map_name, 
                  id=map_name, 
                  type=None,
                  min_occurs=minv_opt,
                  max_occurs=maxv_opt,
                  is_unique=False, 
                  is_set=False)
    
    xsd_complex_type_2 = build_complex_type(xsd_element_1)
    xsd_seq_2 = build_sequence(xsd_complex_type_2)
    
    
    id_2 = build_element_id(map_name, ktype_opt)
    build_element(xsd_seq_2, ktype_opt, id_2)

    id_3 = build_element_id(map_name, vtype_opt)
    build_element(xsd_seq_2, vtype_opt, id_3)          


def build_arrayOf(root: ET.Element, jce: dict):
    print(f"Building {jce[TYPE_NAME]} Type")
    xsd_complex_type_1 = build_complex_type(root, jce[TYPE_NAME])
    
    if jce.get(TYPE_DESCRIPTION):
      build_documention(xsd_complex_type_1, jce.get(TYPE_DESCRIPTION))
      
    xsd_seq_1 = build_sequence(xsd_complex_type_1)
    
    minv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MINV_CONST)
    maxv_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), MAXV_CONST)
    vtype_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), VTYPE_CONST)
    
    if not minv_opt:
      minv_opt = "0"
    
    if not maxv_opt:
      maxv_opt = max_occurs_unbounded
    
    unique_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), UNIQUE_CONST)   
    set_opt = get_type_option_val(jce[TYPE_OPTIONS], jce.get(BASE_TYPE), SET_CONST)   
    
    id = build_element_id(jce[TYPE_NAME], jce[TYPE_NAME])
    build_element(xsd_seq_1, vtype_opt, id, is_unique=unique_opt, is_set=set_opt, min_occurs=minv_opt, max_occurs=maxv_opt) 
    
    
def build_record_type(root: ET.Element, jce: dict):
    print("Building Record Type")
    
    xsd_complex_type = build_complex_type(root, jce[TYPE_NAME])
    xsd_seq = build_sequence(xsd_complex_type)
    
    build_fields(xsd_seq, jce)    


def build_structure_type(root: ET.Element, type: []):
    print("Building Structure Types")
    jce = get_common_elements(type)

    if jce.get(BASE_TYPE) == MAP_CONST:
      build_map_type(root, jce)

    if jce.get(BASE_TYPE) == ARRAY_CONST:
      build_array_type(root, jce)

    if jce.get(BASE_TYPE) == MAPOF_CONST:
      build_mapOf_type(root, jce) 
      
    if jce.get(BASE_TYPE) == ARRAYOF_CONST:
      build_arrayOf(root, jce)                    

    if jce.get(BASE_TYPE) == RECORD_CONST:
      build_record_type(root, jce)     
      
      
def build_types(root : ET.Element):
    global jadn_types_dict
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
        
        
def convert_xsd_from_dict(jadn_dict: dict): 
  xml_str = None
  
  try:
  
    # TODO: jadn validation?

    schema_et = ET.Element(schema_tag)
    schema_et.set('xmlns:jadn', jadn_namespace)    
    build_import(schema_et, jadn_base_type_file_loc, jadn_namespace)
    
    jadn_info = None
    jadn_exports = None
    
    if jadn_dict.get('info'):
      jadn_info= jadn_dict['info']
      
      if jadn_info.get('exports'):
        jadn_exports = jadn_info['exports']
        
    global jadn_types_dict        
    jadn_types_dict = jadn_dict['types']
    
    build_types(schema_et)    
    
    if jadn_exports:
      for export in jadn_exports:
        build_element(schema_et, export, export, export)  
        
    ET.indent(schema_et, space="\t", level=0)        
    xml_str = ET.tostring(schema_et, encoding='unicode')            
    
  except RuntimeError as e:
    print("Error convert_xsd_from_dict: " + e.message)
    raise e  

  return (xml_str, schema_et)


def convert_to_xsd_from_file(jadn_file_name: str):
    try:
      
      jadn_dict = read_type_data_from_file(jadn_file_name)
      schmea_str, schema_et = convert_xsd_from_dict(jadn_dict)
      
      write_filename = get_file_name_only(jadn_file_name)
      write_filename = write_filename + ".xsd"
      write_to_file(schema_et, write_filename) 
      
    except RuntimeError as e:
      print("Error convert_to_xsd_from_file: " + e.message)
      raise e   
    except Exception as e:
      err = traceback.format_exception(*sys.exc_info())
      err_msg = err[3]
      print("JADN to XSD Error: " + err_msg)
      raise e 

    return True   
