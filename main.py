import glob
import os
import sys

from jadnxml.builder.xsd_builder import convert_to_xsd_from_file
from jadnxml.utils.utils import get_after_last_occurance, get_filename_from_path
from jadnxml.validation.validation_manager import validate_xml


if __name__=="__main__":
    
    print("Pick your script (1 or 2): ")
    print("1: JADN XSD Converter")
    print("2: XML Validator")
    program_input = input()
    # program_input = "1"
    
    if program_input == "1":
        print("Converting JADN Schemas found under _data/schemas...")
        
        # Path to schemas
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        path = file_dir + "/_data/schemas/"
        files_to_convert = []
        
        for path_to_file in glob.glob(path + '*.jadn'):
            file = get_filename_from_path(path_to_file)
            files_to_convert.append(file)     
            
        for path_to_file in glob.glob(path + '*.json'):
            file = get_filename_from_path(path_to_file)
            files_to_convert.append(file)                 
        
        for filename in files_to_convert:
            print(f"Converting {filename} to a JADN XSD... ")
            convert_to_xsd_from_file(filename)
            print(f"Converion complete for {filename}, see the _data/out directory to view the results")

        if len(files_to_convert) == 0:
            print("Unable to find JADN or JSON files to convert to XSD files.")
            
    elif program_input == "2":
        print("Validating XML ...")
        
        if(len(sys.argv) == 3):

            xsd = sys.argv[1].strip()
            print("xsd: " + xsd)

            xml = sys.argv[2].strip()
            print("xml: " + xml)

            xsd_file_extension = get_after_last_occurance(".", xsd)
            xml_file_extension = get_after_last_occurance(".", xml)

            if(xsd_file_extension != "xsd"):
                raise "invalid file extension, must be .xsd"
            
            if(xml_file_extension != "xml"):
                raise "invalid file extension, must be .xml"        

            validate_xml(xsd, xml)
            
            print("Validation Complete")
        else:
            validate_xml('note.xsd', 'note.xml')
            
            print("Validation Complete")
    else:
        print("Invalid entry... ")

    
    