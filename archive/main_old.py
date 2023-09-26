from xml.dom.minidom import parseString
import jadn
import json
import markdown
import xmltodict
import dicttoxml
import html_to_json

from archive.files import Files


def xml_to_json():
    print("---- XML to JSON ----")   

    schema_fp = Files.get_schema_fullpath(Files.schema_xml_oc2ls_v101_fn) 
    with open(schema_fp) as xml_file:
        xml_dict = xmltodict.parse(xml_file.read())

    json_data = json.dumps(xml_dict, indent=4)  

    json_test_fp = Files.get_test_data_fullpath(Files.xml_to_json_fn) 
    with open(json_test_fp, "w") as json_file:
        json_file.write(json_data)    

    # print(json_data)
    print("---- JSON to XML > Complete ---- ")
  

def json_to_xml():
    print("---- XML to JSON ---- ")   

    schema_fp = Files.get_schema_fullpath(Files.schema_json_oc2ls_v101_fn) 
    with open(schema_fp) as json_file:
        dict_data = json.load(json_file)    

    xml_data = dicttoxml.dicttoxml(dict_data, attr_type = False)
    xml_data_formatted = parseString(xml_data).toprettyxml()
    xml_bytes = bytes(xml_data_formatted, 'utf-8')        

    xml_fp = Files.get_test_data_fullpath(Files.json_to_xml_fn) 
    with open(xml_fp, "wb") as f:
        f.write(xml_bytes)

    # print(xml_data_formatted)
    print("---- JSON to XML > Complete ---- ")


def jadn_to_json():
    print("---- JADN to JSON ---- ") 

    schema_fp = Files.get_schema_fullpath(Files.schema_jadn_oc2ls_v101_fn) 
    with open(schema_fp) as jadn_file:
        jadn_dict_data = json.load(jadn_file)

    json_object = json.dumps(jadn_dict_data, indent = 4) 

    json_out_fp = Files.get_test_data_fullpath(Files.jadn_to_json_fn) 
    with open(json_out_fp, "w") as json_file:
        json_file.write(json_object)    

    # print(json_object)
    print("---- JADN to JSON > Complete ---- ") 

def json_to_jadn():
    print("---- JSON to JADN ---- ")     

    schema_fp = Files.get_schema_fullpath(Files.schema_json_oc2ls_v101_fn) 
    with open(schema_fp) as json_file:
        dict_data = json.load(json_file)    

    json_out_fp = Files.get_test_data_fullpath(Files.json_to_jadn_fn) 
    jadn.dump(dict_data, json_out_fp)        

    # print(dict_data, indent=4)
    print("---- JSON to JADN > Complete ---- ") 


def xml_to_jadn():
    print("---- XML to JADN ---- ")   

    schema_xml_fp = Files.get_schema_fullpath(Files.schema_xml_oc2ls_v101_fn) 
    with open(schema_xml_fp) as xml_file:
        xml_dict = xmltodict.parse(xml_file.read())

    json_dict = json.dumps(xml_dict, indent=4)   

    jadn_out_fp = Files.get_test_data_fullpath(Files.xml_to_jadn_fn) 
    jadn.dump(json_dict, jadn_out_fp) 

    print("---- XML to JADN > Complete ---- ") 

def json_to_md():
    print("---- JSON to MD ---- ")  

    schema_fp = Files.get_schema_fullpath(Files.schema_json_oc2ls_v101_fn) 
    with open(schema_fp) as json_file:
        dict_data = json.load(json_file)   

    md_out_fp = Files.get_test_data_fullpath(Files.json_to_md_fn) 
    jadn.convert.markdown_dump(dict_data, md_out_fp)

    print("---- JSON to MD > Complete ---- ") 


def md_to_json():
    print("---- MD to JSON, not working well yet ---- ")  

    md_schema_fp = Files.get_schema_fullpath(Files.schema_md_oc2ls_v101_fn)  
    with open(md_schema_fp, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)

    output_json = html_to_json.convert(html)
    json_object = json.dumps(output_json, indent=4)

    json_out_fp = Files.get_test_data_fullpath(Files.md_to_json_fn) 
    with open(json_out_fp, "w") as json_file:
        json_file.write(json_object)        

    print("---- MD to JSON > Complete ---- ") 




if __name__=="__main__":
    # xml_to_json()
    # json_to_xml()
    jadn_to_json()
    # json_to_jadn()
    # xml_to_jadn()
    # json_to_md()
    # md_to_json()