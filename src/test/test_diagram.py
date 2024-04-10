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
    assert ent5
    assert ent5.get_name() == "ent4"
    assert ent5.get_name() != "ent5"
    assert dia.has_entity("ent4")

def test_dia_get_entity_error():
    dia = Diagram()
    assert not dia.has_entity("ent6")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.get_entity("ent6")

def test_dia_delete_entity_success():
    dia = Diagram()
    assert not dia.has_entity("ent6")
    dia.add_entity("ent6")
    assert dia.has_entity("ent6")
    dia.delete_entity("ent6")
    assert not dia.has_entity("ent6")

def test_dia_delete_entity_error():
    dia = Diagram()
    assert not dia.has_entity("ent7")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.delete_entity("ent7")

def test_dia_delete_multiple_entities():
    dia = Diagram()
    dia.add_entity("ent7")
    dia.add_entity("ent8")
    dia.add_entity("ent9")
    assert dia.has_entity("ent7")
    assert dia.has_entity("ent8")
    assert dia.has_entity("ent9")
    dia.delete_entity("ent7")
    dia.delete_entity("ent8")
    assert not dia.has_entity("ent7")
    assert not dia.has_entity("ent8")
    assert dia.has_entity("ent9")
    dia.delete_entity("ent9")
    assert not dia.has_entity("ent7")
    assert not dia.has_entity("ent8")
    assert not dia.has_entity("ent9")

def test_dia_rename_entity_success():
    dia = Diagram()
    dia.add_entity("ent10")
    assert dia.has_entity("ent10")
    assert not dia.has_entity("ent11")
    dia.rename_entity("ent10", "ent11")
    assert not dia.has_entity("ent10")
    assert dia.has_entity("ent11")

def test_dia_rename_entity_old_name_doesnt_exist():
    dia = Diagram()
    assert not dia.has_entity("ent12")
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.rename_entity("ent12", "ent13")

def test_dia_rename_entity_new_name_already_exists():
    dia = Diagram()
    assert not dia.has_entity("ent12")
    dia.add_entity("ent12")
    with pytest.raises(CustomExceptions.EntityExistsError):
        dia.rename_entity("ent11", "ent12")

def test_dia_rename_multiple_entities():
    dia = Diagram()
    dia.add_entity("ent13")
    dia.add_entity("ent14")
    assert dia.has_entity("ent13")
    assert dia.has_entity("ent14")
    assert not dia.has_entity("ent15")
    assert not dia.has_entity("ent16")
    dia.rename_entity("ent13", "ent15")
    dia.rename_entity("ent14", "ent16")
    assert not dia.has_entity("ent13")
    assert not dia.has_entity("ent14")
    assert dia.has_entity("ent15")
    assert dia.has_entity("ent16")

def test_dia_list_entity_details_success():
    dia = Diagram()
    result =
    assert dia.list_entity_details("ent1") == result

def test_dia_list_entity_details_error():
    dia = Diagram()
    with pytest.raises(CustomExceptions.EntityNotFoundError):
        dia.list_entity_details("entity")

def test_dia_list_everything():
    dia = Diagram()
    result =
    assert dia.list_everything() == result

def test_dia_add_relation():
    dia = Diagram()
    dia.add_entity("ent17")
    dia.add_entity("ent18")
    assert len(dia._relations) == 0
    dia.add_relation("ent17", "ent18", "aggregation")
    assert len(dia._relations) == 1

def test_dia_delete_relation():
    dia = Diagram()
    dia.add_entity("ent19")
    dia.add_entity("ent20")
    dia.add_relation("ent19", "ent20", "aggregation")
    assert len(dia._relations) == 2
    dia.delete_relation("ent19", "ent20")
    assert len(dia._relations) == 1
    