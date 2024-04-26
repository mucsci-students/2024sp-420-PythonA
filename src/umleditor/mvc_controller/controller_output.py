from umleditor.mvc_model.custom_exceptions import CustomExceptions as CE

def write(s: str) -> None:
    print(s)

def write_file(path: str, content: str) -> None:
    '''
    Writes the specified content to a file at the given path.

    # Parameters:
    - `path` (str): The path to the file to be written.
    - `content` (str): The content to be written to the file.

    # Returns:
    - None

    # Raises:
    - `FileNotFoundError`: If the specified file is not found.
    - `IOError`: If there is an issue writing to the file.
    - Other exceptions: Any other exceptions that may occur during the file writing process.
    '''
    try:
        open(path, 'w').write(content)
    except Exception:
        raise CE.WriteFileError(path)