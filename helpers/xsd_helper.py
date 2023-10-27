import xml.etree.ElementTree as ET
from constants.jadn_constants import BASE_TYPE, TYPE_NAME, TYPE_OPTIONS
from helpers.jadn_helper import get_type_option_vals
from helpers.options_helper import get_jadn_option

from constants.xsd_constants import *
from utils.utils import safe_list_get
            


def build_choice(parent_et_tag: ET.Element):
    choice = ET.SubElement(parent_et_tag, choice_tag)

    return choice


def build_complex_type(parent_et_tag: ET.Element, name: str = None):
    complex_type = ET.SubElement(parent_et_tag, complexType_tag)
    
    if name:
        complex_type.set('name', name)

    return complex_type


def build_documention(parent_et_tag: ET.Element, documenttion_str: str):
    annotation = ET.SubElement(parent_et_tag, annotation_tag)
    documentation = ET.SubElement(annotation, documentation_tag).text = documenttion_str

    return annotation


def build_element(parent_et_tag: ET.Element, name: str, type: str = None, min_occurs: str = None, max_occurs: str = None, is_unique: str = False, is_set: str = False):
    elem_et = ET.SubElement(parent_et_tag, element_tag, name=name) 

    if type:
        elem_et.set('type', type)

    if min_occurs:
        elem_et.set('minOccurs', min_occurs)

    if max_occurs:
        elem_et.set('maxOccurs', max_occurs)

    if is_unique or is_set:
        unique_et = ET.SubElement(elem_et, unique_tag, name=name + '-Unique')
        ET.SubElement(unique_et, selector_tag, xpath=name)
        ET.SubElement(unique_et, field_tag, xpath='.')

    # if ref:
    #     elem_et.set('ref', ref)        

    # if safe_list_get(type, 4, None):
    #     elem_desc = type[4]
    #     build_documention(elem_et, elem_desc)    

    return elem_et


def build_enumeration(parent_et_tag: ET.Element, value: str):
    enumeration = ET.SubElement(parent_et_tag, enumeration_tag, value=value)

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
    restriction = ET.SubElement(parent_et_tag, restriction_tag, base=base)

    return restriction


def build_sequence(parent_et_tag: ET.Element):
    seq = ET.SubElement(parent_et_tag, sequence_tag)

    return seq


def build_simple_type(parent_et_tag: ET.Element, jadn_name: str):
    simple_type = ET.SubElement(parent_et_tag, simple_type_tag, name=jadn_name)    

    return simple_type



