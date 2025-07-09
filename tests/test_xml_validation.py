from jadnxml.builder.xsd_builder import convert_xsd_from_dict
from jadnxml.validation.validation_manager import validate_xml_str as validate
from jadnxml.utils.utils import generate_xsd_template
  

def test_number(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Number", [], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>1.55</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True

def test_number_2():
    xsd_string = generate_xsd_template("decimal")
    xml_str = """<decimal>0.52</decimal>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_number_f32(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Number", ["/f32"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>1.55</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>zero</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_number_f32_2():
    xsd_string = generate_xsd_template("decimal", "float")
    xml_str = """<decimal>0.52</decimal>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_number_f64(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Number", ["/f64"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>1.55</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>zero</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_number_f64_2():
    xsd_string = generate_xsd_template("decimal", "double")
    xml_str = """<decimal>0.52</decimal>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "String", [], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>Test</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True

def test_string_2():
    xsd_string = generate_xsd_template("string", "")
    xml_str = """<string>Test</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string_date_time(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "String", ["/date-time"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>2025-07-07T15:00:00Z</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>2025-07-07</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_string_date_time_2():
    xsd_string = generate_xsd_template("string", "dateTime")
    xml_str = """<string>2025-07-07T15:00:00Z</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string_date(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "String", ["/date"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>2025-07-07</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>2025-07</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_string_date_2():
    xsd_string = generate_xsd_template("string", "date")
    xml_str = """<string>2025-07-07</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_string_time(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "String", ["/time"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>15:00:00</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>12341</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_string_time_2():
    xsd_string = generate_xsd_template("string", "time")
    xml_str = """<string>15:00:00Z</string>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_integer(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", [], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>15</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True

def test_integer_2():
    xsd_string = generate_xsd_template("integer")
    xml_str = """<integer>15</integer>"""
    invalid_xml_str = """<integer>15.99</integer>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_str)
    assert valid is False

def test_integer_date_time(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/date-time"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>1751677200</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>P3DT4H30M15S</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_date(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/date"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>1751677200</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>2024-11</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_time(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/time"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>1751677200</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>15S</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_g_year_month(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/gYearMonth"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>2024-11</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>11-2024</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_g_year(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/gYear"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>2023</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>24</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_g_month_day(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/gMonthDay"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>--07-08</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>07-08</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_duration(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/duration"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>P0Y0M0DT1H20M30S</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>Test</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_day_time_duration(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/dayTimeDuration"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>P3DT4H30M15S</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>P3DT4</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_year_month_duration(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/yearMonthDuration"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>P2Y6M</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>6M</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_i64(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/i64"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>9223372036854775807</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>9223372036854775808</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_i32(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/i32"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>2147483647</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>2147483648</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_i16(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/i16"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>32767</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>32768</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_i8(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/i8"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>127</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>128</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_u64(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/u64"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>18446744073709551615</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>18446744073709551616</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_u64_2():
    xsd_string = generate_xsd_template("integer", "unsignedLong")
    xml_str = """<integer>18446744073709551615</integer>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_integer_u32(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/u32"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>4294967295</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>14294967296</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_u32_2():
    xsd_string = generate_xsd_template("integer", "unsignedInt")
    xml_str = """<integer>4294967295</integer>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_integer_u16(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/u16"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>65535</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>65536</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_u16_2():
    xsd_string = generate_xsd_template("integer", "unsignedShort")
    xml_str = """<integer>65535</integer>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_integer_u8(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/u8"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>255</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>256</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_u8_2():
    xsd_string = generate_xsd_template("integer", "unsignedByte")
    xml_str = """<integer>255</integer>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_integer_non_negative(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/nonNegativeInteger"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>0</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>-1</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_negative(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/negativeInteger"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>-1</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>0</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_non_positive(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/nonPositiveInteger"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>0</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>1</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_integer_positive(): 
   # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Integer", ["/positiveInteger"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)
    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>1</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>0</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_boolean(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Boolean", [], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>false</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True

def test_boolean_2():
    xsd_string = generate_xsd_template("boolean")
    xml_str = """<boolean>true</boolean>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Binary", [], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>0101</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>01P</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_binary_2():
    xsd_string = generate_xsd_template("byte")
    xml_str = """<byte>0101</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary_base64(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Binary", ["/b64"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>ABCD</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>ABC</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False

def test_binary_base64_2():
    xsd_string = generate_xsd_template("byte", "base64Binary")
    xml_str = """<byte>ABCD</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary_hex(): 
    # Step 1: Create JADN Schema
    jadn_schema = {
    "meta": {
        "package": "http://test/v1.0",
        "roots": ["Record-Name"]
    },
    "types": [
        ["Record-Name", "Record", [], "", [
            [1, "field_value_1", "Binary", ["/x"], ""]
        ]]
    ]
    }    

    # Step 2: Convert JADN to XSD
    xsd_tuple = convert_xsd_from_dict(jadn_schema)
    xsd_string = xsd_tuple[0]
    print(xsd_string)

    # Step 3: Create test XML
    xml_string = """<Record-Name>
        <field_value_1>abcd</field_value_1>
    </Record-Name>"""   

    invalid_xml_string = """<Record-Name>
        <field_value_1>abcz/</field_value_1>
    </Record-Name>"""   

    # Step 4: Valiate XML Against XSD
    valid = validate(xsd_string, xml_string)
    assert valid is True
    valid = validate(xsd_string, invalid_xml_string)
    assert valid is False
def test_binary_hex_2():
    xsd_string = generate_xsd_template("byte", "hexBinary")
    xml_str = """<byte>1ABC</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True

def test_binary_eui():
    xsd_string = generate_xsd_template("byte", "hexBinary")
    xml_str = """<byte>1ABC</byte>"""
    valid = validate(xsd_string, xml_str)
    assert valid is True