import xml.etree.ElementTree as ET
from builder_logic.jadn_constants import BASE_TYPE, FIELDS, OPTION_KEYS, TYPE_DESCRIPTION, TYPE_NAME, TYPE_OPTIONS
from builder_logic.options_helper import get_jadn_option, opt_list_2_dict

from builder_logic.xsd_constants import *
from utils.utils import *
from builder_logic.xsd_helper import *


def get_common_elements(type: []):
    print("Building common elements")
    common_elements = {} 
    common_elements[TYPE_NAME] = safe_list_get(type, 0, None)
    common_elements[BASE_TYPE] = safe_list_get(type, 1, None)
    common_elements[TYPE_OPTIONS] = safe_list_get(type, 2, None)
    common_elements[TYPE_DESCRIPTION] = safe_list_get(type, 3, None)
    common_elements[FIELDS] = safe_list_get(type, 4, None)
    return common_elements


def build_base_types(root: ET.Element):
    print(f"Building Primitive Simple Types")

    for prim_key, prim_value in primitives.items():
      BASE_TYPE = build_simple_type(root, prim_key)  
      restriction = build_restriction(BASE_TYPE, prim_value)    


def build_primitive_type(root: ET.Element, type: []):
    print(f"Building Primitive Type: {type[1]}")
    jce = get_common_elements(type)

    simple_type = build_simple_type(root, jce.get(TYPE_NAME))

    if jce.get(TYPE_DESCRIPTION):
      build_documention(simple_type, jce.get(TYPE_DESCRIPTION))

    restriction = build_restriction(simple_type, primitives.get(type[1]))

    if jce[TYPE_OPTIONS]:
      jadn_options_dict = get_jadn_option(jce[TYPE_OPTIONS])
      for key, option in jadn_options_dict.items():
        print(f"Option added {key} {option}")
        if key == OPTION_KEYS["regex"]:     
          string_restriction_pattern = build_pattern(restriction, option)          


def build_enumeration_type(root: ET.Element, type: []):
    print("Building Enumeration Type")
    jce = get_common_elements(type)

    xsd_simple_type = build_simple_type(root, jce[TYPE_NAME])

    if jce[TYPE_DESCRIPTION]:
      build_documention(xsd_simple_type, jce[TYPE_DESCRIPTION])

    xsd_restriction = build_restriction(xsd_simple_type, xs_token)

    if jce[FIELDS]:
      FIELDS_arr =jce[FIELDS]
      count = len(FIELDS_arr)
      if count > 0:
        for field in FIELDS_arr:
          field_value = field[1]
          xsd_enum = build_enumeration(xsd_restriction, field_value)


def build_specialization_type(root: ET.Element, type: []):
    print("Building Specialization (Choice) Type")
    jce = get_common_elements(type)
    # TODO: Add logic for choice



def build_structure_type(root: ET.Element, type: []):
    print("Building Structure Types")

    jce = get_common_elements(type)

    # TODO: Add logic for ArrayOf


    # TODO: Add logic for MapOf
    # if jce.get(BASE_TYPE) == "MapOf":
    #   print("Building MapOf Type")
    #   xsd_array_of_complex_type = build_complex_type(root, jce[TYPE_NAME])

    #   if jce.get(TYPE_DESCRIPTION):
    #     build_documention(xsd_array_of_complex_type, jce.get(TYPE_DESCRIPTION))
        
    
    # TODO: Add logic for Array
    # TODO: Add logic for Map    

    if jce.get(BASE_TYPE) == "Record":
      print("Building Record Type")
      
      # xsd_element = build_element(root, jce[TYPE_NAME])
      xsd_complex_type = build_complex_type(root, jce[TYPE_NAME])
      xsd_seq = build_sequence(xsd_complex_type)
      
      for field in jce[FIELDS]:
        field_index = field[0]
        field_name = field[1]
        field_type = field[2]
        field_opts = field[3]
        field_desc = field[4]
        
        if field_type == "ArrayOf":
          field_type = get_vtype(field_opts)
          
        xsd_elem = build_element(xsd_seq, field_name, field_type)      
      
      
      # xsd_complex_type = build_complex_type(root, jce[TYPE_NAME])

      # if jce.get(TYPE_DESCRIPTION):
      #   build_documention(xsd_complex_type, jce.get(TYPE_DESCRIPTION))

      # xsd_seq = build_sequence(xsd_complex_type)
      # for elem in type[4]:
      #   xsd_elems = build_element(xsd_seq, elem)

      # restriction = add_restriction(xsd_complex_type, xs_string) # TODO..        
      
      
