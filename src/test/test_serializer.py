# Primary: Danish
# Secondary: Zhang

import os
from umleditor.mvc_controller.serializer import serialize, deserialize
from umleditor.mvc_model.diagram import Diagram
from umleditor.mvc_model.entity import Entity
from umleditor.mvc_model.relation import Relation

path = os.path.join(os.path.dirname(__file__), '../', '../', 'save')
if not os.path.exists(path):
    os.makedirs(path)
path = os.path.join(path, 'test' + '.json')

def test_empty():
    dia = Diagram()
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1', "int")
    load_dia.get_entity('Entity2').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field2', "int")
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

def test_entities():
    dia = Diagram()
    dia.add_entity('Class9')
    dia.add_entity('Class0')
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field2',"int")
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class9')
    assert load_dia.has_entity('Class0')

def test_relations():
    dia = Diagram()
    dia.add_entity('Class1')
    dia.add_entity('Class2')
    dia.add_relation('Class1', 'Class2', 'composition')
    dia.add_relation('Class2', 'Class1', 'inheritance')
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field2',"string")
    load_dia.get_entity('Entity2').add_field('Field3',"bool")
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class1')
    assert load_dia.has_entity('Class2')
    assert Relation('composition', Entity('Class1'), Entity('Class2')) in load_dia._relations
    assert Relation('inheritance', Entity('Class2'), Entity('Class1')) in load_dia._relations


def test_fields():
    dia = Diagram()
    dia.add_entity('Class3')
    dia.add_entity('Class4')
    dia.get_entity('Class3').add_field('Field1', "int")
    dia.get_entity('Class3').add_field('Field2', "string")
    dia.get_entity('Class4').add_field('Field1', "float")
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field2',"string")
    load_dia.get_entity('Entity2').add_field('Field3',"float")
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class1')
    assert load_dia.has_entity('Class2')
    assert 'Field1',"int" in load_dia.get_entity('Class1')._fields
    assert 'Field2',"string" in load_dia.get_entity('Class1')._fields
    assert 'Field1',"float" in load_dia.get_entity('Class2')._fields

def test_methods():
    dia = Diagram()
    dia.add_entity('Class5')
    dia.add_entity('Class6')
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field1', "int")
    load_dia.get_entity('Entity2').add_field('Field2',"float")
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')
    
    assert load_dia.has_entity('Class5')
    assert load_dia.has_entity('Class6')
    assert 'Param1', "int" in load_dia.get_entity('Class6').add_method("Param1", "int")
    assert 'Param1', "int" in load_dia.get_entity('Class6').add_method("Param1", "int")
    assert 'Param2', "int" in load_dia.get_entity('Class6').add_method("Param2", "int")
    assert 'Param3', "int" in load_dia.get_entity('Class6').add_method("Param3", "int")

def test_all_together():
    dia = Diagram()
    dia.add_entity('Class7')
    dia.add_entity('Class8')
    dia.add_relation('Class7', 'Class8', 'composition')
    dia.add_relation('Class8', 'Class7', 'inheritance')
    dia.get_entity('Class7').add_field('Field1',"int")
    dia.get_entity('Class7').add_field('Field2',"int")
    dia.get_entity('Class8').add_field('Field1',"int")
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field1',"int")
    load_dia.get_entity('Entity2').add_field('Field2',"int")
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class7')
    assert load_dia.has_entity('Class8')
    assert Relation('composition', Entity('Class7'), Entity('Class8')) in load_dia._relations
    assert Relation('inheritance', Entity('Class8'), Entity('Class7')) in load_dia._relations
    assert 'Field1', "int" in load_dia.get_entity('Class7')._fields
    assert 'Field2', "int" in load_dia.get_entity('Class7')._fields
    assert 'Field1', "int" in load_dia.get_entity('Class8')._fields
    assert 'Param1', "int" in load_dia.get_entity('Class8').add_method("Param1", "int")
    assert 'Param1', "int" in load_dia.get_entity('Class8').add_method("Param1", "int")
    assert 'Param2', "int" in load_dia.get_entity('Class8').add_method("Param2", "int")
    assert 'Param3', "int" in load_dia.get_entity('Class8').add_method("Param3", "int")
