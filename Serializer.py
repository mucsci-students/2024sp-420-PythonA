import json

class CustomJSONEncoder(json.JSONEncoder):
    '''
    a custom JSON encoder that returns a list when it encounters a set
    '''
    def default(self, obj):
        '''
        The `default` method is a custom implementation within a class that inherits from the `json.JSONEncoder` class in Python.
        It enhances the JSON serialization process by providing special handling for sets.
        '''
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

from Diagram import Diagram
from Entity import Entity
from Relation import Relation

class Serializer:
    def __init__(self) -> None:
        pass

    def serialize(self, diagram: Diagram, path: str) -> bool:
        '''
        Serialize a diagram's entities and relations to a JSON file.

        # Parameters:
        - `diagram` (Diagram): The diagram object containing entities and relations to be serialized.
        - `path` (str): The file path where the JSON file will be saved.

        # Returns:
        - (bool): True if the serialize operation is successful, False otherwise.
        '''
        # TODO: Change error handling after error log is complete
        entities = {name: vars(obj) for name, obj in diagram._entities.items()}
        relations = [vars(x) for x in diagram._relations]
        try:
            self.__write(path=path, content=json.dumps(obj={'entities': entities, 'relations': relations}, cls=CustomJSONEncoder))
        except Exception:
            return False
        return True

    def deserialize(self, diagram: Diagram, path: str) -> bool:
        '''
        Deserialize a diagram from a JSON file and populate its entities and relations.

        # Parameters:
        - `diagram` (Diagram): The diagram object to populate with deserialized data.
        - `path` (str): The file path of the JSON file to deserialize.

        # Returns:
        - (bool): True if the deserialize operation is successful, False otherwise.
        '''
        # TODO: Change error handling after error log is complete
        try:
            diagram_attributes = json.loads(self.__read(path))
        except Exception:
            return False
        for attr_name, attr_obj in diagram_attributes.items():
            if attr_name == 'entities':
                for name, properties in attr_obj.items():
                    entity = Entity(name='dummy') # TODO: Need a default constructor without parameter
                    for property_name, property_val in properties.items():
                        if isinstance(getattr(entity, property_name), set): # Because custom encoder save set as list
                            property_val = set(property_val)
                        setattr(entity, property_name, property_val)
                    diagram._entities[name] = entity
            elif attr_name == 'relations':
                for properties in attr_obj:
                    relation = Relation()
                    for property_name, property_val in properties.items():
                        if isinstance(getattr(relation, property_name), set): # Because custom encoder save set as list
                            property_val = set(property_val)
                        setattr(relation, property_name, property_val)
                    diagram._relations.append(relation)
        return True

    def __read(self, path: str) -> str:
        '''
        Reads the contents of a file and returns the content as a string.

        # Parameters:
        - `path` (str): The path to the file to be read.

        # Returns:
        - (str): The content of the file as a string.

        # Raises:
        - `FileNotFoundError`: If the specified file is not found.
        - `IOError`: If there is an issue reading the file.
        - Other exceptions: Any other exceptions that may occur during the file reading process.
        '''
        return open(path, 'r').read()
    
    def __write(self, path: str, content: str) -> None:
        '''
        Writes the specified content to a file at the given path.

        # Parameters:
        - `path` (str): The path to the file to be written.
        - `content` (str): The content to be written to the file.

        # Returns:
        - None

        # Raises:
        - `FileNotFoundError`: If the specified file is not found.
        - `IOError`: If there is an issue writing to the file.
        - Other exceptions: Any other exceptions that may occur during the file writing process.
        '''
        open(path, 'w').write(content)