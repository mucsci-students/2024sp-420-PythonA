from math import e
from .entity import Entity, UML_Method
from .relation import Relation
from .custom_exceptions import CustomExceptions

class Diagram:
    def __init__(self) -> None:
        self._entities = {}
        self._relations = []

    def add_entity(self, name: str):
        """
        Adds an entity with the given name to the Diagram.

        Args:
            name (str): The name of the entity to add.

        Raises:
            CustomExceptions.EntityExistsError: If an entity
                with the same name already exists.

        Returns:
            None
        """
        if name in self._entities:
            raise CustomExceptions.EntityExistsError(name)
        else:
            self._entities[name] = Entity(name)

    def get_entity(self, name: str):
        """
        Retrieves an entity from the diagram if it exists.

        Args:
            name (str): The name of the entity to be retrieved.
        
        Raises:
            CustomExceptions.EntityNotFoundError if the entity requested does not exist
            
        Returns:
            Entity: If the entity exists.
            None: If the entity does not exist.
        """
        entity = self._entities.get(name, None)
        if entity is None:
            raise CustomExceptions.EntityNotFoundError(name)
        else:    
            return entity

    
    def delete_entity(self, name: str):
        """
        Delete a given entity from the diagram.

        Args:
            name (str): The name of the entity to be deleted.

        Raises:
            CustomExceptions.EntityNotFoundError: If an entity to be deleted
                does not exist.

        Returns:
            None
        """
        if name not in self._entities:
            raise CustomExceptions.EntityNotFoundError(name)
        
        # Check for relations involving the entity and remove them
        else:
            relations_to_remove = []
            for rel in self._relations:
                if rel.contains(self._entities[name]):
                    relations_to_remove.append(rel)
            for rel in relations_to_remove:
                self._relations.remove(rel)
        
            # Remove the entity from the dictionary
            del self._entities[name]


    def rename_entity(self, old_name: str, new_name: str):
        """
        Rename a given entity with a new name.

        Args:
            old_name (str): The current name of the entity to be renamed.
            new_name (str): The new name for the entity.

        Raises:
            CustomExceptions.EntityNotFoundError: If an entity with the old name
                does not exist.
            CustomExceptions.EntityExistsError: If an entity with the new name
                already exists.

        Returns:
            None
        """
        if old_name not in self._entities:
            raise CustomExceptions.EntityNotFoundError(old_name)
        elif new_name in self._entities:
            raise CustomExceptions.EntityExistsError(new_name)
        # Update key
        else:
            entity = self._entities[old_name]
            entity.set_name(new_name)
            self._entities[new_name] = self._entities.pop(old_name)
        
    def list_everything(self):
        """
        Returns a representation of the entire diagram.

        Returns:
            str: A templated representation of all entities, their attributes,
                and their relations.
        """
        result = ""
        for entity in self._entities.values():
            result += self.list_entity_details(entity.get_name()) + "\n"
        return result
        
    def list_entity_details(self, entity_name):
        """
        Returns the attributes and relations of the entity.
        
        Args:
            entity_name (str): The name of the entity to get details of.
            
        Raises:
            None
            
        Returns:
            str: A templated string containing the attributes and relations.
        """
        if not self._entities.__contains__(entity_name):
            raise CustomExceptions.EntityNotFoundError(entity_name)
        else:
            entity = self._entities[entity_name]
            att = entity._attributes
            rels = [rel for rel in self._relations if rel.contains(entity)]
            result ="\n" + entity_name + "'s Attributes:\n"
            att_string = ', '.join(att)
            result2 = entity_name + "'s Relations:\n"
            rel_string = ', '.join(str(rel) for rel in rels)
            return result + att_string + "\n" + result2 + rel_string

    def list_entities(self):
        """
        Returns the entities in the relation.
        
        Returns:
            str: String containing names of all existing entities.
        """
        entity_names = list(self._entities.keys())
        return '\n' + ', '.join(entity_names)
    
    def list_relations(self):
        """
        Lists all existing relations as a string.

        Returns:
            str: A string representation of all existing relations.
        """
        relations_list = []
        for rel in self._relations:
            relations_list.append(str(rel))
        return '\n'.join(relations_list)

        
    def add_relation(self,source, destination, type):
        """
        Adds a relation between two Entities.
        
        Args:
            source (str): The name of the source entity.
            destination (str): The name of the destination entity.
            type (str): The type of the relation.
            
        Raises:
            CustomExceptions.EntityNotFoundError: If either the source or the
                destination entity are not found.
            CustomExceptions.RelationExistsError: If a relation already exists
                between the source and destination entities.
            CustomExceptions.InvalidRelationTypeError: If the relation type is
                not valid.
        """
        # Check for valid relationship type
        if type not in Relation.RELATIONSHIP_TYPE:
            raise CustomExceptions.InvalidRelationTypeError(type)
        
        # Check for valid source and destination
        if source not in self._entities:
            raise CustomExceptions.EntityNotFoundError(source)
        elif destination not in self._entities:
            raise CustomExceptions.EntityNotFoundError(destination)
        # Check for duplicate relationship containing same source and destination
        else:
            for rel in self._relations:
                if rel.get_source() == self._entities[source] and rel.get_destination() == self._entities[destination]:
                    raise CustomExceptions.RelationExistsError(source, destination)
            # Pass entity objects to relation and add relation to list of existing relations
            relationship = Relation(type, self._entities[source], self._entities[destination])
            self._relations.append(relationship)
    
    def delete_relation(self, source, destination):
        """
        Deletes a relation between two Entities.
        
        Args:
            source (str): The name of the source entity.
            destination (str): The name of the destination entity.
        
        Raises:
            CustomExceptions.EntityNotFoundError: If either the source or the
                destination entity is not found.
            CustomExceptions.RelationDoesNotExistError: If a relation does not
                exist between the source and destination entities.
        """
        # Check for valid source and destination
        if source not in self._entities:
            raise CustomExceptions.EntityNotFoundError(source)
        elif destination not in self._entities:
            raise CustomExceptions.EntityNotFoundError(destination)
        # Look for matching relation to delete
        else:
            for i, rel in enumerate(self._relations):
                if rel.get_source() == self._entities[source] and rel.get_destination() == self._entities[destination]:
                    del self._relations[i]
                    return
        raise CustomExceptions.RelationDoesNotExistError(source, destination)
    
    def change_relation_type(self, source, destination, new_type):
        """
        Changes the type of a relation between two Entities.
        
        Args:
            source (str): The name of the source entity.
            destination (str): The name of the destination entity.
            new_type (str): The new type of the relation to change.
        
        Raises:
            CustomExceptions.EntityNotFoundError: If either the source or the
                destination entity is not found.
            CustomExceptions.RelationDoesNotExistError: If a relation does not
                exist between the source and destination entities.
            CustomExceptions.InvalidRelationTypeError: If the relation type to 
            is change not valid.
        """
        # Check for valid relationship type
        if new_type not in Relation.RELATIONSHIP_TYPE:
            raise CustomExceptions.InvalidRelationTypeError(new_type)
        
        # Check for valid source and destination
        for rel in self._relations:
            if rel.get_source() == self._entities[source] and rel.get_destination() == self._entities[destination]:
                rel._type = new_type
                return
        raise CustomExceptions.RelationDoesNotExistError(source, destination)
    
