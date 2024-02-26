from umleditor.mvc_model import Relation
from umleditor.mvc_model import Entity

def test_create_relation():
    rel = Relation("aggregation", Entity("ent1"), Entity("ent2"))
    assert rel

def test_get_source():
    rel = Relation("aggregation", Entity("ent1"), Entity("ent2"))
    assert rel.get_source().get_name() == "ent1"
    assert rel.get_source().get_name() != "ent2"

def test_get_destination():
    rel = Relation("aggregation", Entity("ent1"), Entity("ent2"))
    assert rel.get_destination().get_name() != "ent1"
    assert rel.get_destination().get_name() == "ent2"

def test_contains():
    rel = Relation("aggregation", Entity("ent1"), Entity("ent2"))
    assert rel.contains("ent1")
    assert rel.contains("ent2")
    assert not rel.contains("ent3")

def test_to_string():
    rel = Relation("aggregation", Entity("ent1"), Entity("ent2"))
    assert str(rel) == "ent1 -> aggregation -> ent2"
    assert str(rel) != "ent2 -> ent1"