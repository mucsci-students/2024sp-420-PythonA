from umleditor.mvc_model import Relation, Entity

def test_create_relation():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type=type, source=source, destination=destination)
    assert rel is not None

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

def test_contains():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = next(iter(Relation.RELATIONSHIP_TYPE))
    rel = Relation(type, source, destination)
    assert rel.contains(source) == True
    assert rel.contains(destination) == True
    assert rel.contains(Entity("ent3")) == False

def test_to_string():
    source = Entity("ent1")
    destination = Entity("ent2")
    type = "aggregation"
    rel = Relation(type=type, source=source, destination=destination)
    assert str(rel) == "ent1 -> aggregation -> ent2"