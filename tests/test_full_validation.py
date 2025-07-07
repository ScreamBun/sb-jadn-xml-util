from jadnxml.builder.xml_builder import build_py_from_xml, build_xml_from_json
import xml.etree.ElementTree as ET
from jadnxml.builder.xml_builder import build_xml_from_json
from jadnxml.builder.xsd_builder import build_integer_type_opts, build_number_type_opts, build_string_type_opts, convert_to_xsd_from_file, convert_xsd_from_dict, get_jadn_base_types
from jadnxml.validation.validation_manager import validate_xml_str as validate
import os

def test_number_f32_format():
    file_name = "number_f32"

    # Step 1: Create JADN Schema
    jadn_schema = {
        "types": [
        ["NumberName", "Number", ["/f32"], ""],
        ["RecordName", "Record", [], "", [
            [1, "fieldvalue1", "NumberName", [], ""]
            ]]
        ]
    }

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_str = xsd_tuple[0]
    schema_et = xsd_tuple[1]

    os.makedirs("tests/tmp", exist_ok=True)

    with open(f"tests/tmp/{file_name}.xsd", "w") as f:
        f.write(xsd_str)

    # Step 3: Create test XML
    xml = """<TestFloat>
    <float>0.52</float>
</TestFloat>"""

    with open(f"tests/tmp/{file_name}.xml", "w") as f:
        f.write(xml)

    # Step 4: Valiate XML Against XSD
    valid = validate(f"{file_name}.xsd", f"{file_name}.xml")

    assert valid is True

def test_integer_formats():
    # Step 1: Create JADN Schema
    jadn_schema = {
        "types": [
        ["TestIntegers", "Record", [], "", [
            [1, "field1", "Number", ["/date-time"], ""],
            [2, "field2", "Number", ["/date"], ""],
            [3, "field3", "Number", ["/time"], ""],
            [4, "field4", "Number", ["/gYearMonth"], ""],
            [5, "field5", "Number", ["/gYear"], ""],
            [6, "field6", "Number", ["/gMonthDay"], ""]
        ]]
        ]
    }

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_str = xsd_tuple[0]
    schema_et = xsd_tuple[1]

    os.makedirs("tests/tmp", exist_ok=True)

    with open("tests/tmp/integer.xsd", "w") as f:
        f.write(xsd_str)

    # Step 3: Create test XML
    xml = """<TestIntegers>
    <integer>423123</integer>
    <integer>123</integer>
    <integer>456</integer>
    <integer>1011</integer>
    <integer>2025</integer>
    <integer>1230</integer>
</TestIntegers>"""

    with open("tests/tmp/integer.xml", "w") as f:
        f.write(xml)

    # Step 4: Valiate XML Against XSD
    valid = validate("integer.xsd", "integer.xml")

    assert valid is True