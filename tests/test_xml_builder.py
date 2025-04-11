from jadnxml.builder.xml_builder import build_py_from_xml, build_xml_from_json


def test_build_xml_from_json_dict():
    
    json_data = {
        "person": {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
        }
    }
    
    # filename = "output.xml"
    
    tree = build_xml_from_json(json_data)
    
    # ET.indent(tree, space="\t", level=0)
    # tree.write("./_out/" + filename,
    #           xml_declaration=True,encoding='utf-8',
    #           method="xml")  
    
    assert tree != None
    
def test_build_py_from_xml_array():
    
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <items>
        <item>test</item>
        <item>True</item>
        <item>123</item>
    </items>"""
    
    root = "Root-Test"
    schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    json_data = build_py_from_xml(schema, root, xml)
    
    assert json_data != None    