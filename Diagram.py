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

        
    def add_relation(self, source, destination):
        """
        Adds a relation between two Entities.
        
        Args:
            source (Entity): The entity that is the source of the relation.
            destination (Entity): The entity that is the destination of the relation.
            
        Raises:
            CustumExceptions.RelationExistsError: On attempt to add a relation
                that already exists between the source and the destination
                entities.
                
        Returns:
            The relation that was added.
        """
        for rel in self._relations:
            if rel.get_source() == source and rel.get_destination() == destination:
                raise CustomExceptions.RelationExistsError(source, destination)
        
        relationship = Relation(source, destination)
        self._relations.append(relationship)
        return relationship
    
    def delete_relation(self, source, destination):
        """
        Deletes a relation between two Entities.
        
        Args:
            source (Entity): The enitity that is the source of the relation.
            destination (Entity): The entity that is the destination of the relation.
        
        Raises:
            CustomExceptions.RelationDoesNotExistError: On attempt to delete a
            relation that does not exist between the source and the
            destination entities.
            
        Returns:
            A copy of the deleted relation.
        """
        for i, rel in enumerate(self._relations):
            if rel.get_source() == source and rel.get_destination() == destination:
                deleted_relation = self._relations.pop(i)
                return deleted_relation
        raise CustomExceptions.RelationDoesNotExistError(source, destination)

    def deleteRelation(self, relation: Relation) -> None:
        pass
    
