from Entity import Entity
from Relation import Relation
from CustomExceptions import CustomExceptions

class Diagram:
    def __init__(self) -> None:
        self._entities = dict()
        self._relations = []

    def addEntity(self, name: str) -> None:
        """
        Add a entity with the given name to our dictionary of entities.

        Args:
            name (str): The name of the entity to add.

        Raises:
            CustomExceptions.EntityExistsError: If a entity with the same name already exists.

        Returns:
            None
        """
        if name in self._entities:
            raise CustomExceptions.EntityExistsError(name)
        self._entities[name] = Entity(name)
    
    def deleteEntity(self, name: str) -> None:
        """
        Delete a given entity from our dictionary.

        Args:
            name (str): The name of the entity to deleted.

        Raises:
            CustomExceptions.EntityNotFoundError: If a entity to be deleted does not exist.

        Returns:
            None
        """
        if name not in self._entities:
            raise CustomExceptions.EntityNotFoundError(name)
        # Delete relations containing the given entity
        for relation in self._relations:
            if relation.contains(self._entities[name]):
                self.deleteRelation(relation)
        del self._entities[name]


    def renameEntity(self, oldName: str, newName: str) -> None:
        """
        Rename a given entity with a new name.

        Args:
            oldName (str): The current name of the entity to be renamed.
            newName (str): The new name for the entity.

        Raises:
            CustomExceptions.EntityNotFoundError: If a entity with the old name does not exist.
            CustomExceptions.EntityExistsError: If a entity with the new name already exists.

        Returns:
            None
        """
        if oldName not in self._entities:
            raise CustomExceptions.EntityNotFoundError(oldName)
        if newName in self._entities:
            raise CustomExceptions.EntityExistsError(newName)
        # Update key
        entity = self._entities[oldName]
        entity.setName(newName)
        self._entities[newName] = self._entities.pop(oldName)
        
    def listEntities(self) -> str:
        """
        Returns:
            str: String containing names of all existing entities.
        """
        entity_names = list(self._entities.keys())
        return ', '.join(entity_names)

    def deleteRelation(self, relation: Relation) -> None:
        pass
    