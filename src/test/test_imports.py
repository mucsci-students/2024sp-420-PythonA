#===============================================================================#
                        #Import From Controller Tests#
#===============================================================================#
def test_import_cli_controller():
    from umleditor.mvc_controller.cli_controller import CLI_Controller
    assert CLI_Controller

def test_import_controller_input():
    from umleditor.mvc_controller.controller_input import read_line, read_file
    assert read_line
    assert read_file

def test_import_controller_output():
    from umleditor.mvc_controller.controller_output import write, write_file
    assert write
    assert write_file

def test_import_controller():
    from umleditor.mvc_controller import Controller
    assert Controller

def test_import_gui_controller():
    from umleditor.mvc_controller.gui_controller import ControllerGUI
    assert ControllerGUI

def test_import_serialzer():
    from umleditor.mvc_controller.serializer import CustomJSONEncoder, serialize, deserialize
    assert CustomJSONEncoder
    assert serialize
    assert deserialize

def test_import_uml_lexer():
    from umleditor.mvc_controller.uml_lexer import _command_flag_map, _command_function_map, lex_input
    assert _command_flag_map
    assert _command_function_map
    assert lex_input

def test_import_uml_parser():
    from umleditor.mvc_controller.uml_parser import parse, check_args
    assert parse
    assert check_args

#===============================================================================#
                        #Import From Model Tests#
#===============================================================================#
def test_import_custom_exceptions():
    from umleditor.mvc_model.custom_exceptions import CustomExceptions
    assert CustomExceptions

def test_import_diagram():
    from umleditor.mvc_model import Diagram
    assert Diagram

def test_import_entity():
    from umleditor.mvc_model import Entity
    assert Entity

def test_import_help():
    from umleditor.mvc_model.help_command import help_menu
    assert help_menu

def test_import_method():
    from umleditor.mvc_model import UML_Method
    assert UML_Method

def test_import_relation():
    from umleditor.mvc_model import Relation
    assert Relation


#===============================================================================#
                        #Import From View Tests#
#===============================================================================#
def test_import_class_card():
    from umleditor.mvc_view.gui_view.class_card import ClassCard
    assert ClassCard

def test_import_class_input_dialog():
    from umleditor.mvc_view.gui_view.class_input_dialog import ClassInputDialog
    assert ClassInputDialog

def test_import_view_gui():
    from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
    assert ViewGUI