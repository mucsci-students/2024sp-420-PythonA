from umleditor.mvc_controller.uml_lexer import _command_flag_map

suggestions = list(_command_flag_map.keys())


def autofill(input_line):
    """
    Fills in the last word in your input with a command suggestion.
    It looks at the last word you typed and tries to complete it based on a list of known commands.

    For example, if you type 'cl' and hit Tab, it might complete it to 'class' if 'class' is a known command.

    ## Parameters:
    - 'input_line' (str): The current line of input.

    ## Returns:
    - (str): The current line of input with the command segment autofilled.
    """
    # Extract the current segment based on where the cursor is
    segments = input_line.split()
    if segments:
        current_segment = segments[-1]  # The last segment is assumed to be the current
        matches = [s for s in suggestions if s.startswith(current_segment)]
        if matches:
            segments[-1] = matches[0]  # Replace with the first match
            return ' '.join(segments) + ' '
        return input_line
    else:
        return input_line


def get_args(args):
    suggestions.extend(args)


def undo():
    return 'undo'


def redo():
    return 'redo'
