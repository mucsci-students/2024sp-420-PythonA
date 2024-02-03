import json

from Diagram import Diagram
from Entity import Entity
from Relation import Relation

class Serializer:
    def __init__(self) -> None:
        pass

    def serialize(self, diagram: Diagram, path: str) -> None:
        '''
        Serialize a diagram's entities and relations to a JSON file.

        Parameters:
        - diagram (Diagram): The diagram object containing entities and relations to be serialized.
        - path (str): The file path where the JSON file will be saved.

        Returns:
        None

        Raises:
        - Any exceptions raised during JSON encoding or file writing.

        Usage:
        '''
        entities = {name: vars(obj) for name, obj in diagram._entities.items()}
        relations = [vars(x) for x in diagram._relations]
        self.__write(path=path, content=json.dumps({'entities': entities, 'relations': relations}))

    def deserialize(self, diagram: Diagram, path: str) -> None:
        '''
        Deserialize a diagram from a JSON file and populate its entities and relations.

        Parameters:
        - diagram (Diagram): The diagram object to populate with deserialized data.
        - path (str): The file path of the JSON file to deserialize.

        Returns:
        None

        Raises:
        - Any exceptions raised during JSON decoding or file reading.

        Usage:
        '''
        for attr_name, attr_obj in json.loads(self.__read(path)).items():
            if attr_name == 'entities':
                for name, properties in attr_obj.items():
                    entity = Entity('dummy') # TODO: Need a default constructor without parameter
                    for property_name, property_val in properties.items():
                        setattr(entity, property_name, property_val)
                    diagram._entities[name] = entity
            elif attr_name == 'relations':
                for properties in attr_obj:
                    relation = Relation()
                    for property_name, property_val in properties.items():
                        setattr(relation, property_name, property_val)
                    diagram._relations.append(relation)

    def __read(self, path: str) -> str:
        return open(path, 'r').read()
    
    def __write(self, path: str, content: str) -> None:
        with open(path, 'w') as file:
            file.write(content)