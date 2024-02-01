from Entity import Entity
from Relation import Relation
from CustomExceptions import CustomExceptions

class Diagram:
    def __init__(self) -> None:
        self._entities = dict()
        self._relations = []

    def addClass(self, name: str) -> None:
        """
        Add a class with the given name to our dictionary of entities.

        Args:
            name (str): The name of the class to add.

        Raises:
            CustomExceptions.EntityExistsError: If a class with the same name already exists.

        Returns:
            None
        """
        if name in self._entities:
            raise CustomExceptions.EntityExistsError(name)
        self._entities[name] = Entity(name)

        
