from CustomExceptions import CustomExceptions as CE

def readLine(s='Command: ') -> str:
    '''
    Print a message to cmd and get a line of input

    ## Parameters:
    - `s` (str): The message to print before asking for input

    ## Returns:
    - (str): A line of input
    '''
    return input(s)

def read_file(path: str) -> str:
    '''
    Reads the contents of a file and returns the content as a string.

    #### Parameters:
    - `path` (str): The path to the file to be read.

    #### Returns:
    - (str): The content of the file as a string.

    #### Raises:
    - (CustomExceptions.ReadFileError): If failed to read the file
    '''
    try:
        return open(path, 'r').read()
    except Exception:
        raise CE.ReadFileError(filepath=path)