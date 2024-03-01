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
    for entity in diagram._entities:
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
        # class methods
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
        saved_class['methods'] = saved_methods
        saved_classes.append(saved_class)
    # relationships
    saved_relationships = []
    for relation in diagram._relations:
        saved_relationship = {}
        # relationship source
        saved_relationship['source'] = relation._source._name
        # relationship destination
        saved_relationship['destination'] = relation._destination._name
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
        obj = json.loads(content)
    except Exception:
        raise CE.JsonDecodeError(filepath=path)
    try:
        # classes
        loaded_classes = []
        for saved_class in obj['classes']:
            loaded_class = Entity()
            # class name
            loaded_class._name = saved_class['name']
            # class fields
            loaded_fields = []
            for saved_field in saved_class['fields']:
                loaded_field = str() # str is the type of field
                # class field name
                loaded_field = saved_field['name']
                # class field type
                # TODO: field type unused
                loaded_fields.append(loaded_field)
            loaded_class._fields = loaded_fields
            # class methods
            loaded_methods = []
            for saved_method in saved_class['methods']:
                loaded_method = UML_Method()
                # class method name
                loaded_method._name = saved_method['name']
                # class method return_type
                # TODO: return_type unused
                # class method params
                loaded_params = []
                for saved_param in saved_method['params']:
                    loaded_param = str() # str is the type of param
                    # class method param name
                    loaded_param = saved_param['name']
                    # class method param type
                    # TODO: type unused
                    loaded_params.append(loaded_param)
                loaded_method._params = loaded_params
                loaded_methods.append(loaded_method)
            loaded_class._methods = loaded_methods
            loaded_classes.append(loaded_class)
        diagram._entities = loaded_classes
        # relationships
        loaded_relationships = []
        for saved_relationship in obj['relationships']:
            loaded_relationship = Relation()
            # relationship source
            # loaded_relationship._source = saved_relationship['source']
            loaded_relationship._source = [entity for entity in loaded_classes if entity._name == saved_relationship['source']][0]
            # relationship destination
            # loaded_relationship._destination = saved_relationship['destination']
            loaded_relationship._destination = [entity for entity in loaded_classes if entity._name == saved_relationship['destination']][0]
            # relationship type
            loaded_relationship._type = saved_relationship['type']
            loaded_relationships.append(loaded_relationship)
        diagram._relations = loaded_relationships
    except Exception:
        raise CE.SavedDataError(filepath=path)