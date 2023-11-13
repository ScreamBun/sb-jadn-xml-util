from logic.builder.xsd_builder import create_jadn_xsd


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
    program_input = input()
    
    if program_input == "1":
        print("What's the JADN filename?")
        filename_input = input()
        
        if filename_input:
            print("Building the JADN XSD... ")
            create_jadn_xsd(filename_input)
        else:
            print("Invalid entry... ")
            
    elif program_input == "2":
        # TOD something else
        test = "test"
    else:
        print("Invalid entry... ")

    
    