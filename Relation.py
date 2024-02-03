from Entity import Entity

class Relation:
    def __init__(self, source, destination):
        """
        Creates a relation from source and destination.
        """
        self._source = source
        self._destination = destination
        
    def get_source(self):
        """
        Returns the source.
        """
        return self._source
    
    def get_destination(self):
        """
        Returns the destination.
        """
        return self._destination

    def __str__(self):
        """
        Returns a string representation of a relation.
        """
        return f'{self._source} -> {self._destination}'
