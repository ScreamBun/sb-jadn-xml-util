import xml.etree.ElementTree as ET
from jadnxml.constants.jadn_constants import ATTR_CONST, FIELD_OPTIONS_FROZ_DICT, FIELDS, MAXC_CONST, MINC_CONST, PRIMITIVES, TAGID_CONST 
from jadnxml.helpers.jadn_helper import get_base_type, get_field_option_val
from jadnxml.constants.xsd_constants import choice_tag, complexType_tag, annotation_tag, documentation_tag, element_tag, jadn_prefix, unique_tag, selector_tag, field_tag, enumeration_tag, fraction_digits_tag, group_tag, import_tag, max_length_tag, min_length_tag, max_inclusive_tag, min_inclusive_tag, pattern_tag, restriction_tag, sequence_tag, simple_type_tag
from jadnxml.utils.general import split_on_first_char
from jadnxml.utils.utils import remove_special_characters
            
            
def build_attrs(el: ET.Element, jce: dict, ref_attrs: list = None):
    for field in (jce.get(FIELDS) or []):
        field_name = field[1]
        field_type = field[2]
        field_opts = field[3]
        field_desc = field[4]

        if (
            (field_type in PRIMITIVES and is_attr_opt_found(field_opts)) or
            (ref_attrs is not None and field_type in ref_attrs)
        ):
            attrib_el = ET.SubElement(el, "xs:attribute")
            attrib_el.set("name", field_name)
            attrib_el.set("type", "xs:string") 
            
            is_optional = is_field_optional(field)            
            if is_optional:
                attrib_el.set("use", "optional")
            else:
                attrib_el.set("use", "required")
                
            if field_desc:
                build_documention(attrib_el, field_desc)
                
    return el

def add_id_to_element(et_tag: ET.Element, field_opts: [] = [], val: str = None): 
    if val:  
        et_tag.set('id', val)
    else:    
        id = FIELD_OPTIONS_FROZ_DICT.get(TAGID_CONST)
        val = get_field_option_val(field_opts, id)
        
        if val:  
            et_tag.set('id', val)
    
    return et_tag


def add_minoccurs_to_element(et_tag: ET.Element, field_opts: [] = [], val: str = None):   
    if val:  
        et_tag.set('minOccurs', val)
    else:    
        id = FIELD_OPTIONS_FROZ_DICT.get(MINC_CONST)
        val = get_field_option_val(field_opts, id)
        
        if val:  
            et_tag.set('minOccurs', val)        
    
    return et_tag


def check_for_unbounded(val: str):
    return_val = val
    if val == "0":
        return_val = "unbounded"
    return return_val


def add_maxoccurs_to_element(et_tag: ET.Element, field_opts: [] = [], val: str = None): 
    if val:  
        xsd_val = check_for_unbounded(val)
        et_tag.set('maxOccurs', xsd_val)
    else:    
        id = FIELD_OPTIONS_FROZ_DICT.get(MAXC_CONST)
        val = get_field_option_val(field_opts, id)
        
        if val:  
            xsd_val = check_for_unbounded(val)
            et_tag.set('maxOccurs', xsd_val)    
    
    return et_tag


def build_choice(parent_et_tag: ET.Element):
    choice = ET.SubElement(parent_et_tag, choice_tag)

    return choice


def build_complex_type(parent_et_tag: ET.Element, name: str = None):
    complex_type = ET.SubElement(parent_et_tag, complexType_tag)
    
    if name:
        
        if not parent_et_tag.attrib.get('name'):
        
            complex_type.set('name', name)

    return complex_type


def build_documention(parent_et_tag: ET.Element, documenttion_str: str):
    annotation = None
    if documenttion_str:
        annotation = ET.SubElement(parent_et_tag, annotation_tag)
        documentation = ET.SubElement(annotation, documentation_tag).text = documenttion_str

    return annotation


def build_element(parent_et_tag: ET.Element, name: str, id: str= None, type: str = None, min_occurs: str = None, max_occurs: str = None, is_unique: str = False, is_set: str = False):
    elem_et = ET.SubElement(parent_et_tag, element_tag) 

    if id:
        elem_et.set('id', str(id))
        
    if name:
        name = remove_special_characters(name)
        elem_et.set('name', name)        

    if type:
        is_base_type = get_base_type(type)
        if is_base_type:
            type = jadn_prefix + type
        
        elem_et.set('type', type)

    if min_occurs:
        elem_et.set('minOccurs', min_occurs)

    if max_occurs:
        xsd_val = check_for_unbounded(max_occurs)
        elem_et.set('maxOccurs', xsd_val)

    if is_unique or is_set:
        unique_et = ET.SubElement(elem_et, unique_tag, name=name + '-Unique')
        ET.SubElement(unique_et, selector_tag, xpath=name)
        ET.SubElement(unique_et, field_tag, xpath='.')   

    return elem_et


def build_enumeration(parent_et_tag: ET.Element, id: str, value: str, description: str = None):
    enumeration = ET.SubElement(parent_et_tag, enumeration_tag)
    
    if id:
        # id_txt = "enumeration_" + str(id)
        enumeration.set('id', str(id))
        # enumeration.set('id', id_txt)
    
    if value:
        enumeration.set('value', value)  
    
    if description:
           enumeration = build_documention(enumeration, description)

    return enumeration


