from umleditor.mvc_controller.uml_lexer import _command_flag_map
from umleditor.mvc_model.help_command import help_menu
import re

def test_help():
    menu = help_menu()
    for key in _command_flag_map:
        if key != "help":
            for flag in _command_flag_map[key]:
                val = ""
                if flag != "":
                    val = key + " -" + flag 
                else:
                    val = key + flag
                assert re.search(val, menu) != None, (val + " not in help menu")