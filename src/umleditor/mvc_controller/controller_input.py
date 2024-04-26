from umleditor.custom_exceptions import CustomExceptions as CE
from umleditor.mvc_controller.autofill import CommandCompleter
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

history = InMemoryHistory()


def read_line(s='Command: ') -> str:
    while True:
        user_input = prompt(s, completer=CommandCompleter(), history=history)
        break
    return user_input


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
