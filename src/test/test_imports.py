def test_import_controller():
    from umleditor.mvc_controller import Controller
    assert Controller

def test_import_diagram():
    from umleditor.mvc_model import Diagram
    assert Diagram

def test_import_entity():
    from umleditor.mvc_model import Entity
    assert Entity

def test_import_relation():
    from umleditor.mvc_model import Relation
    assert Relation

def test_import_method():
    from umleditor.mvc_model import UML_Method
    assert UML_Method

def test_controller_input_imports():
    from umleditor.mvc_controller.controller_input import read_line, read_file
    assert read_line
    assert read_file

def test_controller_output_imports():
    from umleditor.mvc_controller.controller_output import write, write_file
    assert write
    assert write_file

def test_serialzer_imports():
    from umleditor.mvc_controller.serializer import CustomJSONEncoder, serialize, deserialize
    assert CustomJSONEncoder
    assert serialize
    assert deserialize
 
def test_import_parser():
    from umleditor.mvc_controller.uml_parser import Parser
    assert Parser

def test_custom_exceptions_import():
    from umleditor.mvc_model.custom_exceptions import CustomExceptions
    assert CustomExceptions

def test_help_import():
    from umleditor.mvc_model.help_command import help_menu
    assert help_menu

def test_cli_lexer_import():
    from umleditor.mvc_view.cli_lexer import _command_flag_map, _command_function_map
    assert _command_flag_map
    assert _command_function_map