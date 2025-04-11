
import json
import xmltodict
import xml.etree.ElementTree as ET

from dict2xml import dict2xml
from jadnxml.utils.utils import find_first_list

def build_xml_from_json(data: dict):  
    
    xml = "<></>"
    if not isinstance(data, dict):
        data = json.loads(data)
    else:
        xml = dict2xml(data)
        # print(xml)
        
    return xml

def build_py_from_xml(schema: dict, root: str, xml_str: str):
    xml_dict = None
    try:
        # Parse the XML string (makes sure it is valid XML)
        xml_et = ET.fromstring(xml_str)

        # Convert the XML data to a dictionary
        xml_dict = xmltodict.parse(xml_str)

        # Convert the dictionary to JSON
        # json_data = json.dumps(xml_dict, indent=4)
        
        types = schema.get('types')
        if types == None or types == []:
            raise ValueError(f"No Types defined")
        
        base_type = None
        for type in types:
            if type[0] == root:
                base_type = type[1]
                break    
        if base_type == None:
            raise ValueError(f"Root Type not found {root}")
        
        if base_type == "Array":
            xml_dict = find_first_list(xml_dict)
            
        # TODO: Other jadn types may need to be handled
        
    except Exception as e: 
        raise ValueError(f"Unable to parse xml, invalid data: {e}")
        
        
    return xml_dict