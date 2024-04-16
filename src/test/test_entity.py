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
    ent1.add_field("field2", "int")
    with pytest.raises(CustomExceptions.FieldExistsError):
        ent1.add_field("field2", "int")

def test_add_field_invalid_type():
    ent1 = Entity("entity1")
    with pytest.raises(CustomExceptions.FieldtypeNotFoundError):
        ent1.add_field("field3", "type")

def test_add_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field1", "int")
    ent1.add_field("field2", "string")
    ent1.add_field("field3", "bool")
    assert ("field1", "int") in ent1._fields
    assert ("field2", "string") in ent1._fields
    assert ("field3", "bool") in ent1._fields
    assert ("field4", "int") not in ent1._fields

def test_delete_field_success():
    ent1 = Entity("entity1")
    assert ("field1", "int") not in ent1._fields
    ent1.add_field("field1", "int")
    assert ("field1", "int") in ent1._fields
    ent1.delete_field("field1")
    assert ("field1", "int") not in ent1._fields

def test_delete_field_doesnt_exist():
    ent1 = Entity("entity1")
    assert ("field", "bool") not in ent1._fields
    with pytest.raises(CustomExceptions.FieldNotFoundError):
        ent1.delete_field("field1")

def test_delete_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field1", "int")
    ent1.add_field("field2", "string")
    ent1.add_field("field3", "bool")
    ent1.add_field("field4", "float")
    assert ("field1", "int") in ent1._fields
    assert ("field2", "string") in ent1._fields
    assert ("field3", "bool") in ent1._fields
    assert ("field4", "float") in ent1._fields
    ent1.delete_field("field1")
    ent1.delete_field("field2")
    ent1.delete_field("field3")
    assert ("field1") not in ent1._fields
    assert ("field2") not in ent1._fields
    assert ("field3") not in ent1._fields
    assert ("field4", "float") in ent1._fields

def test_rename_field():
    ent1 = Entity("entity1")
    assert ("field1","int") not in ent1._fields
    ent1.add_field("field1", "int")
    assert ("field1", "int") in ent1._fields
    assert ("field2", "int") not in ent1._fields
    ent1.rename_field("field1", "int","field2","int")
    assert ("field1","int") not in ent1._fields
    assert ("field2","int") in ent1._fields

def test_rename_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field1", "int")
    ent1.add_field("field2", "int")
    assert ("field1","int") in ent1._fields
    assert ("field2","int") in ent1._fields
    assert ("field3","int") not in ent1._fields
    assert ("field4","int") not in ent1._fields
    ent1.rename_field("field1", "int", "field3", "int")
    ent1.rename_field("field2", "int","field4", "int")
    assert ("field1", "int") not in ent1._fields
    assert ("field2", "int") not in ent1._fields
    assert ("field3", "int") in ent1._fields
    assert ("field4", "int") in ent1._fields

def test_add_method():
    ent1 = Entity("entity1")
    assert not any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    ent1.add_method("method1", "void")
    assert any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)


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

def test_rename_method_success():
    ent1 = Entity("entity1")
    ent1.add_method("method1","void")
    assert any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert not any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)
    ent1.rename_method("method1", "method2")
    assert not any(um._name == "method1" and um._return_type == "void" for um in ent1._methods)
    assert any(um._name == "method2" and um._return_type == "void" for um in ent1._methods)

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


# def test_add_param():
#     ent1 = Entity("entity1")
#     ent1.add_method("method1", "void")
#     method = ent1._methods[0]
#     method.add_parameters("param1", int)
#     assert ("param1", int) in method._params
#
#
# def test_add_multiple_param():
#     ent1 = Entity("entity1")
#     ent1.add_method("method1", "void")
#     method = ent1._methods[0]
#     method.add_parameters("param1", int)
#     method.add_parameters("param2", str)
#     method.add_parameters("param3", float)
#     method.add_parameters("param4", bool)
#     assert ("param1", int) in method._params
#     assert ("param2", str) in method._params
#     assert ("param3", float) in method._params
#     assert ("param4", bool) in method._params
#
# def test_delete_param():
#     ent1 = Entity("entity1")
#     ent1.add_method("method1", "void")
#     method = ent1._methods[0]
#     method.add_parameters("param1", int)
#     method.remove_parameters("param1", int)
#     assert ("param1",int) not in method._params
#
# def test_remove_multiple_param():
#     ent1 = Entity("entity1")
#     ent1.add_method("method1", "void")
#     method = ent1._methods[0]
#     method.add_parameters("param1", int)
#     method.add_parameters("param2", str)
#     method.add_parameters("param3", float)
#     method.add_parameters("param4", bool)
#
#     method.remove_parameters("param1", int)
#     method.remove_parameters("param2", str)
#     method.remove_parameters("param3", float)
#     method.remove_parameters("param4", bool)
#     assert ("param1", int) not in method._params
#     assert ("param2", str) not in method._params
#     assert ("param3", float) not in method._params
#     assert ("param4", bool) not in method._params
#
# def test_change_param():
#     ent1 = Entity("entity1")
#     ent1.add_method("method1", "void")
#     method = ent1._methods[0]
#     method.add_parameters("param1", int)
#     method.change_parameters("param1", int,"param2",int)
#     assert ("param2", int) in method._params


# def test_change_multiple_param():
#     ent1 = Entity("entity1")
#     ent1.add_method("method1", "void")
#     method = ent1._methods[0]
#     method.add_parameters("param1", int)
#     method.add_parameters("param2", str)
#     method.change_parameters("param1", int, "param3", float)
#     method.change_parameters("param2", str, "param4", bool)
#     assert ("param3", float) in method._params
#     assert ("param4", bool) in method._params

