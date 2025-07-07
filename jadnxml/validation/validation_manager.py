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

def validate_xml_str(xsd_f, xml_f):
    is_valid = False

    try:
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        xml_file_path = os.path.join(file_dir, './tests/tmp/' + xml_f)
        xml_file_path = os.path.abspath(os.path.realpath(xml_file_path)) 
        xsd_file_path = os.path.join(file_dir, './tests/tmp/' + xsd_f)
        xsd_file_path = os.path.abspath(os.path.realpath(xsd_file_path)) 

        #xsd_file = open(xsd_file_path)
        #xml_file = open(xml_file_path)

        with open(xsd_file_path, 'r') as f:
            xmlschema_doc = etree.parse(f)
        xmlschema = etree.XMLSchema(xmlschema_doc)

        xml_doc = etree.parse(xml_file_path)

        xmlschema.assert_valid(xml_doc)
        is_valid = xmlschema.validate(xml_doc)

        #xsd_file.close()
        #xml_file.close()
    except Exception as e:
        print(f"XML Validation Error: {e}")
        return (is_valid, e)

    return is_valid
