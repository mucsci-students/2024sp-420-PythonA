from umleditor.mvc_model import Relation

def test_create_relation():
    rel = Relation("ent1", "ent2")
    assert rel

def test_get_source():
    rel = Relation("ent1", "ent2")
    assert rel.get_source() == "ent1"
    assert rel.get_source() != "ent2"

def test_get_destination():
    rel = Relation("ent1", "ent2")
    assert rel.get_destination() != "ent1"
    assert rel.get_destination() == "ent2"

def test_contains():
    rel = Relation("ent1", "ent2")
    assert rel.contains("ent1")
    assert rel.contains("ent2")
    assert not rel.contains("ent3")

def test_to_string():
    rel = Relation("ent1", "ent2")
    assert str(rel) == "ent1 -> ent2"
    assert str(rel) != "ent2 -> ent1"