from constants.jadn_constants import ALLOWED_TYPE_OPTIONS, ARRAYOF_CONST, MAXV_CONST, MINV_CONST, TYPE_OPTIONS_FROZ_DICT


def get_type_option_code(human_name: str):
    code: chr
    
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


def get_minv(opts: [], base_type: str):
    minv_val = None
    is_allowed: bool = False
    
    minv_code = get_type_option_code(MINV_CONST)
    is_allowed = is_type_option_allowed(base_type, MINV_CONST)
    
    if is_allowed:
        for opt in opts:
            if opt[0] == minv_code:
                minv_val = opt[1]
                break
    
    return minv_val


def get_maxv(opts: [], base_type: str):
    maxv_val = None
    is_allowed: bool = False
    
    maxv_code = get_type_option_code(MAXV_CONST)
    is_allowed = is_type_option_allowed(base_type, MAXV_CONST)
    
    if is_allowed:
        for opt in opts:
            if opt[0] == maxv_code:
                maxv_val = opt[1]
                break
    
    return maxv_val


def get_ktype(opts: [], type: str = ARRAYOF_CONST):
    ktype = None
    
    if type == ARRAYOF_CONST:
        ktype = opts[0].replace("+", "", 1)
    elif type == "MapOf":
        ktype = opts[0].replace("+", "", 1)
        
    return ktype


def get_vtype(opts: [], type: str = ARRAYOF_CONST):
    vtype = None
    
    if type == ARRAYOF_CONST:
        vtype = opts[0].replace("*", "", 1)
    elif type == "MapOf":
        vtype = opts[1].replace("*", "", 1)
        
    return vtype