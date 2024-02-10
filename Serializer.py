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

import Input
import Output
from Diagram import Diagram
from Entity import Entity
from Relation import Relation
from CustomExceptions import CustomExceptions as CE

def serialize(diagram: Diagram, path: str) -> None:
    '''
    Serialize a diagram's entities and relations to a JSON file.

    #### Parameters:
    - `diagram` (Diagram): The diagram object containing entities and relations to be serialized.
    - `path` (str): The file path where the JSON file will be saved.
    '''
    entities = {name: vars(obj) for name, obj in diagram._entities.items()}
    relations = []
    for x in diagram._relations:
        properties = vars(x)
        for property_name, property_val in properties.items():
            if isinstance(property_val, Entity):
                properties[property_name] = property_val.get_name()
        relations.append(properties)
    try:
        content = json.dumps(obj={'entities': entities, 'relations': relations}, cls=CustomJSONEncoder)
    except Exception:
        raise CE.JsonEncodeError(filepath=path)
    Output.write_file(path=path, content=content)

def deserialize(diagram: Diagram, path: str) -> None:
    '''
    Deserialize a diagram from a JSON file and populate its entities and relations.

    #### Parameters:
    - `diagram` (Diagram): The diagram object to populate with deserialized data.
    - `path` (str): The file path of the JSON file to deserialize.

    #### Raises:
    - (CustomExceptions.JsonDecodeError): If failed to decode the file
    - (CustomExceptions.SavedDataError): If file data is not consistent with the Diagram
    '''
    content = Input.read_file(path)
    try:
        diagram_attributes = json.loads(content)
    except Exception:
        raise CE.JsonDecodeError(filepath=path)
    try:
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
                        if isinstance(getattr(relation, property_name), Entity):
                            property_val = diagram._entities[property_val]
                        if isinstance(getattr(relation, property_name), set): # Because custom encoder save set as list
                            property_val = set(property_val)
                        setattr(relation, property_name, property_val)
                    diagram._relations.append(relation)
    except Exception:
        raise CE.SavedDataError(filepath=path)