def build_types(root : ET.Element, jadn_types_dict: dict):
    for jadn_type in jadn_types_dict:
      jadn_type_name = jadn_type[1]

      simple_jadn_type = primitives.get(jadn_type_name, None)
      if simple_jadn_type != None:
        build_primitive_type(root, jadn_type)

      enumeration_jadn_type = enumerations.get(jadn_type_name, None)
      if enumeration_jadn_type != None:
        build_enumeration_type(root, jadn_type)

      # Choice
      specialization_jadn_type = specializations.get(jadn_type_name, None)
      if specialization_jadn_type != None:
        build_specialization_type(root, jadn_type)

      structures_jadn_type = structures.get(jadn_type_name, None)
      if structures_jadn_type != None:
        build_structure_type(root, jadn_type) 
  

def build_global_elements(root : ET.Element, jadn_exports):
  for export in jadn_exports:
    build_element(root, export, export)


def create_jadn_xsd():
    root = ET.Element(schema_tag)
    jadn_dict = read_type_data_from_file("music_lib.jadn.json")
    jadn_info= jadn_dict['info']
    jadn_exports = jadn_info['exports']
    jadn_types = jadn_dict['types']

    build_global_elements(root, jadn_exports)
    build_base_types(root)
    build_types(root, jadn_types)     
      
    write_to_file(root, "music_lib.xsd")

    root = ET.Element(schema_tag)
    content1a = ET.SubElement(root, element_tag, name='shiporder')
    content2a = ET.SubElement(content1a, complexType_tag)
    content3a = ET.SubElement(content2a, sequence_tag)
    
    content4a = ET.SubElement(content3a, element_tag, name="orderperson", type=xs_string)
    
    content5a = ET.SubElement(content3a, element_tag, name="shipto")
    content6b = ET.SubElement(content5a, complexType_tag)
    content7a = ET.SubElement(content6b, sequence_tag)
    content8a = ET.SubElement(content7a, element_tag, name="name", type=xs_string)
    content8b = ET.SubElement(content7a, element_tag, name="address", type=xs_string)
    content8c = ET.SubElement(content7a, element_tag, name="city", type=xs_string)
    content8d = ET.SubElement(content7a, element_tag, name="country", type=xs_string)

    content9a = ET.SubElement(content3a, element_tag, name="item", maxOccurs="unbounded")
    content10a = ET.SubElement(content9a, complexType_tag)
    content11a = ET.SubElement(content10a, sequence_tag)
    content12a = ET.SubElement(content11a, element_tag, name="title", type=xs_string)
    content12b = ET.SubElement(content11a, element_tag, name="note", type=xs_string, minOccurs="0")
    content12c = ET.SubElement(content11a, element_tag, name="quantity", type=xs_positiveInteger)
    content12d = ET.SubElement(content11a, element_tag, name="price", type=xs_decimal)

    content13a = ET.SubElement(content2a, attribute_tag, name="orderid", type=xs_string, use="required")

    write_to_file(root, 'exp_shiporder.xsd')

