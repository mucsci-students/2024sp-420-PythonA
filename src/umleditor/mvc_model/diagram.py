from math import e
from .entity import Entity, UML_Method
from .relation import Relation
from .custom_exceptions import CustomExceptions

class Diagram:
    #Singleton Design Pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Diagram, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):  # Prevents reinitialization
            self._entities: list[Entity] = []
            self._relations: list[Relation] = []
            self._initialized = True  # Mark as initialized

    #===============================================================================#
                                #Entity Methods
    #===============================================================================#

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
        if self.has_entity(name):
                raise CustomExceptions.EntityExistsError(name)
        self._entities.append(Entity(name))

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
        dummy = Entity(name)
        entity = self._entities[self._entities.index(dummy)] if self.has_entity(name) else None
        if entity is None:
            raise CustomExceptions.EntityNotFoundError(name)    
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
        entity = self.get_entity(name)
        
        # Check for relations involving the entity and remove them
        relations_to_remove = []
        for rel in self._relations:
            if rel.contains(name):
                relations_to_remove.append(rel)
        for rel in relations_to_remove:
            self._relations.remove(rel)
    
        self._entities.remove(entity)


    def has_entity(self, name:str) -> bool:
        '''Returns true if the entity exists in this diagram, false otherwise'''

        for e in self._entities:
            if e.get_name() == name:
                return True
        return False
    

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
        ent = self.get_entity(old_name)

        if self.has_entity(new_name):
            raise CustomExceptions.EntityExistsError(new_name)        
        ent.set_name(new_name)   

    #===============================================================================#
                                #List Methods
    #===============================================================================#

    def list_everything(self):
        """
        Returns a representation of the entire diagram.

        Returns:
            str: A templated representation of all entities, their attributes,
                and their relations.
        """
        result = ""
        for entity in self._entities:
            result += self.list_entity_details(entity.get_name()) + "\n"
        return result
        
    def list_entity_details(self, entity_name):
        """
        Returns the fields, methods, params, and relations of the entity.
        
        Args:
            entity_name (str): The name of the entity to get details of.
            
        Raises:
            CustomExceptions.EntityNotFoundError: If an entity with the old name
                does not exist.
            
        Returns:
            str: A templated string containing the fields, methods, params
                and relations of an entity.
        """

        ent = self.get_entity(entity_name)
        fields = entity_name +":\n" + entity_name + "'s Fields:\n" + ent.list_fields() + '\n'
        methods = entity_name + "'s Methods:\n" + ent.list_methods()
        relations = entity_name + "'s Relations:\n" + self.list_entity_relations(entity_name)
        return fields + methods + relations

    def list_entities(self):
        """

        Returns the entities in the relation.
        
        Returns:
            str: String containing names of all existing entities.
        """
        entity_names = list(str(e) for e in self._entities)
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
    
    def list_entity_relations(self, name:str):
        ''' Lists all relations that contain a specific entity
        
            Return: A string containing all relations
        '''
        relations_list = []
        for rel in self._relations:
            if(rel.contains(name)):
                relations_list.append(str(rel))
        return '\n'.join(relations_list)

    #===============================================================================#
                                #Relation Methods
    #===============================================================================#
        
    def add_relation(self,source:str, destination:str, type:str):
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
        src = self.get_entity(source)
        dst = self.get_entity(destination)

        if src == dst:
            raise CustomExceptions.SelfRelationError(source)
        
        to_add = Relation(type, src, dst)
        for rel in self._relations:
            if rel.equal_without_type(to_add):
                raise CustomExceptions.RelationExistsError(source, destination)
        # Pass entity objects to relation and add relation to list of existing relations
        self._relations.append(to_add)
    
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
        src = self.get_entity(source)
        dst = self.get_entity(destination)
        # Look for matching relation to delete

        for i, rel in enumerate(self._relations):
            if rel.get_source() == src and rel.get_destination() == dst:
                del self._relations[i]
                return
        raise CustomExceptions.RelationDoesNotExistError(source, destination)

    def change_relation_type(self, source:str, destination:str, new_type:str):
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
        src = self.get_entity(source)
        dst = self.get_entity(destination)

        # Check for valid source and destination
        for rel in self._relations:
            if rel.get_source() == src and rel.get_destination() == dst:
                rel.set_type(new_type)
                return
        raise CustomExceptions.RelationDoesNotExistError(source, destination)
    
    def edit_relation(self, old_src: str, old_dst: str, old_type: str,
                      new_src:str, new_dst:str, new_type:str):
        """
        This method allows for editing an existing relation between two entities by modifying their source,
        destination, or type. If the input parameters remain unchanged, no action is taken.

        Args:
            old_src (str): The original source entity.
            old_dst (str): The original destination entity.
            old_type (str): The original type of relation.
            new_src (str): The new source entity.
            new_dst (str): The new destination entity.
            new_type (str): The new type of relation.
        """
        src = self.get_entity(new_src)
        dst = self.get_entity(new_dst)
        # If input unchanged, return
        if old_src == new_src and old_dst == new_dst and old_type == new_type:
            return
        # If src, dst same attempt to change relation type
        elif old_src == new_src and old_dst == new_dst:
            self.change_relation_type(new_src, new_dst, new_type)
        # Otherwise new relation T.F. add then delete
        else:
            self.add_relation(new_src, new_dst, new_type)
            self.delete_relation(old_src, old_dst)
            
    def getInstance(cls):
        """
        Returns the singleton instance of the Diagram class.
        
        Returns:
            Diagram: The singleton instance.
        """
        if not cls._instance:
            cls._instance = Diagram()
        return cls._instance    
    
