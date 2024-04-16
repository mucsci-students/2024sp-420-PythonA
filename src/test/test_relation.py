from umleditor.mvc_model import Relation, Entity, CustomExceptions
import pytest

def test_import_entity():
    from src.umleditor.mvc_model import Entity
    assert Entity
    assert Entity.get_name
    assert Entity.set_name
    assert Entity.add_field
    assert Entity.delete_field
    assert Entity.rename_field
    assert Entity.get_method
    assert Entity.add_method
    assert Entity.delete_method
    assert Entity.rename_method
    assert Entity.list_fields
    assert Entity.list_methods

def test_import_custom_exceptions():
    from src.umleditor.mvc_model.custom_exceptions import CustomExceptions
    assert CustomExceptions

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
        Relation(type=type, source=source, destination=destination)

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

def test_set_type_success():
    source = Entity("ent3")
    destination = Entity("ent4")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type, source, destination)
    new_type = "composition"
    rel.set_type(new_type)
    assert rel._type != type
    assert rel._type == new_type

def test_set_type_invalid_type():
    source = Entity("ent3")
    destination = Entity("ent4")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type, source, destination)
    new_type = "relationship"
    with pytest.raises(CustomExceptions.InvalidRelationTypeError):
        rel.set_type(new_type)

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

def test_equal_without_type_true():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent1")
    destination2 = Entity("ent2")
    type2 = "composition"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.equal_without_type(rel2) == True
    assert rel2.equal_without_type(rel1) == True

def test_equal_without_type_same_source():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent1")
    destination2 = Entity("ent3")
    type2 = "composition"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.equal_without_type(rel2) == False
    assert rel2.equal_without_type(rel1) == False
    
def test_equal_without_type_same_destination():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent3")
    destination2 = Entity("ent2")
    type2 = "composition"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.equal_without_type(rel2) == False
    assert rel2.equal_without_type(rel1) == False

def test_equal_without_type_everything_different():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent3")
    destination2 = Entity("ent4")
    type2 = "composition"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.equal_without_type(rel2) == False
    assert rel2.equal_without_type(rel1) == False

def test_to_string():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = "aggregation"
    rel = Relation(type=type, source=source, destination=destination)
    assert str(rel) == "ent1 -> aggregation -> ent2"

def test_eq_everything_equal():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1,destination1)
    source2 = Entity("ent1")
    destination2 = Entity("ent2")
    type2 = "aggregation"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.__eq__(rel2) == True
    assert rel2.__eq__(rel1) == True


def test_eq_sources_not_equal():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent3")
    destination2 = Entity("ent2")
    type2 = "aggregation"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.__eq__(rel2) == False
    assert rel2.__eq__(rel1) == False


def test_eq_destinations_not_equal():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent1")
    destination2 = Entity("ent3")
    type2 = "aggregation"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.__eq__(rel2) == False
    assert rel2.__eq__(rel1) == False
    
def test_eq_types_not_equal():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "aggregation"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent1")
    destination2 = Entity("ent2")
    type2 = "composition"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.__eq__(rel2) == False
    assert rel2.__eq__(rel1) == False
    
def test_eq_everything_not_equal():
    source1 = Entity("ent1")
    destination1 = Entity("ent2")
    type1 = "inheritance"
    rel1 = Relation(type1, source1, destination1)
    source2 = Entity("ent3")
    destination2 = Entity("ent4")
    destination2 = Entity("ent4")
    type2 = "realization"
    rel2 = Relation(type2, source2, destination2)
    assert rel1.__eq__(rel2) == False
    assert rel2.__eq__(rel1) == False

