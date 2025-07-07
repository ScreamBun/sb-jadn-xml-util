import sys
import traceback
from jadnxml.utils.utils import get_xml_file, get_xsd_file
import xml.etree.ElementTree as ET
import xmltodict
from lxml import etree
import os

# Ref: https://github.com/usnistgov/OSCAL/blob/main/src/utils/oscal-content-validator.py

def validate_xml(xsd_file_name, xml_file_name):
    print(f"Validating '{xml_file_name}' data against '{xsd_file_name}' schema")
    is_valid = False
    
    try:
      
        xmlschema = get_xsd_file(xsd_file_name, True)  
        xml_doc = get_xml_file(xml_file_name)  

        # Validate the XML document using the XML schema
        xmlschema.assertValid(xml_doc)
        is_valid = xmlschema.validate(xml_doc)   
      
    except Exception as e:
        err = traceback.format_exception(*sys.exc_info())
        err_msg = err[3]
        print("XML Validation Error: " + err_msg)
        return (is_valid, err_msg)

    print(f"*** Is data valid? {is_valid} ***")
    return is_valid

def validate_xml_str(xsd, xml):
    xml_doc = etree.fromstring(xml)
    xsd_doc = etree.fromstring(xsd)
    xml_schema = etree.XMLSchema(xsd_doc)
    print(xml)
    try: 
        return xml_schema.validate(xml_doc)
    except Error as e:
        print(f"XML Validation Error: {e}")
        return False