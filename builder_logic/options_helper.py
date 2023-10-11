from ast import List

from builder_logic.jadn_constants import OPTION_KEYS, OPTIONS


def opt_list_2_dict(opts: []):
    """
    Convert JADN formatted option in list format to a dict
    :param opts: JADN formatted options
    :raise KeyError: invalid option given
    :return: key/value formatted options
    """
    rslt = {}
    for opt in opts:
        key, val = opt[0], opt[1:]
        if args := OPTIONS.get(ord(key)):
            rslt[args[0]] = args[1](val)
        else:
            raise KeyError(f"Unknown option id of {key}")
    return rslt


def get_jadn_option(options: []):
    return_options = {}

    if len(options) > 0:

        # TODO: just handling first option for now....need for loop
        for option in options:

            # TODO: add other options
            # regex or pattern
            if OPTION_KEYS["regex"] == option[0] or OPTION_KEYS["pattern"] == option[0]:
                trimmed_option = option[1:]
                return_options['%'] = trimmed_option 
                
            # Left off here......
          
    return return_options