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

    # Parameters:
    - `path` (str): The path to the file to be read.

    # Returns:
    - (str): The content of the file as a string.

    # Raises:
    - `FileNotFoundError`: If the specified file is not found.
    - `IOError`: If there is an issue reading the file.
    - Other exceptions: Any other exceptions that may occur during the file reading process.
    '''
    return open(path, 'r').read()