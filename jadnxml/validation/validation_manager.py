import sys
import traceback
from jadnxml.utils.utils import get_xml_file, get_xsd_file
from lxml import etree

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

def validate_xml_str(xsd_str: str, xml_str: str):
    xml_doc = etree.fromstring(xml_str)
    xsd_doc = etree.fromstring(xsd_str)
    is_valid = False
    
    if xml_doc is None or xsd_doc is None:
        print("Error: XML or XSD document is None")
        return False
    
    try:
        xml_schema = etree.XMLSchema(xsd_doc)
    except Exception as e:
        print(f"XML Syntax Error: {e}")
        return False

    try: 
        is_valid = xml_schema.validate(xml_doc)
        
        if not is_valid:
            print("Validation failed. Error log:")
            for error in xml_schema.error_log:
                print(f"Line {error.line}: {error.message}")        
        
    except Exception as e:
        print(f"XML Validation Error: {e}")
        return False
    
    return is_valid