def build_fraction_digits(parent_et_tag: ET.Element, value: str):
    fraction_digits = ET.SubElement(parent_et_tag, fraction_digits_tag, value=value)

    return fraction_digits


def build_group_ref(parent_et_tag: ET.Element, ref: str):
    group_ref = ET.SubElement(parent_et_tag, group_tag, ref=ref + 'Group')
                     

    return group_ref


def build_group(parent_et_tag: ET.Element, name: str = None, minOccurs: str = None, maxOccurs: str = None):
    group = ET.SubElement(parent_et_tag, group_tag)
    
    if name:
        group.set('name', name + 'Group')  
        
    if minOccurs:
        group.set('minOccurs', minOccurs)  
        
    if maxOccurs:
        group.set('maxOccurs', maxOccurs)                    

    return group


def build_element_id(parent_name: str, element_name: str):
    id = str(parent_name) + "_" + str(element_name)
    id = id.replace('-', '_')
    return id.lower()


def build_import(parent_et_tag: ET.Element, schema_loc: str, namespace: str):
    import_et = ET.SubElement(parent_et_tag, import_tag)
    
    if schema_loc:
        import_et.set('schemaLocation', schema_loc)   
        
    if namespace:
        import_et.set('namespace', namespace)           

    return import_et


def build_max_length(parent_et_tag: ET.Element, value: str):
    max_length = ET.SubElement(parent_et_tag, max_length_tag)
    
    if value:
        max_length.set('value', value)    

    return max_length


def build_min_length(parent_et_tag: ET.Element, value: str):
    min_length = ET.SubElement(parent_et_tag, min_length_tag)
    
    if value:
        min_length.set('value', value)    

    return min_length


def build_max_inclusive(parent_et_tag: ET.Element, value: str):
    max_inclusive = ET.SubElement(parent_et_tag, max_inclusive_tag)
    
    if value:
        max_inclusive.set('value', value)      

    return max_inclusive


def build_min_inclusive(parent_et_tag: ET.Element, value: str):
    min_inclusive = ET.SubElement(parent_et_tag, min_inclusive_tag)
    
    if value:
        min_inclusive.set('value', value)    

    return min_inclusive


def build_pattern(parent_et_tag: ET.Element, restriction_pattern: str):
    pattern = ET.SubElement(parent_et_tag, pattern_tag, value=restriction_pattern)      

    return pattern


def build_restriction(parent_et_tag: ET.Element, base: str):
    restriction = None
    
    is_base_type = get_base_type(base)
    if is_base_type:
        base = jadn_prefix + base      
    
    if "element" in parent_et_tag.tag:
        simple_type_tag = build_simple_type(parent_et_tag)      
        restriction = ET.SubElement(simple_type_tag, restriction_tag, base=base)
    else:
        restriction = ET.SubElement(parent_et_tag, restriction_tag, base=base)
           
    if parent_et_tag.attrib.get('type'):
        if restriction.attrib.get('base'):
            parent_et_tag.attrib.pop('type')
            # Note: Can't have a element type and a restriction base, must be one or the other
            # Removing element type and keeping more specific restriction base

    return restriction


def build_sequence(parent_et_tag: ET.Element):
    seq = ET.SubElement(parent_et_tag, sequence_tag)

    return seq


def build_simple_type(parent_et_tag: ET.Element, jadn_name: str = None):
    simple_type = ET.SubElement(parent_et_tag, simple_type_tag)  
    
    if jadn_name:  
        simple_type.set('name', jadn_name)

    return simple_type


def get_min_length(opts: list) -> int:
    min_val = get_opt_int("{", opts)
    # if min_val == None:
    #     min_val = 0    
    return min_val


def get_min_occurs(opts: list) -> int:
    min_val = get_opt_int("[", opts)
    if min_val == None:
        min_val = 1
    return min_val


def get_opt_int(key: str, opts: list):
    return_val = None

    for opt in opts:
        opt_key, opt_val = split_on_first_char(opt)
        if key == opt_key:
            try:
                return_val = int(opt_val)
            except ValueError as e:
                print("Invalid option: requires integer value: " + e)
            break
        
    return return_val

def is_attr_opt_found(val: list):
    return_val = False
    if val and ATTR_CONST in val:
        return_val = True
    return return_val


def is_field_optional(j_field: list) -> bool: 
    is_optional = False
    
    field_opts = j_field[3] if len(j_field) > 3 else []
    
    min_occurs = get_min_occurs(field_opts)
    min_length = get_min_length(field_opts)
    
    if min_length == 0 or min_occurs == 0:
        is_optional = True
    
    return is_optional


def split_types_by_attr(types_list):
    """
    Splits types into those with '/attr' in their options and those without.
    Sets self.jadn_types_dict to types without '/attr' and self.ref_attrs to types with '/attr'.
    Returns (types_without_attr, types_with_attr)
    """
    
    types_with_attr = []
    types_without_attr = []
    
    for t in types_list:
        opts = t[2] if len(t) > 2 else []
        if any(opt == "/attr" for opt in opts):
            # types_with_attr.append(t)
            types_with_attr.append(t[0])
        else:
            types_without_attr.append(t)

    return types_without_attr, types_with_attr


