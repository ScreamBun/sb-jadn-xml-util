from setuptools import setup, find_packages
 
setup(
    name="jadn-xml",
    version="1.0", 
    packages=["jadnxml", "jadnxml.builder", "jadnxml.constants", "jadnxml.utils", "jadnxml.validation"],
    install_requires=[
        "numpy>=1.20,<1.22",
        "pandas>=1.3",
        "requests==2.25.1",
        "dicttoxml==1.7.16",
        "html-to-json==2.0.0",
        "jadn==0.6.18",
        "lxml==4.9.2",
        "Markdown==3.4.1",
        "markdown-to-json==1.0.0",
        "xmltodict==0.13.0"
    ]    
)