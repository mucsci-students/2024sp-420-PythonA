def test_import_controller():
    from umleditor.mvc_controller import Controller
    
    assert Controller

def test_import_diagram():
    from umleditor.mvc_model import Diagram

    assert Diagram

def test_import_entity():
    from umleditor.mvc_model import Entity

    assert Entity

def test_import_relation():
    from umleditor.mvc_model import Relation

    assert Relation