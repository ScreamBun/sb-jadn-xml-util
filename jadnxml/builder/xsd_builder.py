import xml.etree.ElementTree as ET
from jadnxml.helpers.jadn_helper import get_active_type_option_vals, get_opt_type_val, get_type_option_val, get_vtype
from jadnxml.helpers.xsd_helper import add_maxoccurs_to_element, add_minoccurs_to_element, build_choice, build_complex_type, build_documention, build_element, build_enumeration, build_fraction_digits, build_import, build_max_inclusive, build_max_length, build_min_inclusive, build_min_length, build_pattern, build_restriction, build_sequence, build_simple_type

from jadnxml.constants.jadn_constants import ARRAY_CONST, ARRAYOF_CONST, BASE_TYPE, BINARY_CONST, BINARY_REG_CONST, DATE, DATE_TIME, DURATION, ENUM_CONST, F16, F16_DIGITS, F32, F32_DIGITS, FIELDS, FORMAT_CONST, FORMAT_OPTIONS_FROZ_DICT, INTEGER_CONST, KTYPE_CONST, MAP_CONST, MAPOF_CONST, MAXF_CONST, MAXV_CONST, MINF_CONST, MINV_CONST, NUMBER_CONST, PATTERN_CONST, POINTER_CONST, PRIMITIVE_TYPES, RECORD_CONST, SELECTOR_TYPES, SET_CONST, STRING_CONST, STRUCTURED_TYPES, TIME, TYPE_DESCRIPTION, TYPE_NAME, TYPE_OPTIONS, UNIQUE_CONST, UNSIGNED_BITS, VTYPE_CONST
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

    # date
    date_type = build_simple_type(root, DATE)
    build_restriction(date_type, xs_date) 
    
    # time
    time_type = build_simple_type(root, TIME)
    build_restriction(time_type, xs_time)     
    
    # dateTime
    date_time_type = build_simple_type(root, DATE_TIME)
    build_restriction(date_time_type, xs_dateTime)         
    
    # string formats with regex
    string_base_types_w_reg = find_items_by_val(FORMAT_OPTIONS_FROZ_DICT, STRING_CONST)
    binary_base_types_w_reg = find_items_by_val(FORMAT_OPTIONS_FROZ_DICT, BINARY_CONST)
    string_binary_base_types_w_reg = {**string_base_types_w_reg, **binary_base_types_w_reg}
    for type_key, type_value in string_binary_base_types_w_reg.items():
      if type_value[3]:
        base_type = build_simple_type(root, type_key)
        base_restriction = build_restriction(base_type, xs_string)
        build_pattern(base_restriction, type_value[3])   
                  
    for struct_key, struct_value in STRUCTURED_TYPES.items():
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
    for field in (jce.get(FIELDS) or []):
      field_index = field[0]
      field_name = field[1]
      field_type = field[2]
      field_opts = field[3]
      field_desc = field[4]
      
      if field_type == ARRAYOF_CONST:
        field_type = get_vtype(field_opts)
        
      field_type_et = build_element(xsd_seq, field_name, id=field_index, type=field_type)
      
      if field_opts:
        
        # field_type_et = add_id_to_element(field_type_et, field_opts)        
        field_type_et = add_minoccurs_to_element(field_type_et, field_opts)
        field_type_et = add_maxoccurs_to_element(field_type_et, field_opts)       
        
        #TODO: key, link, not using yet?
        # field_type_et = add_ref_to_element(field_type_et, field_opts)       
        
        #TODO: dir?
        
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
        build_min_inclusive(restriction, minv_val)       
        
      if maxv_val:     
        build_max_inclusive(restriction, maxv_val)         

    else:
                  
      if minv_val or maxv_val:
        restriction = build_restriction(parent_et, base_type)
                
        if minv_val:     
          build_min_inclusive(restriction, minv_val)       
          
        if maxv_val:     
          build_max_inclusive(restriction, maxv_val)   


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
      field_id = field[0]
      field_value = field[1]
      field_description = safe_list_get(field, 2,  None)
      
      build_enumeration(xsd_restriction, field_id, field_value, field_description)


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
        build_element(schema_et, export, export)  
        
    xml_str = ET.tostring(schema_et, encoding='unicode')            
    
  except RuntimeError as e:
    print("Error convert_xsd_from_dict: " + e.message)
    raise e  

  return xml_str


def convert_to_xsd_from_file(jadn_file_name: str):
    try:
      
      jadn_dict = read_type_data_from_file(jadn_file_name)
      schema_et = convert_xsd_from_dict(jadn_dict)
      
      write_filename = get_file_name_only(jadn_file_name)
      write_filename = write_filename + ".xsd"
      write_to_file(schema_et, write_filename) 
      
    except RuntimeError as e:
      print("Error convert_to_xsd_from_file: " + e.message)
      raise e   
    
    return True   
