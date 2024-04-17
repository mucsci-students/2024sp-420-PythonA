from umleditor.mvc_model import Diagram
from umleditor.mvc_model import CustomExceptions
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
    assert not dia.has_entity("ent")
    dia.add_entity("ent")
    assert dia.has_entity("ent")

def test_dia_add_entity_error():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityExistsError):
        dia.add_entity("ent")

def test_dia_add_multiple_entities():
    dia = Diagram()
    assert not dia.has_entity("ent1")
    assert not dia.has_entity("ent2")
    assert not dia.has_entity("ent3")
    dia.add_entity("ent1")
    dia.add_entity("ent2")
    assert dia.has_entity("ent1")
    assert dia.has_entity("ent2")
    assert not dia.has_entity("ent3")
    dia.add_entity("ent3")
    assert dia.has_entity("ent1")
    assert dia.has_entity("ent2")
    assert dia.has_entity("ent3")

def test_dia_get_entity_success():
    dia = Diagram()
    assert not dia.has_entity("ent4")
    dia.add_entity("ent4")
    ent5 = dia.get_entity("ent4")
    assert ent5.get_name() == "ent4"
    assert ent5.get_name() != "ent5"
    assert dia.has_entity("ent4")

def test_dia_get_entity_error():
    dia = Diagram()
    assert not dia.has_entity("ent5")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.get_entity("ent5")

def test_dia_delete_entity_success():
    dia = Diagram()
    assert not dia.has_entity("ent5")
    dia.add_entity("ent5")
    assert dia.has_entity("ent5")
    dia.delete_entity("ent5")
    assert not dia.has_entity("ent5")

def test_dia_delete_entity_error():
    dia = Diagram()
    assert not dia.has_entity("ent5")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_entity("ent5")

def test_dia_delete_multiple_entities():
    dia = Diagram()
    dia.add_entity("ent6")
    dia.add_entity("ent7")
    dia.add_entity("ent8")
    assert dia.has_entity("ent6")
    assert dia.has_entity("ent7")
    assert dia.has_entity("ent8")
    dia.delete_entity("ent6")
    dia.delete_entity("ent7")
    assert not dia.has_entity("ent6")
    assert not dia.has_entity("ent7")
    assert dia.has_entity("ent8")
    dia.delete_entity("ent8")
    assert not dia.has_entity("ent6")
    assert not dia.has_entity("ent7")
    assert not dia.has_entity("ent8")

def test_dia_rename_entity_success():
    dia = Diagram()
    dia.add_entity("ent6")
    assert dia.has_entity("ent6")
    assert not dia.has_entity("ent7")
    dia.rename_entity("ent6", "ent7")
    assert not dia.has_entity("ent6")
    assert dia.has_entity("ent7")

def test_dia_rename_entity_old_name_doesnt_exist():
    dia = Diagram()
    assert not dia.has_entity("ent6")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.rename_entity("ent6", "ent8")

def test_dia_rename_entity_new_name_already_exists():
    dia = Diagram()
    assert dia.has_entity("ent1")
    assert dia.has_entity("ent2")
    with pytest.raises(CustomExceptions.EntityExistsError):
        dia.rename_entity("ent1", "ent2")

def test_dia_rename_multiple_entities():
    dia = Diagram()
    dia.add_entity("ent8")
    dia.add_entity("ent9")
    assert dia.has_entity("ent8")
    assert dia.has_entity("ent9")
    assert not dia.has_entity("ent10")
    assert not dia.has_entity("ent11")
    dia.rename_entity("ent8", "ent10")
    dia.rename_entity("ent9", "ent11")
    assert not dia.has_entity("ent8")
    assert not dia.has_entity("ent9")
    assert dia.has_entity("ent10")
    assert dia.has_entity("ent11")

def test_dia_list_entity_details_success():
    dia = Diagram()
    result = "ent1:\nent1's Fields:\n \nent1's Methods:\n ent1's Relations:\n "
    assert dia.list_entity_details("ent1") == result

def test_dia_list_entity_details_error():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.list_entity_details("entity")

def test_dia_list_everything():
    dia = Diagram()
    result = "y"
    assert dia.list_everything() == result

def test_dia_list_entities():
    dia = Diagram()
    result = "class, ent1, ent2, ent3, ent4, ent5, ent6, ent7, ent8, ent9, ent10, ent11, ent12, ent13, ent14, ent15, ent16"
    assert dia.list_entities() == result

def test_dia_list_relations():
    dia = Diagram()
    result = "y"
    assert dia.list_relations() == result

def test_dia_list_entity_relations():
    dia = Diagram()
    result = "y"
    assert dia.list_entity_relations() == result

def test_dia_add_relation_success():
    dia = Diagram()
    dia.add_entity("ent17")
    dia.add_entity("ent18")
    assert len(dia._relations) == 0
    dia.add_relation("ent17", "ent18", "aggregation")
    assert len(dia._relations) == 1

def test_dia_add_relation_source_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.add_relation("entity", "ent18", "aggregation")

def test_dia_add_relation_destination_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.add_relation("ent17", "entity", "aggregation")

def test_dia_add_relation_that_already_exists():
    dia = Diagram()
    with pytest.raises(CustomExceptions.RelationExistsError):
        dia.add_relation("ent17", "ent18", "aggregation")

def test_dia_add_relation_invalid_type():
    dia = Diagram()
    dia.add_entity("ent19")
    dia.add_entity("ent20")
    with pytest.raises(CustomExceptions.InvalidRelationTypeError):
        dia.add_relation("ent19", "ent20", "relationship")

def test_dia_delete_relation_success():
    dia = Diagram()
    dia.add_entity("ent20")
    dia.add_entity("ent21")
    dia.add_relation("ent20", "ent21", "aggregation")
    assert len(dia._relations) == 2
    dia.delete_relation("ent20", "ent21")
    assert len(dia._relations) == 1

def test_dia_delete_relation_source_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("entity", "ent21")

def test_dia_delete_relation_destination_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("ent20", "entity")

def test_dia_delete_relation_that_doesnt_exist():
    dia = Diagram()
    dia.add_entity("ent22")
    dia.add_entity("ent23")
    with pytest.raises(CustomExceptions.RelationDoesNotExistError):
        dia.delete_relation("ent22", "ent23")

def test_change_relation_type_success():
    dia = Diagram()
    dia.add_entity("ent24")
    dia.add_entity("ent25")
    dia.add_relation("ent24", "ent25", "aggregation")
    dia.change_relation_type("ent24", "ent25", "composition")

def test_dia_change_relation_type_invalid_type():
    dia = Diagram()
    with pytest.raises(CustomExceptions.InvalidRelationTypeError):
        dia.change_relation_type("ent24", "ent25", "relationship")

def test_change_relation_type_source_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("entity", "ent25")

def test_change_relation_type_destination_doesnt_exist():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_relation("ent24", "entity")

def test_change_relation_type_relation_doesnt_exist():
    dia = Diagram()
    dia.add_entity("ent26")
    dia.add_entity("ent27")
    with pytest.raises(CustomExceptions.RelationDoesNotExistError):
        dia.change_relation_type("ent26", "ent27", "composition")


