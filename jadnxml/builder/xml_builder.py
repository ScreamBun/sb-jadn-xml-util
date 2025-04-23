
import json
import xmltodict
import xml.etree.ElementTree as ET

from dict2xml import dict2xml
from jadnxml.utils.utils import find_first_list, get_base_type_and_schema_type, get_dict_from_xml_data, get_list_from_xml_data, use_id_as_key

def build_xml_from_json(data: dict):  
    
    xml = "<></>"
    if not isinstance(data, dict):
        data = json.loads(data)
    else:
        xml = dict2xml(data)
        # print(xml)
        
    return xml

def build_py_from_xml(schema: dict, root: str, xml_str: str):
    data_dict = None
    try:
        # Parse the XML string (makes sure it is valid XML first)
        ET.fromstring(xml_str)
        
        types = schema.get('types')
        if types == None or types == []:
            raise ValueError(f"No Types defined")
        
        base_type, schema_type = get_base_type_and_schema_type(schema, root)        
        if base_type in ["Array", "ArrayOf"]:
            data_dict = get_list_from_xml_data(xml_str)
            
        elif base_type in ["Choice"]:
            is_use_id = use_id_as_key(schema_type)
            data_dict = get_dict_from_xml_data(xml_str, root, use_id_as_key=is_use_id)
            
        elif base_type in ["Map", "MapOf"]:
            is_use_id = use_id_as_key(schema_type)
            data_dict = get_dict_from_xml_data(xml_str, root, use_id_as_key=is_use_id)            
            
        else:
            data_dict = get_dict_from_xml_data(xml_str, root)

        # TODO: Other jadn types may need to be handled

        if data_dict == None:
            raise ValueError(f"Unable to locate root in xml")
        
    except Exception as e: 
        raise ValueError(f"Unable to parse xml, invalid data: {e}")
        
        
    return data_dict