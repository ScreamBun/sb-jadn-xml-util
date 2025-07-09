from datetime import date, timedelta
import json
import os
import pathlib
import re
from lxml import etree
import xml.etree.ElementTree as ET
import xmltodict

def convert_str_to_int(str_val: str):
  return_int: int = 0
  try:
      return_int = int(str_val)
  except ValueError:
      print(f'unable to convert str ${str_val} to int')  
  return return_int


def find_first_list(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for value in data.values():
            result = find_first_list(value)
            if result is not None:
                return result
    return None

def find_items_by_val(dictionary: dict, search_string: str):
    return {key:val for key,val in dictionary.items() if any(search_string in s for s in val)}


def get_after_last_occurance(char: str, value: str):
    str_split = value.rsplit(char, 1)
    after_last = str_split[-1]
    return after_last

def get_base_type_and_schema_type(schema: dict, root: str):
    base_type = None
    schema_type = None
    
    if schema and root:    
        types = schema.get('types')
        if types == None or types == []:
            raise ValueError(f"No Types defined")
        
        for type in types:
            if type[0] == root:
                base_type = type[1]
                schema_type = type
                break
    
    if base_type == None:
        raise ValueError(f"Root Type not found {root}")
    if schema_type == None:
        raise ValueError(f"Schema Type not found for {root}")
    
    return base_type, schema_type

def get_file_extension_only(file_name: str):
    file_extension = pathlib.Path(file_name).suffix    
    return file_extension


def get_file_name_only(file_name: str):
    file_name_only = pathlib.Path(file_name).stem    
    return file_name_only

def get_list_from_xml_data(xml_str: str):
    data_list = None
    if xml_str:
        data_dict = xmltodict.parse(xml_str, xml_attribs=False)
        data_list = find_first_list(data_dict)    
        
    return data_list

def get_dict_from_xml_data(xml_str: str, root_tag: str, use_id_as_key: bool = False):
    data_dict = {}
    dict_to_parse = xmltodict.parse(xml_str, xml_attribs=use_id_as_key)
    root_dict = dict_to_parse.get(root_tag)
    
    if root_dict:
        if use_id_as_key:            
            for index, (root_data_value) in enumerate(root_dict.values()):
                actual_key = None
                actual_val = None 
                
                if isinstance(root_data_value, dict): 
                    
                    if root_data_value.get("@key") or root_data_value.get("@id"):
                         
                        for index, (attr_key, attr_value) in enumerate(root_data_value.items()):
                            
                            if attr_key == "@key" or attr_key == "@id":
                                actual_key = attr_value
                            elif attr_key == "#text":
                                actual_val = attr_value
                                
                            if actual_val and actual_key:
                                break
                            
                    else:
                        raise ValueError(f"Unable to locate key or id in xml")
                        
                else:
                    raise ValueError(f"Unable to locate key or id in xml")
                        
                if actual_key and actual_val: 
                    data_dict[actual_key] = actual_val
                
        elif not use_id_as_key:
            data_dict = root_dict 
         
    return data_dict


def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

def use_id_as_key(root):
    options = safe_list_get(root, 2, None)
    if options and "=" in options:
        return True
    else:
        return False

def add_days_to_date(date_val: date, days_to_add: int):
    return_date = date_val + timedelta(days=days_to_add)
    return return_date


def get_filename_from_path(path: str):
    return os.path.basename(path).split('/')[-1]    


def get_xml_file(file_name):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    # print(file_dir)
    xml_file_path = os.path.join(file_dir, './_data/xml/' + file_name)
    xml_file_path = os.path.abspath(os.path.realpath(xml_file_path))  

    doc = etree.parse(xml_file_path)    

    return doc


def get_xsd_file(file_name, isParseToET: bool = False):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    # print(file_dir)
    xsd_file_path = os.path.join(file_dir, '_data/xsd/' + file_name)
    xsd_file_path = os.path.abspath(os.path.realpath(xsd_file_path))   

    if isParseToET:
        with open(xsd_file_path, 'r') as f:
            xmlschema_doc = etree.parse(f)
        xmlschema = etree.XMLSchema(xmlschema_doc)
    else:
        with open(xsd_file_path, 'r') as f:
            xmlschema = f.read()    

    return xmlschema

def remove_special_characters(string):
    return re.sub(r'[^a-zA-Z0-9-_]', '', string)


def read_file(file_name):
  with open(file_name, 'r') as f:
      data = f.read()

  return data;


def write_to_file(root: ET.Element, filename: str):
    tree = ET.ElementTree(root)
    # ET.indent(tree, space="\t", level=0)

    tree.write("./_out/" + filename,
              xml_declaration=True,encoding='utf-8',
              method="xml")    
    
    
def read_type_data_from_file(filename):
  f = open('./_data/schemas/' + filename) 
  data = json.load(f)
 
  f.close()

  return data

def generate_xsd_template(type, option=None):
    if not option:
        return f"""
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <xs:element name="{type}" type="xs:{type}"/>
    </xs:schema>
    """
    else:
        return f"""
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <xs:element name="{type}" type="xs:{option}"/>
    </xs:schema>
    """