from umleditor.mvc_model import Relation, Entity, CustomExceptions
import pytest

def test_create_relation_success():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type=type, source=source, destination=destination)
    assert rel is not None

def test_create_relation_invalid_type():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = "relationship"
    with pytest.raises(CustomExceptions.InvalidRelationTypeError):
        rel = Relation(type=type, source=source, destination=destination)

def test_get_source():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type, source, destination)
    assert rel.get_source().get_name() == "ent1"
    assert rel.get_source().get_name() != "ent2"

def test_get_destination():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type, source, destination)
    assert rel.get_destination().get_name() == "ent2"
    assert rel.get_destination().get_name() != "ent1"

def test_contains_true():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type, source, destination)
    assert rel.contains(source.get_name()) == True
    assert rel.contains(destination.get_name()) == True
    
def test_contains_false():
    source = Entity("ent3")
    destination = Entity("ent4")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type, source, destination)
    assert rel.contains("ent5") == False

def test_to_string():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = "aggregation"
    rel = Relation(type=type, source=source, destination=destination)
    assert str(rel) == "ent1 -> aggregation -> ent2"