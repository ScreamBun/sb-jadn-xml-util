from xml.etree import ElementTree as ET
ET.register_namespace('com',"http://www.company.com") #some name

# build a tree structure
root = ET.Element("{http://www.company.com}STUFF")
body = ET.SubElement(root, "{http://www.company.com}MORE_STUFF")
body.text = "STUFF EVERYWHERE!"

# wrap it in an ElementTree instance, and save as XML
tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)

tree.write("./out/page.xml",
           xml_declaration=True,encoding='utf-8',
           method="xml")