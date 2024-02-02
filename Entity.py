class Entity:
    def __init__(self, name:str) -> None:
        """
        Initialize a new Entity instance.

        Args:
            name (str): The name of the entity.
        """
        self.setName(name)

    def setName(self, name: str) -> None:
        """
        Update entity name

        Args:
            name (str): New name to be set

        Raises:
            ValueError: If the name contains non-alphanumeric characters.
        """
        if not name.isalnum():
            raise ValueError("Name must contain only alphanumeric characters")
        self._name = name
  