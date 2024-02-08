import xml.etree.ElementTree as ET


def json_to_xml(json_data, parent):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            element = ET.SubElement(parent, key)
            json_to_xml(value, element)
    else:
        parent.text = str(json_data)

def build_xml_from_json_str(json_data: dict | str, root: str = "root"):  
    
    root = ET.Element(root)
    json_to_xml(json_data, root)
    ET.indent(root, space="\t", level=0)
    xml_str = ET.tostring(root, encoding='unicode')    
    print(xml_str)
    
    return xml_str