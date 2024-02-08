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

    def getEntity(self, name: str) -> None:
        """
        Retrieves an entity from the diagram if it exists.

        Args:
            name (str): The name of the entity to be retrieved.

        Returns:
            Entity or None: The Entity object if it exists, otherwise None
        """
        return self._entities.get(name, None)

    
    def deleteEntity(self, name: str) -> None:
        """
        Delete a given entity from our dictionary.

        Args:
            name (str): The name of the entity to be deleted.

        Raises:
            CustomExceptions.EntityNotFoundError: If an entity to be deleted does not exist.

        Returns:
            None
        """
        if name not in self._entities:
            raise CustomExceptions.EntityNotFoundError(name)
        
        # Check for relations involving the entity and remove them
        relations_to_remove = []
        for relation in self._relations:
            if relation.contains(self._entities[name]):
                relations_to_remove.append(relation)
        for relation in relations_to_remove:
            self._relations.remove(relation)
        
        # Remove the entity from the dictionary
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
        
    def add_att_to_entity(self, ent, attr):
        #TODO:  Comments
        ent_updating = self._entities[ent]
        ent_updating.add_attribute(attr)
        
    def listEntities(self) -> str:
        """
        Returns:
            str: String containing names of all existing entities.
        """
        entity_names = list(self._entities.keys())
        return ', '.join(entity_names)
    
    def list_relations(self) -> str:
        """
        Lists all existing relations as a string.

        Returns:
            str: A string representation of all existing relations.
        """
        relations_list = []
        for relation in self._relations:
            relations_list.append(str(relation))
        return '\n'.join(relations_list)

        
    def add_relation(self, source, destination) -> None:
        """
        Adds a relation between two Entities.
        
        Args:
            source (str): The name of the source entity
            destination (str): The name of the destination entity
            
        Raises:
            CustomExceptions.EntityNotFoundError: If either the source or the destination entity is not found.
            CustomExceptions.RelationExistsError: If a relation already exists between the source and destination entities.
        """
        # Check for valid source and destination
        if source not in self._entities:
            raise CustomExceptions.EntityNotFoundError(source)
        if destination not in self._entities:
            raise CustomExceptions.EntityNotFoundError(destination)
        # Check for duplicate relationship containing same source and destination
        for rel in self._relations:
            if rel.get_source() == self._entities[source] and rel.get_destination() == self._entities[destination]:
                raise CustomExceptions.RelationExistsError(source, destination)
        # Pass entity objects to relation and add relation to list of existing relations
        relationship = Relation(self._entities[source], self._entities[destination])
        self._relations.append(relationship)
    
    def delete_relation(self, source, destination) -> None:
        """
        Deletes a relation between two Entities.
        
        Args:
            source (str): The str that is the source of the relation.
            destination (str): The str that is the destination of the relation.
        
        Raises:
            CustomExceptions.EntityNotFoundError: If either the source or the destination entity is not found.
            CustomExceptions.RelationDoesNotExistError: If a relation does not exist between the source and destination entities.
        """
        # Check for valid source and destination
        if source not in self._entities:
            raise CustomExceptions.EntityNotFoundError(source)
        if destination not in self._entities:
            raise CustomExceptions.EntityNotFoundError(destination)
        # Look for matching relation to delete
        for i, rel in enumerate(self._relations):
            if rel.get_source() == self._entities[source] and rel.get_destination() == self._entities[destination]:
                del self._relations[i]
                return
        raise CustomExceptions.RelationDoesNotExistError(source, destination)
