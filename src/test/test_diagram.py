from umleditor.mvc_model.diagram import Diagram
from umleditor.custom_exceptions import CustomExceptions
import pytest
"""
These test that the basic functions for Diagram interact
with the other classes. The individual classes/functions
are tested more thoroughly in other test files.
"""

def test_create_diagram():
    dia = Diagram()
    assert dia

def test_has_entity_success():
    dia = Diagram()
    dia.add_entity('class')
    assert dia.has_entity('class') == True

def test_has_entity_error():
    dia = Diagram()
    assert dia.has_entity('entity') == False

def test_dia_add_entity_success():
    dia = Diagram()
    assert not dia.has_entity("entity")
    dia.add_entity("entity")
    assert dia.has_entity("entity")

def test_dia_add_entity_error():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityExistsError):
        dia.add_entity("entity")

# def test_dia_add_multiple_entities():
#     dia = Diagram()
#     assert not dia.has_entity("ent1")
#     assert not dia.has_entity("ent2")
#     assert not dia.has_entity("ent3")
#     dia.add_entity("ent1")
#     dia.add_entity("ent2")
#     assert dia.has_entity("ent1")
#     assert dia.has_entity("ent2")
#     assert not dia.has_entity("ent3")
#     dia.add_entity("ent3")
#     assert dia.has_entity("ent1")
#     assert dia.has_entity("ent2")
#     assert dia.has_entity("ent3")

def test_dia_get_entity_success():
    dia = Diagram()
    ent = dia.get_entity("entity")
    assert ent.get_name() == "entity"
    assert dia.has_entity("entity")

def test_dia_get_entity_error():
    dia = Diagram()
    assert not dia.has_entity("ent")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.get_entity("ent")

def test_dia_delete_entity_success():
    dia = Diagram()
    assert not dia.has_entity("entity2")
    dia.add_entity("entity2")
    assert dia.has_entity("entity2")
    dia.delete_entity("entity2")
    assert not dia.has_entity("entity2")

def test_dia_delete_entity_with_relationship():
    dia = Diagram()
    assert len(dia._relations) == 0
    dia.add_relation("class", "entity", "composition")
    assert len(dia._relations) == 1
    dia.delete_entity("class")
    assert len(dia._relations) == 0


def test_dia_delete_entity_error():
    dia = Diagram()
    assert not dia.has_entity("entity2")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_entity("entity2")

# def test_dia_delete_multiple_entities():
#     dia = Diagram()
#     dia.add_entity("ent6")
#     dia.add_entity("ent7")
#     dia.add_entity("ent8")
#     assert dia.has_entity("ent6")
#     assert dia.has_entity("ent7")
#     assert dia.has_entity("ent8")
#     dia.delete_entity("ent6")
#     dia.delete_entity("ent7")
#     assert not dia.has_entity("ent6")
#     assert not dia.has_entity("ent7")
#     assert dia.has_entity("ent8")
#     dia.delete_entity("ent8")
#     assert not dia.has_entity("ent6")
#     assert not dia.has_entity("ent7")
#     assert not dia.has_entity("ent8")

def test_dia_rename_entity_success():
    dia = Diagram()
    assert dia.has_entity("entity")
    assert not dia.has_entity("entity1")
    dia.rename_entity("entity", "entity1")
    assert not dia.has_entity("entity")
    assert dia.has_entity("entity1")

def test_dia_rename_entity_old_name_doesnt_exist():
    dia = Diagram()
    assert not dia.has_entity("entity2")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.rename_entity("entity2", "entity1")

def test_dia_rename_entity_new_name_already_exists():
    dia = Diagram()
    assert dia.has_entity("entity1")
    dia.add_entity("entity2")
    assert dia.has_entity("entity2")
    with pytest.raises(CustomExceptions.EntityExistsError):
        dia.rename_entity("entity1", "entity2")

# def test_dia_rename_multiple_entities():
#     dia = Diagram()
#     dia.add_entity("ent8")
#     dia.add_entity("ent9")
#     assert dia.has_entity("ent8")
#     assert dia.has_entity("ent9")
#     assert not dia.has_entity("ent10")
#     assert not dia.has_entity("ent11")
#     dia.rename_entity("ent8", "ent10")
#     dia.rename_entity("ent9", "ent11")
#     assert not dia.has_entity("ent8")
#     assert not dia.has_entity("ent9")
#     assert dia.has_entity("ent10")
#     assert dia.has_entity("ent11")

def test_dia_list_entity_details_success():
    dia = Diagram()
    result = "entity1:\nentity1's Fields:\n\nentity1's Methods:\nentity1's Relations:\n"
    assert dia.list_entity_details("entity1") == result

def test_dia_list_entity_details_error():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.list_entity_details("entity")

def test_dia_list_everything():
    dia = Diagram()
    result = "entity1:\nentity1's Fields:\n\nentity1's Methods:\nentity1's Relations:\n\nentity2:\nentity2's Fields:\n\nentity2's Methods:\nentity2's Relations:\n\n"
    assert dia.list_everything() == result

def test_dia_list_entities():
    dia = Diagram()
    result = "\nentity1, entity2"
    assert dia.list_entities() == result

def test_dia_list_relations():
    dia = Diagram()
    dia.add_relation("entity1", "entity2", "inheritance")
    result = ['entity1 -> inheritance -> entity2']
    assert dia.list_relations() == result

def test_dia_list_entity_relations():
    dia = Diagram()
    result = "entity1 -> inheritance -> entity2"
    assert dia.list_entity_relations("entity1") == result

def test_dia_add_relation_success():
    dia = Diagram()
    dia.add_entity("entity3")
    assert len(dia._relations) == 1
    dia.add_relation("entity2", "entity3", "aggregation")
    assert len(dia._relations) == 2

def test_dia_add_relation_self():
    dia = Diagram()
    with pytest.raises(CustomExceptions.SelfRelationError):
        dia.add_relation("entity1", "entity1", "realization")

def test_dia_add_relation_source_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.add_relation("entity", "entity1", "aggregation")

def test_dia_add_relation_destination_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.add_relation("entity1", "entity", "aggregation")

def test_dia_add_relation_that_already_exists():
    dia = Diagram()
    with pytest.raises(CustomExceptions.RelationExistsError):
        dia.add_relation("entity1", "entity2", "inheritance")

def test_dia_add_relation_invalid_type():
    dia = Diagram()
    with pytest.raises(CustomExceptions.InvalidRelationTypeError):
        dia.add_relation("entity1", "entity3", "relationship")

def test_dia_delete_relation_success():
    dia = Diagram()
    assert len(dia._relations) == 2
    dia.delete_relation("entity2", "entity3")
    assert len(dia._relations) == 1

def test_dia_delete_relation_source_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("entity", "entity2")

def test_dia_delete_relation_destination_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("entity2", "entity")

def test_dia_delete_relation_that_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.RelationDoesNotExistError):
        dia.delete_relation("entity1", "entity3")

def test_change_relation_type_success():
    dia = Diagram()
    dia.change_relation_type("entity1", "entity2", "realization")

def test_dia_change_relation_type_invalid_type():
    dia = Diagram()
    with pytest.raises(CustomExceptions.InvalidRelationTypeError):
        dia.change_relation_type("entity1", "entity2", "relationship")

def test_change_relation_type_source_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("entity", "entity3")

def test_change_relation_type_destination_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("entity3", "entity")

def test_change_relation_type_relation_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.RelationDoesNotExistError):
        dia.change_relation_type("entity1", "entity3", "realization")

def test_getInstance():
    dia = Diagram()
    assert dia.getInstance() == dia


