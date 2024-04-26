# Primary: Danish
# Secondary: Zhang
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

from umleditor.mvc_controller.controller_input import read_file
import umleditor.mvc_controller.controller_output as controller_output
from umleditor.mvc_model.diagram import Diagram
from umleditor.mvc_model.entity import Entity, UML_Method
from umleditor.mvc_model.relation import Relation
from umleditor.custom_exceptions import CustomExceptions as CE


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
        # class
        saved_class = {}; saved_classes.append(saved_class)
        # class name
        saved_class['name'] = entity._name
        # class fields
        saved_fields = []; saved_class['fields'] = saved_fields
        for field_name, field_type in entity._fields:
            # class field
            saved_field = {}; saved_fields.append(saved_field)
            # class field name
            saved_field['name'] = field_name
            # class field type
            saved_field['type'] = field_type
        # class methods
        saved_methods = []; saved_class['methods'] = saved_methods
        for method in entity._methods:
            # class method
            saved_method = {}; saved_methods.append(saved_method)
            # class method name
            saved_method['name'] =method._name
            # class method return_type
            saved_method['return_type'] = method._return_type
            # class method params
            saved_params = [];saved_method['params'] = saved_params
            for param_name in method._params:
                # class method param
                saved_param = {}; saved_params.append(saved_param)
                # class method param name
                saved_param['name'] = param_name
                # class method param type
                # saved_param['type'] = param_type if param_type else 'None'
        if hasattr(entity, '_location') and entity._location:
            saved_class['position'] = {'x': entity._location[0], 'y': entity._location[1]}
              
    # relationships
    saved_relationships = []
    for relation in diagram._relations:
        # relationship
        saved_relationship = {}; saved_relationships.append(saved_relationship)
        # relationship source
        saved_relationship['source'] = relation._source._name
        # relationship destination
        saved_relationship['destination'] = relation._destination._name
        # relationship type
        saved_relationship['type'] = relation._type

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
            # class
            loaded_class = Entity()
            # class name
            loaded_class._name = saved_class['name']
            # class fields
            loaded_fields = []
            for saved_field in saved_class['fields']:
                # field name
                field_name = saved_field['name']
                # field type
                field_type_str = saved_field['type']
                # field_type = type_mapping.get(field_type_str, str)

                loaded_field = (field_name, field_type_str)
                loaded_fields.append(loaded_field)

            # Assign the reconstructed list of fields to the loaded class
            loaded_class._fields = loaded_fields

            # class methods
            loaded_methods = []
            for saved_method in saved_class['methods']:
                # class method
                loaded_method = UML_Method()
                # class method name
                loaded_method._name = saved_method['name']
                # class method return_type
                loaded_method._return_type = None if saved_method['return_type'] == 'None' else saved_method[
                    'return_type']
                # class method params
                loaded_params = []
                for saved_param in saved_method['params']:
                    # Extracting param name and type (as string)
                    param_name = saved_param['name']
                    # param_type = None if saved_param['type'] == 'None' else saved_param['type']
                    # Append tuple of param name and type
                    loaded_params.append(param_name)
                loaded_method._params = loaded_params
                loaded_methods.append(loaded_method)
            loaded_class._methods = loaded_methods
            
            if 'position' in saved_class:
                loaded_class._location = [saved_class['position']['x'], saved_class['position']['y']]



            loaded_classes.append(loaded_class)
        diagram._entities = loaded_classes
        # relationships
        loaded_relationships = []
        for saved_relationship in obj['relationships']:
            # relationship
            loaded_relationship = Relation()
            # relationship source
            for entity in loaded_classes:
                if entity._name == saved_relationship['source']:
                    loaded_relationship._source = entity
            # relationship destination
            for entity in loaded_classes:
                if entity._name == saved_relationship['destination']:
                    loaded_relationship._destination = entity
            # relationship type
            loaded_relationship._type = saved_relationship['type']
            loaded_relationships.append(loaded_relationship)
        diagram._relations = loaded_relationships
    except Exception:
        raise CE.SavedDataError(filepath=path)
