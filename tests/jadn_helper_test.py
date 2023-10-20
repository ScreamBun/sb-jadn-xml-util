

from constants.jadn_constants import MAP_CONST
from helpers.jadn_helper import get_type_option_vals


def test_map_get_type_option_vals():
    
    opts = ["=", "X", "{4", "}8"]
    base_type = MAP_CONST
    return_val = get_type_option_vals(opts, base_type)
    
    assert return_val != None and len(return_val) > 0
    assert return_val.get("=") == "="
    assert return_val.get("X") == "X"
    assert return_val.get("{") == "4"
    assert return_val.get("}") == "8"
