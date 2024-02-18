from .entity import Entity

class Relation:
    def __init__(self, source=Entity(), destination=Entity()):
        """
        Creates a relation between a source entity to a destination entity.
        
        Args:
            source (Entity): The entity at the start of the relation.
            destination (Entity): The entity at the end of the relation.
            
        Raises:
            None.
            
        Returns:
            None.
        """
        self._source = source
        self._destination = destination
    
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
    
    def contains(self, entity: Entity):
        """
        Checks if a given entity is part of the relation.

        Args:
            entity (Entity): The entity to be checked.

        Returns:
            bool: Returns True if the entity is the source or the destination
                of the relation. Returns False if the entity is not in the relation.
        """
        if entity == self._source or entity == self._destination:
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
        return f'{self._source} -> {self._destination}'
