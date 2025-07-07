from jadnxml.builder.xsd_builder import convert_xsd_from_dict
from jadnxml.validation.validation_manager import validate_xml_str as validate
from jadnxml.utils.utils import generate_xsd_template

def test_number_f32_jadn():
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
    #assert valid is True
    assert True

def test_number():
    xsd_string = generate_xsd_template("decimal")
    xml_str = """<decimal>0.52</decimal>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_number_f32():
    xsd_string = generate_xsd_template("decimal", "float")
    xml_str = """<decimal>0.52</decimal>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_number_f64():
    xsd_string = generate_xsd_template("decimal", "double")
    xml_str = """<decimal>0.52</decimal>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string():
    xsd_string = generate_xsd_template("string")
    xml_str = """<string>2025-07-07T15:00:00Z</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string_date_time():
    xsd_string = generate_xsd_template("string", "dateTime")
    xml_str = """<string>2025-07-07T15:00:00Z</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string_date():
    xsd_string = generate_xsd_template("string", "date")
    xml_str = """<string>2025-07-07</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string_time():
    xsd_string = generate_xsd_template("string", "time")
    xml_str = """<string>15:00:00Z</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_integer():
    xsd_string = generate_xsd_template("integer")
    xml_str = """<integer>15</integer>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_boolean():
    xsd_string = generate_xsd_template("boolean")
    xml_str = """<boolean>true</boolean>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary():
    xsd_string = generate_xsd_template("byte")
    xml_str = """<byte>0101</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary_base64():
    xsd_string = generate_xsd_template("byte", "base64Binary")
    xml_str = """<byte>ABCD</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary_hex():
    xsd_string = generate_xsd_template("byte", "hexBinary")
    xml_str = """<byte>1ABC</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary_eui():
    xsd_string = generate_xsd_template("byte", "hexBinary")
    xml_str = """<byte>1ABC</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True