def create_dict_to_xml():
    a = {
        "info": {
            "package": "http://oasis-open.org/openc2/oc2ls/v1.1",
            "title": "OpenC2 Language Profile",
            "description": "Language Profile from the OpenC2 Language Specification version 1.1",
            "exports": ["OpenC2-Command", "OpenC2-Response"]
        },
        "types": [
            ["OpenC2-Command", "Record", [], "The Command defines an Action to be performed on a Target", [
                [1, "action", "Action", [], "The task or activity to be performed (i.e., the 'verb')."],
                [2, "target", "Target", [], "The object of the Action. The Action is performed on the Target."],
                [3, "args", "Args", ["[0"], "Additional information that applies to the Command."],
                [4, "actuator", "Actuator", ["[0"], "The subject of the Action. The Actuator executes the Action on the Target."],
                [5, "command_id", "Command-ID", ["[0"], "An identifier of this Command."]
                ]
            ]
        ]        
    }

    b = {
  "info": {
    "package": "http://oasis-open.org/openc2/oc2ls/v1.1",
    "title": "OpenC2 Language Profile",
    "description": "Language Profile from the OpenC2 Language Specification version 1.1",
    "exports": ["OpenC2-Command", "OpenC2-Response"]
  },
  "types": [
    ["OpenC2-Command", "Record", [], "The Command defines an Action to be performed on a Target", [
        [1, "action", "Action", [], "The task or activity to be performed (i.e., the 'verb')."],
        [2, "target", "Target", [], "The object of the Action. The Action is performed on the Target."],
        [3, "args", "Args", ["[0"], "Additional information that applies to the Command."],
        [4, "actuator", "Actuator", ["[0"], "The subject of the Action. The Actuator executes the Action on the Target."],
        [5, "command_id", "Command-ID", ["[0"], "An identifier of this Command."]
      ]],
    ["OpenC2-Response", "Record", [], "", [
        [1, "status", "Status-Code", [], "An integer status code."],
        [2, "status_text", "String", ["[0"], "A free-form human-readable description of the Response status."],
        [3, "results", "Results", ["[0"], "Map of key:value pairs that contain additional results based on the invoking Command."]
      ]],
    ["Action", "Enumerated", [], "", [
        [1, "scan", "Systematic examination of some aspect of the entity or its environment."],
        [2, "locate", "Find an object physically, logically, functionally, or by organization."],
        [3, "query", "Initiate a request for information."],
        [6, "deny", "Prevent a certain event or action from completion, such as preventing a flow from reaching a destination or preventing access."],
        [7, "contain", "Isolate a file, process, or entity so that it cannot modify or access assets or processes."],
        [8, "allow", "Permit access to or execution of a Target."],
        [9, "start", "Initiate a process, application, system, or activity."],
        [10, "stop", "Halt a system or end an activity."],
        [11, "restart", "Stop then start a system or an activity."],
        [14, "cancel", "Invalidate a previously issued Action."],
        [15, "set", "Change a value, configuration, or state of a managed entity."],
        [16, "update", "Instruct a component to retrieve, install, process, and operate in accordance with a software update, reconfiguration, or other update."],
        [18, "redirect", "Change the flow of traffic to a destination other than its original destination."],
        [19, "create", "Add a new entity of a known type (e.g., data, files, directories)."],
        [20, "delete", "Remove an entity (e.g., data, files, flows)."],
        [22, "detonate", "Execute and observe the behavior of a Target (e.g., file, hyperlink) in an isolated environment."],
        [23, "restore", "Return a system to a previously known state."],
        [28, "copy", "Duplicate an object, file, data flow, or artifact."],
        [30, "investigate", "Task the recipient to aggregate and report information as it pertains to a security event or incident."],
        [32, "remediate", "Task the recipient to eliminate a vulnerability or attack point."]
      ]],
    ["Target", "Choice", [], "", [
        [1, "artifact", "Artifact", [], "An array of bytes representing a file-like object or a link to that object."],
        [2, "command", "Command-ID", [], "A reference to a previously issued Command."],
        [3, "device", "Device", [], "The properties of a hardware device."],
        [7, "domain_name", "Domain-Name", [], "A network domain name."],
        [8, "email_addr", "Email-Addr", [], "A single email address."],
        [9, "features", "Features", [], "A set of items used with the query Action to determine an Actuator's capabilities."],
        [10, "file", "File", [], "Properties of a file."],
        [11, "idn_domain_name", "IDN-Domain-Name", [], "An internationalized domain name."],
        [12, "idn_email_addr", "IDN-Email-Addr", [], "A single internationalized email address."],
        [13, "ipv4_net", "IPv4-Net", [], "An IPv4 address range including CIDR prefix length."],
        [14, "ipv6_net", "IPv6-Net", [], "An IPv6 address range including prefix length."],
        [15, "ipv4_connection", "IPv4-Connection", [], "A 5-tuple of source and destination IPv4 address ranges, source and destination ports, and protocol."],
        [16, "ipv6_connection", "IPv6-Connection", [], "A 5-tuple of source and destination IPv6 address ranges, source and destination ports, and protocol."],
        [20, "iri", "IRI", [], "An internationalized resource identifier (IRI)."],
        [17, "mac_addr", "MAC-Addr", [], "A Media Access Control (MAC) address - EUI-48 or EUI-64 as defined in [EUI]."],
        [18, "process", "Process", [], "Common properties of an instance of a computer program as executed on an operating system."],
        [25, "properties", "Properties", [], "Data attribute associated with an Actuator."],
        [19, "uri", "URI", [], "A uniform resource identifier (URI)."]
      ]],
    ["Actuator", "Choice", [], ""],
    ["Args", "Map", ["{1"], "", [
        [1, "start_time", "Date-Time", ["[0"], "The specific date/time to initiate the Command"],
        [2, "stop_time", "Date-Time", ["[0"], "The specific date/time to terminate the Command"],
        [3, "duration", "Duration", ["[0"], "The length of time for an Command to be in effect"],
        [4, "response_requested", "Response-Type", ["[0"], "The type of Response required for the Command: none, ack, status, complete"]
      ]],
    ["Results", "Map", ["{1"], "Response Results", [
        [1, "versions", "Versions", ["[0"], "List of OpenC2 language versions supported by this Actuator"],
        [2, "profiles", "Profiles", ["[0"], "List of profiles supported by this Actuator"],
        [3, "pairs", "Action-Targets", ["[0"], "List of targets applicable to each supported Action"],
        [4, "rate_limit", "Number", ["y0.0", "[0"], "Maximum number of requests per minute supported by design or policy"],
        [5, "args", "Enumerated", ["#Args", "[0", "]0"], "List of supported Command Arguments"]
      ]],
    ["Action-Targets", "MapOf", ["*Targets", "+Action", "{1"], "Map of all actions to all targets"],
    ["Targets", "ArrayOf", ["*>Target", "{1", "}1", "q"], "List of all Target types"],
    ["Status-Code", "Enumerated", ["="], "", [
        [102, "Processing", "an interim Response used to inform the Producer that the Consumer has accepted the Command but has not yet completed it"],
        [200, "OK", "the Command has succeeded"],
        [201, "Created", "the Command has succeeded and a new resource has been created as a result of it"],
        [400, "Bad Request", "the Consumer cannot process the Command due to something that is perceived to be a Producer error (e.g., malformed Command syntax)"],
        [401, "Unauthorized", "the Command Message lacks valid authentication credentials for the target resource or authorization has been refused for the submitted credentials"],
        [403, "Forbidden", "the Consumer understood the Command but refuses to authorize it"],
        [404, "Not Found", "the Consumer has not found anything matching the Command"],
        [500, "Internal Error", "the Consumer encountered an unexpected condition that prevented it from performing the Command"],
        [501, "Not Implemented", "the Consumer does not support the functionality required to perform the Command"],
        [503, "Service Unavailable", "the Consumer is currently unable to perform the Command due to a temporary overloading or maintenance of the Consumer"]
      ]],
    ["Artifact", "Record", ["{1"], "", [
        [1, "mime_type", "String", ["[0"], "Permitted values specified in the IANA Media Types registry, [RFC6838]"],
        [2, "payload", "Payload", ["[0"], "Choice of literal content or URL"],
        [3, "hashes", "Hashes", ["[0"], "Hashes of the payload content"]
      ]],
    ["Device", "Map", ["{1"], "", [
        [1, "hostname", "Hostname", ["[0"], "A hostname that can be used to connect to this device over a network"],
        [2, "idn_hostname", "IDN-Hostname", ["[0"], "An internationalized hostname that can be used to connect to this device over a network"],
        [3, "device_id", "String", ["[0"], "An identifier that refers to this device within an inventory or management system"]
      ]],
    ["Domain-Name", "String", ["/hostname"], "[RFC1034], Section 3.5"],
    ["Email-Addr", "String", ["/email"], "Email address - [RFC5322], Section 3.4.1"],
    ["Features", "ArrayOf", ["*Feature", "}10", "q"], "An array of zero to ten names used to query an Actuator for its supported capabilities."],
    ["File", "Map", ["{1"], "", [
        [1, "name", "String", ["[0"], "The name of the file as defined in the file system"],
        [2, "path", "String", ["[0"], "The absolute path to the location of the file in the file system"],
        [3, "hashes", "Hashes", ["[0"], "One or more cryptographic hash codes of the file contents"]
      ]],
    ["IDN-Domain-Name", "String", ["/idn-hostname"], "Internationalized Domain Name - [RFC5890], Section 2.3.2.3"],
    ["IDN-Email-Addr", "String", ["/idn-email"], "Internationalized email address - [RFC6531]"],
    ["IPv4-Net", "Array", ["/ipv4-net"], "IPv4 address and prefix length", [
        [1, "ipv4_addr", "IPv4-Addr", [], "IPv4 address as defined in [RFC0791]"],
        [2, "prefix_length", "Integer", ["[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
      ]],
    ["IPv4-Connection", "Record", ["{1"], "5-tuple that specifies a tcp/ip connection", [
        [1, "src_addr", "IPv4-Net", ["[0"], "IPv4 source address range"],
        [2, "src_port", "Port", ["[0"], "Source service per [RFC6335]"],
        [3, "dst_addr", "IPv4-Net", ["[0"], "IPv4 destination address range"],
        [4, "dst_port", "Port", ["[0"], "Destination service per [RFC6335]"],
        [5, "protocol", "L4-Protocol", ["[0"], "Layer 4 protocol (e.g., TCP) - see L4-Protocol section"]
      ]],
    ["IPv6-Net", "Array", ["/ipv6-net"], "IPv6 address and prefix length", [
        [1, "ipv6_addr", "IPv6-Addr", [], "IPv6 address as defined in [RFC8200]"],
        [2, "prefix_length", "Integer", ["[0"], "prefix length. If omitted, refers to a single host address"]
      ]],
    ["IPv6-Connection", "Record", ["{1"], "5-tuple that specifies a tcp/ip connection", [
        [1, "src_addr", "IPv6-Net", ["[0"], "IPv6 source address range"],
        [2, "src_port", "Port", ["[0"], "Source service per [RFC6335]"],
        [3, "dst_addr", "IPv6-Net", ["[0"], "IPv6 destination address range"],
        [4, "dst_port", "Port", ["[0"], "Destination service per [RFC6335]"],
        [5, "protocol", "L4-Protocol", ["[0"], "Layer 4 protocol (e.g., TCP) - [Section 3.4.2.10]"]
      ]],
    ["IRI", "String", ["/iri"], "Internationalized Resource Identifier, [RFC3987]"],
    ["MAC-Addr", "Binary", ["/eui"], "Media Access Control / Extended Unique Identifier address - EUI-48 or EUI-64 as defined in [EUI]"],
    ["Process", "Map", ["{1"], "", [
        [1, "pid", "Integer", ["{0", "[0"], "Process ID of the process"],
        [2, "name", "String", ["[0"], "Name of the process"],
        [3, "cwd", "String", ["[0"], "Current working directory of the process"],
        [4, "executable", "File", ["[0"], "Executable that was executed to start the process"],
        [5, "parent", "Process", ["[0"], "Process that spawned this one"],
        [6, "command_line", "String", ["[0"], "The full command line invocation used to start this process, including all arguments"]
      ]],
    ["Properties", "ArrayOf", ["*String", "{1", "q"], "A list of names that uniquely identify properties of an Actuator."],
    ["URI", "String", ["/uri"], "Uniform Resource Identifier, [RFC3986]"],
    ["Date-Time", "Integer", ["{0"], "Date and Time"],
    ["Duration", "Integer", ["{0"], "A length of time"],
    ["Feature", "Enumerated", [], "Specifies the results to be returned from a query features Command", [
        [1, "versions", "List of OpenC2 Language versions supported by this Actuator"],
        [2, "profiles", "List of profiles supported by this Actuator"],
        [3, "pairs", "List of supported Actions and applicable Targets"],
        [4, "rate_limit", "Maximum number of Commands per minute supported by design or policy"],
        [5, "args", "List of supported Command Argumemnts"]
      ]],
    ["Hashes", "Map", ["{1"], "Cryptographic hash values", [
        [1, "md5", "Binary", ["/x", "{16", "}16", "[0"], "MD5 hash as defined in [RFC1321]"],
        [2, "sha1", "Binary", ["/x", "{20", "}20", "[0"], "SHA1 hash as defined in [RFC6234]"],
        [3, "sha256", "Binary", ["/x", "{32", "}32", "[0"], "SHA256 hash as defined in [RFC6234]"]
      ]],
    ["Hostname", "String", ["/hostname"], "Internet host name as specified in [RFC1123]"],
    ["IDN-Hostname", "String", ["/idn-hostname"], "Internationalized Internet host name as specified in [RFC5890], Section 2.3.2.3"],
    ["IPv4-Addr", "Binary", ["/ipv4-addr"], "32 bit IPv4 address as defined in [RFC0791]"],
    ["IPv6-Addr", "Binary", ["/ipv6-addr"], "128 bit IPv6 address as defined in [RFC8200]"],
    ["L4-Protocol", "Enumerated", [], "Value of the protocol (IPv4) or next header (IPv6) field in an IP packet. Any IANA value, [RFC5237]", [
        [1, "icmp", "Internet Control Message Protocol - [RFC0792]"],
        [6, "tcp", "Transmission Control Protocol - [RFC0793]"],
        [17, "udp", "User Datagram Protocol - [RFC0768]"],
        [132, "sctp", "Stream Control Transmission Protocol - [RFC4960]"]
      ]],
    ["Payload", "Choice", [], "", [
        [1, "bin", "Binary", [], "Specifies the data contained in the artifact"],
        [2, "url", "URI", [], "MUST be a valid URL that resolves to the un-encoded content"]
      ]],
    ["Port", "Integer", ["{0", "}65535"], "Transport Protocol Port Number, [RFC6335]"],
    ["Response-Type", "Enumerated", [], "", [
        [0, "none", "No response"],
        [1, "ack", "Respond when Command received"],
        [2, "status", "Respond with progress toward Command completion"],
        [3, "complete", "Respond when all aspects of Command completed"]
      ]],
    ["Versions", "ArrayOf", ["*Version", "{0", "}10", "q"], "List of OpenC2 language versions"],
    ["Profiles", "ArrayOf", ["*Namespace", "{0", "}0", "q"], "List of OpenC2 profiles"],
    ["Version", "String", [], "Major.Minor version number"],
    ["Namespace", "String", ["/uri"], "Unique name of an Actuator Profile"],
    ["Command-ID", "String", ["%^\\S{0,36}$"], "Command Identifier"]
    ]
    }


    root_name = 'foobar'


if __name__=="__main__":    
   create_jadn_xsd()