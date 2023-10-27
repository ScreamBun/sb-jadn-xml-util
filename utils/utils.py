from datetime import date, timedelta
import json
import os
from lxml import etree
import xml.etree.ElementTree as ET


def convert_str_to_int(str_val: str):
  return_int: int = 0
  try:
      return_int = int(str_val)
  except ValueError:
      print(f'unable to convert str ${str_val} to int')  
  return return_int


def get_after_last_occurance(char: str, value: str):
    str_split = value.rsplit(char, 1)
    after_last = str_split[-1]
    return after_last


def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default
  

def add_days_to_date(date_val: date, days_to_add: int):
    return_date = date_val + timedelta(days=days_to_add)
    return return_date


def get_xml_file(file_name):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    print(file_dir)
    xml_file_path = os.path.join(file_dir, './_data/xml/' + file_name)
    xml_file_path = os.path.abspath(os.path.realpath(xml_file_path))  

    doc = etree.parse(xml_file_path)    

    return doc


def get_xsd_file(file_name):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    print(file_dir)
    xsd_file_path = os.path.join(file_dir, './_data/xsd/' + file_name)
    xsd_file_path = os.path.abspath(os.path.realpath(xsd_file_path))   

    with open(xsd_file_path, 'r') as f:
        xmlschema_doc = etree.parse(f)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    return xmlschema


def read_file(file_name):
  with open(file_name, 'r') as f:
      data = f.read()

  return data;


def write_to_file(root: ET.Element, filename: str):
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)

    tree.write("./_out/" + filename,
              xml_declaration=True,encoding='utf-8',
              method="xml")    
    
def read_type_data_from_file(filename):
  f = open('./_data/schemas/' + filename) 
  data = json.load(f)
 
  f.close()

  return data