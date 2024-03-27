from umleditor.mvc_model import CustomExceptions as CE
from umleditor.usability.autofill import autofill, redo, undo
import readchar


def read_line(s='Command: ') -> str:
    """
     Print a message to cmd and get a line of input, supporting autofill functionality
    for the last word before a space, and handling undo and redo operations.

    ## Parameters:
    - `s` (str): The message to print before asking for input

    ## Returns:
    - (str): A line of input with the last word autofilled if Tab is pressed,
             and 'undo' or 'redo' added if 'z' or 'y' are pressed, respectively.
    """
    print(s, end='', flush=True)
    input_line = []
    while True:
        ch = readchar.readkey()
        if ch == readchar.key.TAB:
            # Call autofill with the current input line
            new_input_line = autofill(''.join(input_line))
            # Calculate the number of characters to overwrite (clear)
            num_chars_to_clear = len(input_line) - len(new_input_line) + 1
            print('\r' + s + new_input_line + ' ' * num_chars_to_clear, end='', flush=True)
            input_line = list(new_input_line)
        elif ch == 'z':  # Undo operation
            input_line = list(undo())  # Replace input_line with the result of undo()
            print('\r' + s + ''.join(input_line), end='', flush=True)
            print()
            return ''.join(input_line).strip()  # Hitting Enter
        elif ch == 'y':  # Redo operation
            input_line = list(redo())  # Replace input_line with the result of redo()
            print('\r' + s + ''.join(input_line), end='', flush=True)
            print()
            return ''.join(input_line).strip()  # Hitting Enter
        elif ch == readchar.key.ENTER:
            print()  # Move to the next line
            return ''.join(input_line).strip()  # Hitting Enter
        elif ch == readchar.key.BACKSPACE:
            if input_line:  # Remove the last character from input_line
                input_line.pop()
                print('\r' + s + ''.join(input_line) + ' ', end='', flush=True)  # Refresh the input display
                print('\b', end='', flush=True) # Move cursor back to the right position
        else:
            input_line.append(ch)
            print(ch, end='', flush=True)  # Echo the input character


def read_file(path: str) -> str:
    """
    Reads the contents of a file and returns the content as a string.

    #### Parameters:
    - `path` (str): The path to the file to be read.

    #### Returns:
    - (str): The content of the file as a string.

    #### Raises:
    - (CustomExceptions.ReadFileError): If failed to read the file
    """
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception:
        raise CE.ReadFileError(filepath=path)
