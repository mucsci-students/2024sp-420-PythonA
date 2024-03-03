#===============================================================================#
                        #Import From Controller Tests#
#===============================================================================#
def test_import_cli_controller():
    from umleditor.mvc_controller.cli_controller import CLI_Controller
    assert CLI_Controller
    assert CLI_Controller.run

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
    assert Controller.run
    assert Controller.quit
    assert Controller.save
    assert Controller.load

def test_import_gui_controller():
    from umleditor.mvc_controller.gui_controller import ControllerGUI
    assert ControllerGUI
    assert ControllerGUI.run
    assert ControllerGUI.save_file
    assert ControllerGUI.load_file
    assert ControllerGUI.rename_class
    assert ControllerGUI.add_class
    assert ControllerGUI.delete_class
    assert ControllerGUI.acceptance_state

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
    assert Diagram.add_entity
    assert Diagram.get_entity
    assert Diagram.delete_entity
    assert Diagram.has_entity
    assert Diagram.rename_entity
    assert Diagram.list_everything
    assert Diagram.list_entity_details
    assert Diagram.list_entities
    assert Diagram.list_relations
    assert Diagram.list_entity_relations
    assert Diagram.add_relation
    assert Diagram.delete_relation
    assert Diagram.change_relation_type
    assert Diagram.edit_relation

def test_import_entity():
    from umleditor.mvc_model import Entity
    assert Entity
    assert Entity.get_name
    assert Entity.set_name
    assert Entity.add_field
    assert Entity.delete_field
    assert Entity.rename_field
    assert Entity.get_method
    assert Entity.add_method
    assert Entity.add_method_and_params
    assert Entity.edit_method
    assert Entity.delete_method
    assert Entity.rename_method
    assert Entity.list_fields
    assert Entity.list_methods

def test_import_uml_method():
    from umleditor.mvc_model.entity import UML_Method
    assert UML_Method
    assert UML_Method.get_method_name
    assert UML_Method.set_method_name
    assert UML_Method.add_parameters
    assert UML_Method.remove_parameters
    assert UML_Method.change_parameters

def test_import_help():
    from umleditor.mvc_model.help_command import help_menu
    assert help_menu

def test_import_relation():
    from umleditor.mvc_model import Relation
    assert Relation
    assert Relation.get_source
    assert Relation.get_destination
    assert Relation.set_type
    assert Relation.contains

#===============================================================================#
                        #Import From View Tests#
#===============================================================================#
def test_import_class_card():
    from umleditor.mvc_view.gui_view.class_card import ClassCard
    assert ClassCard

def test_import_class_input_dialog():
    from umleditor.mvc_view.gui_view.class_input_dialog import CustomInputDialog
    assert CustomInputDialog

def test_import_view_gui():
    from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
    assert ViewGUI