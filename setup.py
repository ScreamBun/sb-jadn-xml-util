from setuptools import setup, find_packages
 
setup(
    data_files=[('jadn_base_types', ['_data/xsd/jadn_base_types.xsd'])],
    name="jadnxml",
    version="1.10.0", 
    packages=["jadnxml", "jadnxml.builder", "jadnxml.constants", "jadnxml.helpers", "jadnxml.utils", "jadnxml.validation"],
    install_requires=[
        "dict2xml",
        "lxml",
        "xmltodict"
    ]    
)