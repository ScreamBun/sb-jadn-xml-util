import json
import xml.etree.ElementTree as ET

from dicttoxml import dicttoxml


def build_xml_from_json(data: dict):  
    
    xml = "<></>"
    if not isinstance(data, dict):
        data = json.loads(data)
    else:
        xml = dicttoxml(data)
        print(xml)
        
    return xml