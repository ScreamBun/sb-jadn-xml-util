from jadnxml.builder.xsd_builder import convert_xsd_from_dict
from jadnxml.validation.validation_manager import validate_xml_str as validate

def test_number_f32():
    # Step 1: Create JADN Schema
    jadn_schema = {
        "types": [
        ["Number-Name", "Number", ["/f32"], ""],
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Number-Name", [], ""]
            ]]
        ]
    }

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_str = xsd_tuple[0]
    print(xsd_str)

    # Step 3: Create test XML
    xml_str = """<TestFloat>
    <float>0.52</float>
</TestFloat>"""

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_str, xml_str)
    assert valid is True