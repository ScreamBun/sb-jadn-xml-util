from constants.jadn_constants import ALLOWED_TYPE_OPTIONS, ARRAYOF_CONST, MAPOF_CONST, MAXV_CONST, MINV_CONST, TYPE_OPTIONS_FROZ_DICT


def get_type_option_code(human_name: str):
    code: chr = None
    
    for opt in TYPE_OPTIONS_FROZ_DICT.items():
        if opt[0] == human_name:
            code = opt[1]
            break
    
    return code

def get_type_option_human_name(code: chr):
    human_name: chr
    
    for opt in TYPE_OPTIONS_FROZ_DICT.items():
        if opt[1] == code:
            human_name = opt[0]
            break
    
    return human_name

def is_type_option_allowed(base_type: str, human_name: str):
    is_allowed: bool = False
    
    for opt in ALLOWED_TYPE_OPTIONS[base_type]:
        if opt == human_name:
            is_allowed = True
            break
    
    return is_allowed


def get_type_option_val(opts: [], base_type: str, opt_human_name: str):
    opt_val = None
    
    is_allowed = is_type_option_allowed(base_type, opt_human_name)
    
    if is_allowed:
        opt_key_char = get_type_option_code(opt_human_name)
        for opt in opts:
            if opt[0] == opt_key_char:
                if len(opt) == 1:
                    opt_val = opt[0]
                else:
                    opt_val = opt[1:len(opt)]
                break
    
    return opt_val

# NOT USED
def get_ktype(opts: [], type: str = ARRAYOF_CONST):
    ktype = None
    
    if type == ARRAYOF_CONST:
        ktype = opts[0].replace("+", "", 1)
    elif type == MAPOF_CONST:
        ktype = opts[0].replace("+", "", 1)
        
    return ktype

# USED, BUT SHOULD BE REPLACED WITH GET OPTION VAL
def get_vtype(opts: [], type: str = ARRAYOF_CONST):
    vtype = None
    
    if type == ARRAYOF_CONST:
        vtype = opts[0].replace("*", "", 1)
    elif type == MAPOF_CONST:
        vtype = opts[1].replace("*", "", 1)
        
    return vtype