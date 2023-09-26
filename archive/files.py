import os


class Files:

    schema_dir = "./test_data/schemas/"

    schema_jadn_th_fn = "device-th-base-resolved.jadn"
    schema_jadn_oc2ls_v101_fn = "oc2ls-v1.0.1-resolved.jadn"
    schema_json_oc2ls_v101_fn = "oc2ls-v1.0.1-resolved.json"
    schema_md_oc2ls_v101_fn = "oc2ls-v1.0.1-resolved.md"
    schema_xml_oc2ls_v101_fn = "oc2ls-v1.0.1-resolved.xml"
    schema_jadn_oc2ls_v11_fn = "oc2ls-v1.1-lang_resolved.jadn"

    md_to_json_fn = "md_to_json.json"
    jadn_to_json_fn = "jadn_to_json.json"
    json_to_jadn_fn = "json_to_jadn.jadn"
    json_to_md_fn = "json_to_md.md"
    json_to_xml_fn = "json_to_xml.xml"
    xml_to_jadn_fn = "xml_to_jadn.jadn"
    xml_to_json_fn = "xml_to_json.json"    

    def get_test_data_dir() -> str:
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_data')

    def get_schema_data_dir() -> str:
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_data/schemas')

    def get_schema_fullpath(fn: str) -> str:
        dir = Files.get_schema_data_dir()
        return os.path.join(dir, fn)    

    def get_test_data_fullpath(fn: str) -> str:
        dir = Files.get_test_data_dir()
        return os.path.join(dir, fn)               