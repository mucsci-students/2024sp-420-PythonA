from umleditor.mvc_model import CustomExceptions as CE
from umleditor.usability.autofill import autofill, redo, undo
from readchar import readkey, key

def read_line(s='Command: ') -> str:
    """
     Print a message to cmd and get a line of input, supporting autofill functionality
    for the last word before a space, and handling undo and redo operations.

    ## Parameters:
    - `s` (str): The message to print before asking for input

    ## Returns:
    - (str): A line of input with the last word autofilled if Tab is pressed,
             and 'undo' or 'redo' added if '*' or '**' are pressed, respectively.
    """
    print(s, end='', flush=True)
    input_line = []
    cursor_pos = 0  # Keep track of the cursor's position
    while True:
        ch = readkey()
        if ch == key.TAB:
            # Call autofill with the current input line
            new_input_line = autofill(''.join(input_line))
            # Calculate the number of characters to overwrite (clear)
            num_chars_to_clear = len(input_line) - len(new_input_line) + 1
            print('\r' + s + new_input_line + ' ' * num_chars_to_clear, end='', flush=True)
            input_line = list(new_input_line)
            cursor_pos = len(input_line)  # Move cursor to the end
        elif ch == '*':  # Undo operation
            input_line = list(undo())  # Replace input_line with the result of undo()
            print('\r' + s + ''.join(input_line), end='', flush=True)
            print()
            return ''.join(input_line).strip()  # Hitting Enter
        elif ch == '**':  # Redo operation
            input_line = list(redo())  # Replace input_line with the result of redo()
            print('\r' + s + ''.join(input_line), end='', flush=True)
            print()
            return ''.join(input_line).strip()  # Hitting Enter
        elif ch == key.ENTER:
            print()  # Move to the next line
            return ''.join(input_line).strip()  # Hitting Enter
        elif ch == key.BACKSPACE:
            if cursor_pos > 0:  # Ensure cursor isn't at the start
                input_line.pop(cursor_pos - 1)
                cursor_pos -= 1  # Move cursor back
                print('\r' + s + ''.join(input_line) + ' ', end='', flush=True)  # Refresh the input display
                print('\r' + s + ''.join(input_line[:cursor_pos]), end='',
                      flush=True)  # Move cursor to correct position
        elif ch == key.RIGHT:
            if cursor_pos < len(input_line):  # Ensure cursor isn't at the end
                cursor_pos += 1
                print('\r' + s + ''.join(input_line[:cursor_pos]), end='', flush=True)  # Move cursor to the right
        elif ch == key.LEFT:
            if cursor_pos > 0:  # Ensure cursor isn't at the start
                cursor_pos -= 1
                print('\r' + s + ''.join(input_line[:cursor_pos]), end='', flush=True)  # Move cursor to the left
        elif ch in [key.UP, key.DOWN]:
            # Ignore up and down arrow keys and maintain the cursor position
            print('\r' + s + ''.join(input_line) + ' ', end='', flush=True)  # Refresh the input display
            print('\r' + s + ''.join(input_line[:cursor_pos]), end='', flush=True)  # Reset cursor to correct position
        else:
            input_line.insert(cursor_pos, ch)
            cursor_pos += 1  # Advance cursor after insertion
            print('\r' + s + ''.join(input_line) + ' ', end='', flush=True)  # Refresh the input display
            print('\r' + s + ''.join(input_line[:cursor_pos]), end='', flush=True)  # Move cursor to correct position


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
