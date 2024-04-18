# Primary: Danish
#Secondary: Zhang

from umleditor.mvc_model import Entity, CustomExceptions
import pytest


def test_create_entity():
    ent1 = Entity("entity1")
    assert ent1

def test_get_name():
    ent1 = Entity("entity1")
    assert ent1.get_name() == "entity1"
    assert ent1.get_name() != "entity2"

def test_set_name():
    ent1 = Entity("entity1")
    ent1.set_name("entity2")
    assert ent1.get_name() == "entity2"
    assert ent1.get_name() != "entity1"

def test_entity_equals():
    ent1 = Entity("entity1")
    ent2 = Entity("entity2")
    assert ent1 == ent1
    assert ent2 == ent2
    assert ent1 != ent2
    assert ent2 != ent1

def test_set_name():
    ent1 = Entity("entity1")
    assert ent1.get_name() == "entity1"
    assert ent1.get_name() != "entity2"
    ent1.set_name("entity2")
    assert ent1.get_name() != "entity1"
    assert ent1.get_name() == "entity2"

def test_add_field_success():
    ent1 = Entity("entity1")
    assert ("field1","int") not in ent1._fields
    ent1.add_field("field1", "int")
    assert ("field1","int") in ent1._fields

def test_add_field_already_exists():
    ent1 = Entity("entity1")
    assert ("field2", "int") not in ent1._fields
    ent1.add_field("field2", "int")
    assert ("field2", "int") in ent1._fields
    with pytest.raises(CustomExceptions.FieldExistsError):
        ent1.add_field("field2", "bool")

def test_add_field_invalid_type():
    ent1 = Entity("entity1")
    with pytest.raises(CustomExceptions.FieldtypeNotFoundError):
        ent1.add_field("field3", "type")

def test_add_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field4", "int")
    ent1.add_field("field5", "string")
    ent1.add_field("field6", "bool")
    assert ("field4", "int") in ent1._fields
    assert ("field5", "string") in ent1._fields
    assert ("field6", "bool") in ent1._fields
    assert ("field7", "int") not in ent1._fields

def test_delete_field_success():
    ent1 = Entity("entity1")
    assert ("field7", "int") not in ent1._fields
    ent1.add_field("field7", "int")
    assert ("field7", "int") in ent1._fields
    ent1.delete_field("field7")
    assert ("field7", "int") not in ent1._fields

def test_delete_field_doesnt_exist():
    ent1 = Entity("entity1")
    assert ("field7", "bool") not in ent1._fields
    with pytest.raises(CustomExceptions.FieldNotFoundError):
        ent1.delete_field("field7")

def test_delete_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field7", "int")
    ent1.add_field("field8", "string")
    ent1.add_field("field9", "bool")
    ent1.add_field("field10", "float")
    assert ("field7", "int") in ent1._fields
    assert ("field8", "string") in ent1._fields
    assert ("field9", "bool") in ent1._fields
    assert ("field10", "float") in ent1._fields
    ent1.delete_field("field7")
    ent1.delete_field("field8")
    ent1.delete_field("field9")
    assert ("field7") not in ent1._fields
    assert ("field8") not in ent1._fields
    assert ("field9") not in ent1._fields
    assert ("field10", "float") in ent1._fields

def test_rename_field():
    ent1 = Entity("entity1")
    assert ("field11","int") not in ent1._fields
    ent1.add_field("field11", "int")
    assert ("field11", "int") in ent1._fields
    assert ("field12", "int") not in ent1._fields
    ent1.rename_field("field11", "int","field12","int")
    assert ("field11","int") not in ent1._fields
    assert ("field12","int") in ent1._fields

def test_rename_field_old_name_doesnt_exist():
    ent1 = Entity("entity1")
    assert ("field13","int") not in ent1._fields
    with pytest.raises(CustomExceptions.FieldNotFoundError):
        ent1.rename_field("field13", "int","field2","int")

def test_rename_field_new_name_already_exists():
    ent1 = Entity("entity1")
    assert ("field14","string") not in ent1._fields
    ent1.add_field("field14", "string")
    assert ("field15", "string") not in ent1._fields
    ent1.add_field("field15", "string")
    with pytest.raises(CustomExceptions.FieldNotFoundError):
        ent1.rename_field("field14", "string","field15","string")

def test_rename_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field16", "int")
    ent1.add_field("field17", "int")
    assert ("field16","int") in ent1._fields
    assert ("field17","int") in ent1._fields
    assert ("field18","int") not in ent1._fields
    assert ("field19","int") not in ent1._fields
    ent1.rename_field("field16", "int", "field18", "int")
    ent1.rename_field("field17", "int","field19", "int")
    assert ("field16", "int") not in ent1._fields
    assert ("field17", "int") not in ent1._fields
    assert ("field18", "int") in ent1._fields
    assert ("field19", "int") in ent1._fields

def test_get_method_success():
    ent1 = Entity("entity1")
    ent2 = Entity("entity2")
    assert not any(um._name == "method" and um._return_type == "string" for um in ent1._methods)
    ent1.add_method("method", "string")
    assert ent1.get_method("method") == ent2.add_method("method")

