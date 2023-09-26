from lxml import etree
from utils.utils import get_xml_file, get_xsd_file

# Ref: https://github.com/usnistgov/OSCAL/blob/main/src/utils/oscal-content-validator.py

def validate_xml(xsd_file_name, xml_file_name):

    xmlschema = get_xsd_file(xsd_file_name)  
    xml_doc = get_xml_file(xml_file_name)  

    # Validate the XML document using the XML schema
    xmlschema.assertValid(xml_doc)
    is_valid = xmlschema.validate(xml_doc)        

    return is_valid
