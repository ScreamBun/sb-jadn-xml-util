from constants.jadn_constants import *


def get_root_et(multi_root: dict, name: str):
    
    root_found = multi_root.get(name)
    
    if root_found == None:
        root_found = multi_root.get('schema')
    
    return root_found


def get_all_jadn_descendants(match_name: str, data_to_search: [], family_tree: []):
    
    for jadn_type in data_to_search:
        jadn_type_name = jadn_type[0]    
    
        if match_name == jadn_type_name:
            family_tree.append(match_name)
            
            if jadn_type[1] == MAPOF_CONST:
                field_data = jadn_type[2]
                map_k = field_data[0]
                map_v = field_data[1]
                map_filtered_key = map_k[1:len(map_k)]
                map_filtered_val = map_v[1:len(map_v)]
                
                if map_filtered_key not in family_tree:
                    get_all_jadn_descendants(map_filtered_key, data_to_search, family_tree)
                    
                if map_filtered_val not in family_tree:
                    get_all_jadn_descendants(map_filtered_val, data_to_search, family_tree)                                    
                
            elif jadn_type[1] == ARRAYOF_CONST:
                field_data = jadn_type[2]
                arr_v = field_data[0]
                arr_filtered_val = arr_v[1:len(arr_v)]
                if arr_filtered_val:
                    if arr_filtered_val not in family_tree:
                        get_all_jadn_descendants(arr_filtered_val, data_to_search, family_tree)  
                
            else:
                if len(jadn_type[4]) > 0:
                    for field in jadn_type[4]:
                        if field[2]:
                            if field[2] not in family_tree:
                                get_all_jadn_descendants(field[2], data_to_search, family_tree)  
    
    return family_tree


def get_base_type(type: str):
    is_found = None
    for item in ALL_TYPES:
        if item == type:
            is_found = item
            break
    return is_found


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


def find_ref_type(name, all_types):
    type_found = None
    for type in all_types:
        if type[0] == name:
            type_found = type
            break

    return type_found

def get_type_option_vals(opts: [], base_type: str, all_types: {}):
    opt_vals_fd = {}
    
    for opt_code in TYPE_OPTIONS_FROZ_DICT.values():
        opt_vals_fd[opt_code] = None
    
    allowed_opts = ALLOWED_TYPE_OPTIONS.get(base_type)
    if not allowed_opts:
        ref_type = find_ref_type(base_type, all_types)
        if ref_type:
            base_type = ref_type[1]
    
    for allowed_opt in ALLOWED_TYPE_OPTIONS.get(base_type):
        opt_key_char = get_type_option_code(allowed_opt)
        for opt in opts:
            if opt[0] == opt_key_char:
                if len(opt) == 1:
                    opt_val = opt[0]
                    opt_vals_fd[opt_key_char] = opt_val
                else:
                    opt_val = opt[1:len(opt)]
                    opt_vals_fd[opt_key_char] = opt_val
                break
    
    return opt_vals_fd


def get_active_type_option_vals(opts: [], base_type: str, all_types: {}):
    type_opts = get_type_option_vals(opts, base_type, all_types)
    return dict(filter(lambda item: item[1] != None, type_opts.items()))


def get_opt_type_val(type_opt_const_name: str, active_type_opts: {}):
    code = TYPE_OPTIONS_FROZ_DICT.get(type_opt_const_name)
    return active_type_opts.get(code)    
    

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


def get_field_option_val(opts: [], id: str):
    opt_val = None
    
    for opt in opts:
        if opt[0] == id:
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


def get_vtype(opts: [], type: str = ARRAYOF_CONST):
    vtype = None
    
    for opt in opts:
        if opt[0] == "*":
            vtype = opt.replace("*", "", 1)
            break
        
    return vtype