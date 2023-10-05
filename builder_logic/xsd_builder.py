import xml.etree.ElementTree as ET

from builder_logic.xsd_constants import *
from utils.utils import safe_list_get


def build_documention(parent_et_tag: ET.Element, documenttion_str: str):
    annotation = ET.SubElement(parent_et_tag, annotation_tag)
    documentation = ET.SubElement(annotation, documentation_tag).text = documenttion_str

    return annotation


def build_element(parent_et_tag: ET.Element, type: [], max_occurs: str = None, ref: str = None):
    elem_name = safe_list_get(type, 1, None)
    elem_type = safe_list_get(type, 2, None)

    # if elem_type not in primitives:
    #     ref = elem_type
    #     elem_type = None

    elem_et = ET.SubElement(parent_et_tag, element_tag, name=elem_name)  # TODO min/max occurs

    if elem_type:
        elem_et.set('type', elem_type)

    if max_occurs:
        elem_et.set('maxOccurs', max_occurs)

    if ref:
        elem_et.set('ref', ref)        

    if safe_list_get(type, 4, None):
        elem_desc = type[4]
        build_documention(elem_et, elem_desc)    

    return elem_et


def build_enumeration(parent_et_tag: ET.Element, value: str):
    enumeration = ET.SubElement(parent_et_tag, enumeration_tag, value=value)

    return enumeration


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

def build_complex_type(parent_et_tag: ET.Element, jadn_name: str):
    complex_type = ET.SubElement(parent_et_tag, complexType_tag, name=jadn_name)    

    return complex_type


def get_jadn_option(options: []):
    return_options = {}

    if len(options) > 0:

        # TODO: just handling first option for now....need for loop
        for option in options:

            # TODO: add other options
            # regex
            if options_keys["regex"] == option[0]:
                trimmed_option = option[1:]
                return_options['%'] = trimmed_option 
          
    return return_options