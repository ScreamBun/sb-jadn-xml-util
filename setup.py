from setuptools import setup, find_packages
 
setup(
    name="jadn-xml",
    version="1.2", 
    packages=["jadnxml", "jadnxml.builder", "jadnxml.constants", "jadnxml.helpers", "jadnxml.utils", "jadnxml.validation"],
    install_requires=[
        "requests",
        "dicttoxml",
        "html-to-json",
        "lxml",
        "Markdown",
        "markdown-to-json",
        "xmltodict"
    ]    
)