import xml.etree.ElementTree as ET

from builder_logic.xsd_constants import *


def add_enumeration(parent_et_tag: ET.Element, value: str):
    enumeration = ET.SubElement(parent_et_tag, enumeration_tag, value=value)

    return enumeration


def add_restriction(parent_et_tag: ET.Element, base: str):
    restriction = ET.SubElement(parent_et_tag, restriction_tag, base=base)

    return restriction


def add_pattern(parent_et_tag: ET.Element, restriction_pattern: str):
    pattern = ET.SubElement(parent_et_tag, pattern_tag, value=restriction_pattern)      

    return pattern


def add_documention(parent_et_tag: ET.Element, documenttion_str: str):
    annotation = ET.SubElement(parent_et_tag, annotation_tag)
    documentation = ET.SubElement(annotation, documentation_tag).text = documenttion_str

    return annotation


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