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
    
## Leftoff here..........    
    
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
    
def test_build_py_from_xml_choice_id():
    
    xml = """<Root-Test>
        <field_value_1 key="1">data 1</field_value_1>
    </Root-Test>"""
    
    root = "Root-Test"
    schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    json_data = build_py_from_xml(schema, root, xml)
    
    assert json_data != None

def test_build_py_from_xml_f32():
    xml = """<Root-Test>
        <float>3.14</float>
    </Root-Test>"""

    root = "Root-Test"
    schema = {
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "Number", ["/f32"], ""]
            ]]
        ]
    }

    json_data = build_py_from_xml(schema, root, xml)

    assert json_data is not None

def test_build_py_from_xml_integer():
    xml = """<Root-Test>
        <integer>423123</integer>
        <integer>123</integer>
        <integer>456</integer>
        <integer>1011</integer>
        <integer>2025</integer>
        <integer>1230</integer>
    </Root-Test>"""

    root = "Root-Test"
    schema = {
        "types": [
            ["Root-Test", "Record", [], "", [
                        [1, "field1", "Integer", ["/date-time"], ""],
                        [2, "field2", "Integer", ["/date"], ""],
                        [3, "field3", "Integer", ["/time"], ""],
                        [4, "field4", "Integer", ["/gYearMonth"], ""],
                        [5, "field5", "Integer", ["/gYear"], ""],
                        [6, "field6", "Integer", ["/gMonthDay"], ""]
            ]]
        ]
    }

    json_data = build_py_from_xml(schema, root, xml)

    assert json_data is not None
    
def test_build_py_from_xml_choice():
    
    xml = """<Root-Test>
        <field_value_1 key="1">data 1</field_value_1>
    </Root-Test>"""
    
    root = "Root-Test"
    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    json_data = build_py_from_xml(j_schema, root, xml)
    
    assert json_data != None   