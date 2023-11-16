import glob
import os
from logic.builder.xsd_builder import create_jadn_xsd
from utils.utils import get_filename_from_path


if __name__=="__main__":
    # if(len(sys.argv) == 3):

    #     xsd = sys.argv[1].strip()
    #     print("xsd: " + xsd)

    #     xml = sys.argv[2].strip()
    #     print("xml: " + xml)

    #     xsd_file_extension = get_after_last_occurance(".", xsd)
    #     xml_file_extension = get_after_last_occurance(".", xml)

    #     if(xsd_file_extension != "xsd"):
    #         raise "invalid file extension, must be .xsd"
        
    #     if(xml_file_extension != "xml"):
    #         raise "invalid file extension, must be .xml"        

    #     validate_xml(xsd, xml)
    # else:
    #     validate_xml('students.xsd', 'students.xml')

    print("Pick your script (1 or 2): ")
    print("1: JADN XSD Converter")
    print("2: XML Validator")
    # program_input = input()
    program_input = "1"
    
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
            create_jadn_xsd(filename)
            print(f"Converion complete for {filename}, see the _data/out directory to view the results")

        if len(files_to_convert) == 0:
            print("Unable to find JADN or JSON files to convert to XSD files.")
            
    elif program_input == "2":
        # TODO call validator logic with XSD and XML
        test = "test"
    else:
        print("Invalid entry... ")

    
    