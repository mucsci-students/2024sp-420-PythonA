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

from umleditor.mvc_controller.controller_input import read_file, read_line
import umleditor.mvc_controller.controller_output as controller_output
from umleditor.mvc_model.diagram import Diagram
from umleditor.mvc_model.entity import Entity, UML_Method
from umleditor.mvc_model.relation import Relation
from umleditor.mvc_model.custom_exceptions import CustomExceptions as CE

def serialize(diagram: Diagram, path: str) -> None:
    '''
    Serialize a diagram's entities and relations to a JSON file.

    #### Parameters:
    - `diagram` (Diagram): The diagram object containing entities and relations to be serialized.
    - `path` (str): The file path where the JSON file will be saved.
    '''
    # classes
    saved_classes = []
    for entity in diagram._entities.values():
        saved_class = {}
        # class name
        saved_class['name'] = entity._name
        # class fields
        saved_fields = []
        for field in entity._fields:
            saved_field = {}
            # class field name
            saved_field['name'] = field
            # class field type
            saved_field['type'] = 'undefined' #TODO
            saved_fields.append(saved_field)
        saved_class['fields'] = saved_fields
        # class method
        saved_methods = []
        for method in entity._methods:
            saved_method = {}
            # class method name
            saved_method['name'] = method._name
            # class method return_type
            saved_method['return_type'] = 'undefined' #TODO
            # class method params
            saved_params = []
            for param in method._params:
                saved_param = {}
                # class method param name
                saved_param['name'] = param
                # class method param type
                saved_param['type'] = 'undefined' # TODO
                saved_params.append(saved_param)
            saved_method['params'] = saved_params
            saved_methods.append(saved_method)
        saved_class['methods'] = saved_method
        saved_classes.append(saved_class)
    # relationships
    saved_relationships = []
    for relation in diagram._relations:
        saved_relationship = {}
        # relationship source
        saved_relationship['source'] = relation._source
        # relationship destination
        saved_relationship['destination'] = relation._destination
        # relationship type
        saved_relationship['type'] = relation._type
        saved_relationships.append(saved_relationship)
    try:
        obj = {'classes': saved_classes, 'relationships': saved_relationships}
        content = json.dumps(obj=obj, cls=CustomJSONEncoder)
    except Exception:
        raise CE.JsonEncodeError(filepath=path)
    controller_output.write_file(path=path, content=content)

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
    content = read_file(path)
    try:
        diagram_attributes = json.loads(content)
    except Exception:
        raise CE.JsonDecodeError(filepath=path)
    try:
        for attr_name, attr_obj in diagram_attributes.items():
            if attr_name == 'entities':
                for name, properties in attr_obj.items():
                    entity = Entity()
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