def test_get_method_doesnt_exist():
    ent1 = Entity("entity1")
    assert not any(um._name == "method2" and um._return_type == "float" for um in ent1._methods)
    with pytest.raises(CustomExceptions.MethodNotFoundError):
        assert ent1.get_method("method2")

def test_add_method_success():
    ent1 = Entity("entity1")
    assert not any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    ent1.add_method("method1", "void")
    assert any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)

def test_add_method_already_exists():
    ent1 = Entity("entity1")
    assert not any(um._name == "method2" and um._return_type == "int" for um in ent1._methods)
    ent1.add_method("method2", "int")
    with pytest.raises(CustomExceptions.MethodExistsError):
        ent1.add_method("method2", "int")

def test_add_method_invalid_return_type():
    ent1 = Entity("entity1")
    with pytest.raises(CustomExceptions.MethodExistsError):
        ent1.add_method("method3", "type")

def test_add_mutliple_methods():
    ent1 = Entity("entity1")
    assert not any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method3" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method4" and um._return_type == "void" for um in ent1._methods)
    ent1.add_method("method1","void")
    ent1.add_method("method2", "void")
    ent1.add_method("method3","void")
    assert any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)
    assert any(um._name == "method3" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method4" and um._return_type == "void" for um in ent1._methods)

def test_delete_method_success():
    ent1 = Entity("entity1")
    ent1.add_method("method5", "bool")
    assert any(um._name == "method5" and um._return_type == "bool" for um in ent1._methods)
    ent1.delete_method("method5")
    assert not any(um._name == "method5" and um._return_type == "bool" for um in ent1._methods)

def test_delete_method_doesnt_exist():
    ent1 = Entity("entity1")
    assert not any(um._name == "method6" and um._return_type == "void" for um in ent1._methods)
    with pytest.raises(CustomExceptions.MethodNotFoundError):
        ent1.delete_method("method6")

def test_rename_method_success():
    ent1 = Entity("entity1")
    ent1.add_method("method1","void")
    assert any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)
    ent1.rename_method("method1", "method2")
    assert not any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)

def test_rename_method_old_name_doesnt_exist():
    ent1 = Entity("entity1")
    with pytest.raises(CustomExceptions.MethodNotFoundError):
        ent1.rename_method("method1", "method2")

def test_rename_method_new_name_already_exists():
    ent1 = Entity("entity1")
    ent1.add_method("method1", "void")
    ent1.add_method("method2", "void")
    with pytest.raises(CustomExceptions.MethodExistsError):
        ent1.rename_method("method1", "method2")

def test_rename_multiple_methods():
    ent1 = Entity("entity1")
    ent1.add_method("method1","void")
    ent1.add_method("method2","void")
    assert any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method3" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method4" and um._return_type == "void" for um in ent1._methods)
    ent1.rename_method("method1", "method3")
    ent1.rename_method("method2", "method4")
    assert not any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)
    assert any(um._name == "method3" and um._return_type == "void" for um in ent1._methods)
    assert any(um._name == "method4" and um._return_type == "void" for um in ent1._methods)


def test_add_param():
    ent1 = Entity("entity1")
    ent1.add_method("method1", "void")
    method = ent1._methods[0]
    method.add_parameters("param1")
    assert ("param1") in method._params


def test_add_multiple_param():
    ent1 = Entity("entity1")
    ent1.add_method("method1", "void")
    method = ent1._methods[0]
    method.add_parameters("param2")
    method.add_parameters("param3")
    method.add_parameters("param4")
    assert ("param2") in method._params
    assert ("param3") in method._params
    assert ("param4") in method._params

def test_delete_param():
    ent1 = Entity("entity1")
    ent1.add_method("method1", "void")
    method = ent1._methods[0]
    method.add_parameters("param1")
    method.remove_parameters("param1")
    assert ("param1") not in method._params

def test_remove_multiple_param():
    ent1 = Entity("entity1")
    ent1.add_method("method1", "void")
    method = ent1._methods[0]
    method.add_parameters("param1")
    method.add_parameters("param2")
    method.add_parameters("param3")
    method.add_parameters("param4")
    method.remove_parameters("param1")
    method.remove_parameters("param2")
    method.remove_parameters("param3")
    method.remove_parameters("param4")
    assert ("param1") not in method._params
    assert ("param2") not in method._params
    assert ("param3") not in method._params
    assert ("param4") not in method._params

def test_change_param():
    ent1 = Entity("entity1")
    ent1.add_method("method1", "void")
    method = ent1._methods[0]
    method.add_parameters("param1")
    method.change_parameters("param1","param2")
    assert ("param2") in method._params

def test_change_multiple_param():
    ent1 = Entity("entity1")
    ent1.add_method("method1", "void")
    method = ent1._methods[0]
    method.add_parameters("param1")
    method.add_parameters("param2")
    method.change_parameters("param1", "param3")
    method.change_parameters("param2", "param4")
    assert ("param3") in method._params
    assert ("param4") in method._params

