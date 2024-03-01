from .entity import Entity
from .custom_exceptions import CustomExceptions

class Relation:
    RELATIONSHIP_TYPE = ['aggregation', 'composition', 'inheritance', 'realization']

    def __init__(self, type=next(iter(RELATIONSHIP_TYPE)), source=Entity(), destination=Entity()):
        """
        Creates a relation between a source entity to a destination entity.
        
        Args:
            source (Entity): The entity at the start of the relation.
            destination (Entity): The entity at the end of the relation.
            type (str): The type of the relation - ['aggregation', 'composition', 'inheritance', 'realization'] 
            
        Raises:
            CustomExceptions.InvalidRelationTypeError: If the type of the relation is 
                not valid.
            
        Returns:
            None.
        """
        # check if the type is valid
        if type not in self.RELATIONSHIP_TYPE:
            raise CustomExceptions.InvalidRelationTypeError(type)
        self._source = source
        self._destination = destination
        self._type = type
    
    def get_source(self):
        """
        Returns the source entity of the the relation.
        
        Args:
            None.
            
        Raises:
            None.
        
        Returns:
            source (Entity): The source entity of the relation.
        """
        return self._source
    
    def get_destination(self):
        """
        Returns the destination entity of the relation.
        
        Args:
            None.
            
        Raises:
            None.
            
        Returns:
            destination (Entity): The destination entity of the relation.
        """
        return self._destination
    
    def set_type(self, new_type:str):
        if new_type not in self.RELATIONSHIP_TYPE:
            raise CustomExceptions.InvalidRelationTypeError(type)

        self._type = new_type


    def contains(self, name:str):
        """
        Checks if a given entity is part of the relation.

        Args:
            name(str): The entity to be checked.

        Returns:
            bool: Returns True if the entity is the source or the destination
                of the relation. Returns False if the entity is not in the relation.
        """
        if name == self._source.get_name() or name == self._destination.get_name():
            return True
        else:
            return False

    def __str__(self):
        """
        Returns a string representation of a relation.
        
        Args:
            None.
            
        Raises:
            None.
            
        Returns:
            str: A string representation of the relation.
        """
        return f'{self._source} -> {self._type} -> {self._destination}'
    
    def __eq__(self, other):
        '''Equality op overload
            
            Return: 
            True - all the fields in this == all the fields in other
            False - at least one field is different
        '''
        if self._source != other._source:
            return False
        
        if self._destination != other._destination:
            return False
        
        return True