#===============================================================================#
                        #Import From Controller Tests#
#===============================================================================#
def test_import_cli_controller():
    from src.umleditor.mvc_controller.cli_controller import CLI_Controller
    assert CLI_Controller
    assert CLI_Controller.run

def test_import_controller_input():
    from src.umleditor.mvc_controller.controller_input import read_line, read_file
    assert read_line
    assert read_file

def test_import_controller_output():
    from src.umleditor.mvc_controller.controller_output import write, write_file
    assert write
    assert write_file

def test_import_controller():
    from src.umleditor.mvc_controller import Controller
    assert Controller
    assert Controller.run
    assert Controller.quit
    assert Controller.save
    assert Controller.load

def test_import_gui_controller():
    from src.umleditor.mvc_controller.gui_controller import ControllerGUI
    assert ControllerGUI
    assert ControllerGUI.run
    assert ControllerGUI.save_file
    assert ControllerGUI.load_file
    assert ControllerGUI.rename_class
    assert ControllerGUI.add_class
    assert ControllerGUI.delete_class
    assert ControllerGUI.acceptance_state

def test_import_serialzer():
    from src.umleditor.mvc_controller.serializer import CustomJSONEncoder, serialize, deserialize
    assert CustomJSONEncoder
    assert serialize
    assert deserialize

def test_import_uml_lexer():
    from src.umleditor.mvc_controller.uml_lexer import _command_flag_map, _command_function_map, lex_input
    assert _command_flag_map
    assert _command_function_map
    assert lex_input

def test_import_uml_parser():
    from src.umleditor.mvc_controller.uml_parser import parse, check_args
    assert parse
    assert check_args

#===============================================================================#
                        #Import From Model Tests#
#===============================================================================#
def test_import_custom_exceptions():
    from src.umleditor.mvc_model.custom_exceptions import CustomExceptions
    assert CustomExceptions

def test_import_diagram():
    from src.umleditor.mvc_model import Diagram
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

def test_import_entity():
    from src.umleditor.mvc_model import Entity
    assert Entity
    assert Entity.get_name
    assert Entity.set_name
    assert Entity.add_field
    assert Entity.delete_field
    assert Entity.rename_field
    assert Entity.get_method
    assert Entity.add_method
    assert Entity.delete_method
    assert Entity.rename_method
    assert Entity.list_fields
    assert Entity.list_methods

def test_import_uml_method():
    from src.umleditor.mvc_model.entity import UML_Method
    assert UML_Method
    assert UML_Method.get_method_name
    assert UML_Method.set_method_name
    assert UML_Method.add_parameters
    assert UML_Method.remove_parameters
    assert UML_Method.change_parameters

def test_import_help():
    from umleditor.mvc_view.help_command import help_menu
    assert help_menu

def test_import_relation():
    from src.umleditor.mvc_model import Relation
    assert Relation
    assert Relation.get_source
    assert Relation.get_destination
    assert Relation.set_type
    assert Relation.contains

#===============================================================================#
                        #Import From View Tests#
#===============================================================================#
def test_import_class_card():
    from src.umleditor.mvc_view.gui_view.gui_cworld.class_card import ClassCard
    assert ClassCard
    assert ClassCard.set_name
    assert ClassCard.initUI
    assert ClassCard.connect_menus
    assert ClassCard.set_styles
    assert ClassCard.show_class_menu
    assert ClassCard.show_row_menu
    assert ClassCard.rename_action_clicked
    assert ClassCard.confirm_rename_clicked
    assert ClassCard.accept_new_name
    assert ClassCard.edit_action_clicked
    assert ClassCard.delete_action_clicked
    assert ClassCard.confirm_delete_class
    assert ClassCard.menu_action_clicked
    assert ClassCard.eventFilter
    assert ClassCard.escape_from_row
    assert ClassCard.enable_context_menus
    assert ClassCard.verify_input
    assert ClassCard.split_relation
    assert ClassCard.deselect_line
    assert ClassCard.get_selected_line
    assert ClassCard.get_task_signal
    assert ClassCard.get_enable_signal
    assert ClassCard.add_field
    assert ClassCard.add_method
    assert ClassCard.add_relation

def test_import_class_input_dialog():
    from src.umleditor.mvc_view.gui_view.gui_cworld.class_input_dialog import CustomInputDialog
    assert CustomInputDialog

def test_import_view_gui():
    from src.umleditor.mvc_view.gui_view.gui_cworld.view_GUI import ViewGUI
    assert ViewGUI
    assert ViewGUI.get_signal
    assert ViewGUI.connect_menu
    assert ViewGUI.invalid_input_message
    assert ViewGUI.forward_signal
    assert ViewGUI.add_class_click
    assert ViewGUI.confirm_class_clicked
    assert ViewGUI.add_class_card
    assert ViewGUI.delete_class_card
    assert ViewGUI.delete_all_class_card
    assert ViewGUI.save_click
    assert ViewGUI.confirm_save_clicked
    assert ViewGUI.load_click
    assert ViewGUI.confirm_load_clicked
    assert ViewGUI.exit_click
    assert ViewGUI.help_click
    assert ViewGUI.enable_widgets
    