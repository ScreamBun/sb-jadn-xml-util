import sys
import traceback
from jadnxml.utils.utils import get_xml_file, get_xsd_file

# Ref: https://github.com/usnistgov/OSCAL/blob/main/src/utils/oscal-content-validator.py

def validate_xml(xsd_file_name, xml_file_name):
    print(f"Validating '{xml_file_name}' data against '{xsd_file_name}' schema")
    is_valid = False
    
    try:
      
        xmlschema = get_xsd_file(xsd_file_name)  
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
