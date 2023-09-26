import sys
from builder_logic.xsd_manager import create_music_lib
from utils.utils import get_after_last_occurance
from validation_logic.validation_manager import validate_xml


if __name__=="__main__":

    # create_customer_order()
    # create_customer_order2()
    # create_customer_order3()
    # create_dict_to_xml()

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
    else:
        validate_xml('students.xsd', 'students.xml')

    # create_music_lib()
    
    