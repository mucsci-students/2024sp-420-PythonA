class Entity:
    def __init__(self, name:str) -> None:
        """
        Initialize a new Entity instance.

        Args:
            name (str): The name of the entity.

        Raises:
            ValueError: If the name contains non-alphanumeric characters.

        """
        if not name.isalnum():
            raise ValueError("Name must contain only alphanumeric characters")
        self._name = name