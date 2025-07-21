from jadnxml.builder.xsd_builder import XSDBuilder
from jadnxml.validation.validation_manager import validate_xml_str as validate


def test_field_attribute_from_field(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
            ["Record-Name", "Record", [], "", [
                [1, "id", "String", ["/attr"], ""],
                [2, "info_1", "String", [], ""],
                [2, "info_2", "String", [], ""]
            ]]
        ]
    }    

    # Step 2: Convert JADN to XSD
    builder = XSDBuilder()
    xsd_tuple = builder.convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)   

    valid_xml = """<Record-Name id="123">
        <info_1>Test</info_1>
        <info_2>True</info_2>
    </Record-Name>"""           
    
    invalid_xml = """<Record-Name id="abc123">
        <info_1>Some value</info_1>
        <info_2>1</info_2>
    </Record-Name>"""

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, valid_xml)
    assert valid is True
    
    valid = validate(xsd_string, invalid_xml)
    assert valid is False
    
def test_type_attribute_from_ref(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
            ["Record-Name", "Record", [], "", [
                [1, "id", "String-Test", [], ""],
                [2, "info_1", "String", [], ""],
                [2, "info_2", "String", [], ""]
            ]],
            ["String-Test", "String", ["/attr"], "", []]
        ]
    }    

    # Step 2: Convert JADN to XSD
    builder = XSDBuilder()
    xsd_tuple = builder.convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)   

    valid_xml = """<Record-Name id="123">
        <info_1>Test</info_1>
        <info_2>True</info_2>
    </Record-Name>"""           
    
    invalid_xml = """<Record-Name id="abc123">
        <info_1>Some value</info_1>
        <info_2>1</info_2>
    </Record-Name>"""

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, valid_xml)
    assert valid is True
    
    valid = validate(xsd_string, invalid_xml)
    assert valid is False
    

def test_type_attribute_optional(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
            ["Record-Name", "Record", [], "", [
                [1, "id", "String-Test", ["[0"], ""],
                [2, "info_1", "String", [], ""],
                [2, "info_2", "String", [], ""]
            ]],
            ["String-Test", "String", ["/attr"], "", []]
        ]
    }    

    # Step 2: Convert JADN to XSD
    builder = XSDBuilder()
    xsd_tuple = builder.convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)   

    valid_xml = """<Record-Name id="123">
        <info_1>Test</info_1>
        <info_2>True</info_2>
    </Record-Name>"""           
    
    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, valid_xml)
    assert valid is True    
    
    valid_xml = """<Record-Name>
        <info_1>Test</info_1>
        <info_2>True</info_2>
    </Record-Name>"""
    
    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, valid_xml)
    assert valid is True
    
def test_type_attribute_required(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
            ["Record-Name", "Record", [], "", [
                [1, "id", "String-Test", ["[1"], ""],
                [2, "info_1", "String", [], ""],
                [2, "info_2", "String", [], ""]
            ]],
            ["String-Test", "String", ["/attr"], "", []]
        ]
    }    

    # Step 2: Convert JADN to XSD
    builder = XSDBuilder()
    xsd_tuple = builder.convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)   

    valid_xml = """<Record-Name id="123">
        <info_1>Test</info_1>
        <info_2>True</info_2>
    </Record-Name>"""           
    
    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, valid_xml)
    assert valid is True    
    
    valid_xml = """<Record-Name>
        <info_1>Test</info_1>
        <info_2>True</info_2>
    </Record-Name>"""
    
    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, valid_xml)
    assert valid is False      