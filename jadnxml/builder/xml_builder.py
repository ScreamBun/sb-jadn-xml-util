import json

from dict2xml import dict2xml


def build_xml_from_json(data: dict):  
    
    xml = "<></>"
    if not isinstance(data, dict):
        data = json.loads(data)
    else:
        xml = dict2xml(data)
        # print(xml)
        
    return xml