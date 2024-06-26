# Primary: Danish
# Secondary: Zhang
from umleditor.mvc_model import CustomExceptions as CE
from .uml_lexer import lex_input as lex
from umleditor.mvc_model import Diagram, Entity, Relation, UML_Method
from ..mvc_view.cli_view import help_command
import re
import keyword

# list of all classes that need to be searched for commands
classes = [Diagram, Entity, Relation, UML_Method, help_command]


def parse(c, input_str: str) -> list:
    bits = input_str.split()

    # Extract the command and flag
    command_str = lex(bits[0:1], bits[1:2])

    # Determine the class of the command
    command_class = __find_class(command_str)

    obj = c
    args = []

    if command_class == Entity and command_str == "add_method":

        # Validate the number of arguments for adding a method
        if len(bits) < 5:
            raise CE.NeedsMoreInput()

        # Extract the class name and method name
        class_name = bits[2]
        method_name = bits[3]
        return_type = bits[4]
        obj = c._diagram.get_entity(class_name)

        args = [method_name, return_type]

    if command_class == Entity and command_str == "delete_method":

        # Validate the number of arguments for adding a method
        if len(bits) < 4:
            raise CE.NeedsMoreInput()

        # Extract the class name and method name
        class_name = bits[2]
        method_name = bits[3]
        obj = c._diagram.get_entity(class_name)

        args = [method_name]


    elif command_class == UML_Method and command_str == "add_parameters":

        # Minimum length is 4 when the parameter type is not provided

        if len(bits) < 3:
            raise CE.NeedsMoreInput()

        # Extract parameters based on provided arguments

        entity_name = bits[2]
        method_name = bits[3]
        parameter_name = bits[4]

        # Assign parameter_type only if it's provided
        ent = c._diagram.get_entity(entity_name)
        obj = ent.get_method(method_name)

        # Prepare arguments for adding a parameter
        args = [parameter_name]


    elif command_class == UML_Method and command_str == "remove_parameters":

        if len(bits) < 3:
            raise CE.NeedsMoreInput()

        entity_name, method_name, parameter_name = bits[2:5]
        ent = c._diagram.get_entity(entity_name)

        obj = ent.get_method(method_name)


        # Ensure the parameter type is valid and convert it to the correct type object
        args = obj.remove_parameters(parameter_name)



    elif command_class == UML_Method and command_str == "change_parameters":


        if len(bits) < 6:
            raise CE.NeedsMoreInput()
        entity_name, method_name, op_name, np_name = bits[2:6]
        ent = c._diagram.get_entity(entity_name)
        obj = ent.get_method(method_name)

        # obj.change_parameters(op_name,np_name)
        args = [op_name, np_name]


    else:
        # Handle other commands as before
        if not str(bits[1:2]).__contains__("-"):
            args = check_args(bits[1:])
        else:
            args = check_args(bits[2:])

        if command_class == Diagram:
            obj = c._diagram
        elif command_class == Entity:
            if not args:
                raise CE.NeedsMoreInput()
            obj = c._diagram.get_entity(args.pop(0))
        elif command_class == help_command:
            obj = help_command


    return [getattr(obj, command_str)] + args


def __split_list(args: list[str]) -> list[list[str]]:
    """Splits a list on the delimiter "|"

        Returns
            A list of lists containing the lhs and rhs of the "|"
    """
    lhs = []
    rhs = []
    seen_bar = False
    for arg in args:
        if arg == '|':
            seen_bar = True
            continue

        rhs.append(arg) if seen_bar else lhs.append(arg)

    if len(rhs) == 0:
        return [lhs]
    else:
        return [lhs, rhs]


def __find_class(function: str):
    """ Takes a function and locates the class that it exists in

        Args:
            function - the function to locate in a class

        Returns:
            the class the function originates in"""
    for cl in classes:
        if hasattr(cl, function):
            return cl


def is_valid_arg(arg):
    if keyword.iskeyword(arg) or not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\-]*$', arg):
        return False
    return True
def check_args(args: list):
    """Given a list of args, checks to make sure each one is valid.
        Valid is defined as containing alphanumeric chars, underscore, and hyphen.


        Args:
            args(list): a list of strings to be checked

        Return:
            CustomExceptions.InvalidArgumentError if an argument provided is invalid
            The list of args provided if all args are valid
    """
    for arg in args:
        if not is_valid_arg(arg):
            raise CE.InvalidArgumentError(arg)

    return args

