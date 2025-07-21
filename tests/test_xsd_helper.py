import xml.etree.ElementTree as ET

from lxml import etree
from jadnxml.helpers.xsd_helper import build_attrs, is_field_optional, split_types_by_attr


def test_split_types_by_attr():
    """
    Splits types into those with '/attr' in their options and those without.
    Sets self.jadn_types_dict to types without '/attr' and self.ref_attrs to types with '/attr'.
    Returns (types_without_attr, types_with_attr)
    """
    
    types_list = [
        ["Record-Name", "Record", [], "", [
            [1, "id_a", "ID", [], ""],
            [2, "info_1", "String", [], ""],
            [2, "info_2", "String", [], ""]
        ]],
        ["Another-Record", "Record", [], "", [
            [1, "id_b", "String", ["/attr"], ""],
            [2, "info_1", "String", [], ""]
        ]],
        ["ID", "String", ["/attr"], "", []]        
    ]
    
    split_types = split_types_by_attr(types_list)
    jadn_types_dict = split_types[0]
    jadn_ref_attrs = split_types[1]

    assert len(jadn_types_dict) == 2
    assert len(jadn_ref_attrs) == 1
    

def test_build_attrs():
    """
    Tests the build_attrs function to ensure it correctly adds attributes to the XSD element.
    """
    
    # Mocking an XML Element
    root = ET.Element("root")
    
    # Mocking a JADN type with attributes
    jce = {
        "type_name": "TestType",
        "fields": [
            [1, "id", "id", ["/attr"], "Identifier"],
            [2, "info_1", "String", ["/attr"], "Information 1"]
        ],
        "description": "Test Type Description"
    }
    
    # Mocking reference attributes
    jadn_ref_attrs = ["id"]
    
    # Call the function
    build_attrs(root, jce, jadn_ref_attrs)
    
    ET.indent(root, space="\t", level=0)
    xml_str = ET.tostring(root, encoding='unicode')
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True, encoding='unicode')    
    
    print(xml_str)
    
    nsmap = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    # Check if attributes are added correctly
    assert len(root.findall(".//xs:attribute", namespaces=nsmap)) == 2
    attrib_el = root.find(".//xs:attribute[@name='id']", namespaces=nsmap)
    assert attrib_el is not None
    assert attrib_el.attrib['type'] == 'xs:string'
    
def test_is_field_optional():
    """
    Tests the is_field_optional function to ensure it correctly identifies optional fields.
    """
    
    # Mocking a JADN field with options indicating it's optional
    j_field = [1, "id", "String", ["[0"], ""]
    
    # Call the function
    is_optional = is_field_optional(j_field)
    
    # Assert that the field is identified as optional
    assert is_optional is True
    
    # Mocking a JADN field without options indicating it's required
    j_field = [2, "info_1", "String", [], ""]
    
    # Call the function again
    is_optional = is_field_optional(j_field)
    
    # Assert that the field is not identified as optional
    assert is_optional is False     