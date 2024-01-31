class CustomExceptions:
    class Error(Exception):
        """Base class for other exceptions."""
        pass

    class EntityExistsError(Error):
        """Exception raised when an entity with a given name already exists."""

        def __init__(self, name) -> None:
            super().__init__(f"Object with name '{name}' already exists.")
