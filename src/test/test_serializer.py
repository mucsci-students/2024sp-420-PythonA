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
    load_dia.get_entity('Entity1').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field2')
    load_dia.get_entity('Entity1').add_method_and_params('Method1')
    load_dia.get_entity('Entity1').add_method_and_params('Method2')
    load_dia.get_entity('Entity2').add_method_and_params('Method1', 'Param1')
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

def test_entities():
    dia = Diagram()
    dia.add_entity('Class1')
    dia.add_entity('Class2')
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field2')
    load_dia.get_entity('Entity1').add_method_and_params('Method1')
    load_dia.get_entity('Entity1').add_method_and_params('Method2')
    load_dia.get_entity('Entity2').add_method_and_params('Method1', 'Param1')
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class1')
    assert load_dia.has_entity('Class2')

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
    load_dia.get_entity('Entity1').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field2')
    load_dia.get_entity('Entity1').add_method_and_params('Method1')
    load_dia.get_entity('Entity1').add_method_and_params('Method2')
    load_dia.get_entity('Entity2').add_method_and_params('Method1', 'Param1')
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class1')
    assert load_dia.has_entity('Class2')
    assert Relation('composition', Entity('Class1'), Entity('Class2')) in load_dia._relations
    assert Relation('inheritance', Entity('Class2'), Entity('Class1')) in load_dia._relations

def test_fields():
    dia = Diagram()
    dia.add_entity('Class1')
    dia.add_entity('Class2')
    dia.get_entity('Class1').add_field('Field1')
    dia.get_entity('Class1').add_field('Field2')
    dia.get_entity('Class2').add_field('Field1')
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field2')
    load_dia.get_entity('Entity1').add_method_and_params('Method1')
    load_dia.get_entity('Entity1').add_method_and_params('Method2')
    load_dia.get_entity('Entity2').add_method_and_params('Method1', 'Param1')
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class1')
    assert load_dia.has_entity('Class2')
    assert 'Field1' in load_dia.get_entity('Class1')._fields
    assert 'Field2' in load_dia.get_entity('Class1')._fields
    assert 'Field1' in load_dia.get_entity('Class2')._fields

def test_methods():
    dia = Diagram()
    dia.add_entity('Class1')
    dia.add_entity('Class2')
    dia.get_entity('Class1').add_method_and_params('Method1')
    dia.get_entity('Class2').add_method_and_params('Method1', 'Param1')
    dia.get_entity('Class2').add_method_and_params('Method2')
    dia.get_entity('Class2').add_method_and_params('Method3', 'Param1', 'Param2', 'Param3')
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field2')
    load_dia.get_entity('Entity1').add_method_and_params('Method1')
    load_dia.get_entity('Entity1').add_method_and_params('Method2')
    load_dia.get_entity('Entity2').add_method_and_params('Method1', 'Param1')
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')
    
    assert load_dia.has_entity('Class1')
    assert load_dia.has_entity('Class2')
    assert load_dia.get_entity('Class1').get_method('Method1')
    assert load_dia.get_entity('Class2').get_method('Method1')
    assert 'Param1' in load_dia.get_entity('Class2').get_method('Method1')._params
    assert load_dia.get_entity('Class2').get_method('Method2')
    assert load_dia.get_entity('Class2').get_method('Method3')
    assert 'Param1' in load_dia.get_entity('Class2').get_method('Method3')._params
    assert 'Param2' in load_dia.get_entity('Class2').get_method('Method3')._params
    assert 'Param3' in load_dia.get_entity('Class2').get_method('Method3')._params

def test_all_together():
    dia = Diagram()
    dia.add_entity('Class1')
    dia.add_entity('Class2')
    dia.add_relation('Class1', 'Class2', 'composition')
    dia.add_relation('Class2', 'Class1', 'inheritance')
    dia.get_entity('Class1').add_field('Field1')
    dia.get_entity('Class1').add_field('Field2')
    dia.get_entity('Class2').add_field('Field1')
    dia.get_entity('Class1').add_method_and_params('Method1')
    dia.get_entity('Class2').add_method_and_params('Method1', 'Param1')
    dia.get_entity('Class2').add_method_and_params('Method2')
    dia.get_entity('Class2').add_method_and_params('Method3', 'Param1', 'Param2', 'Param3')
    serialize(dia, path)

    load_dia = Diagram()
    load_dia.add_entity('Entity1')
    load_dia.add_entity('Entity2')
    load_dia.add_relation('Entity1', 'Entity2', 'composition')
    load_dia.add_relation('Entity2', 'Entity1', 'realization')
    load_dia.get_entity('Entity1').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field1')
    load_dia.get_entity('Entity2').add_field('Field2')
    load_dia.get_entity('Entity1').add_method_and_params('Method1')
    load_dia.get_entity('Entity1').add_method_and_params('Method2')
    load_dia.get_entity('Entity2').add_method_and_params('Method1', 'Param1')
    deserialize(load_dia, path)
    assert not load_dia.has_entity('Entity1')
    assert not load_dia.has_entity('Entity2')

    assert load_dia.has_entity('Class1')
    assert load_dia.has_entity('Class2')
    assert Relation('composition', Entity('Class1'), Entity('Class2')) in load_dia._relations
    assert Relation('inheritance', Entity('Class2'), Entity('Class1')) in load_dia._relations
    assert 'Field1' in load_dia.get_entity('Class1')._fields
    assert 'Field2' in load_dia.get_entity('Class1')._fields
    assert 'Field1' in load_dia.get_entity('Class2')._fields
    assert load_dia.get_entity('Class1').get_method('Method1')
    assert load_dia.get_entity('Class2').get_method('Method1')
    assert 'Param1' in load_dia.get_entity('Class2').get_method('Method1')._params
    assert load_dia.get_entity('Class2').get_method('Method2')
    assert load_dia.get_entity('Class2').get_method('Method3')
    assert 'Param1' in load_dia.get_entity('Class2').get_method('Method3')._params
    assert 'Param2' in load_dia.get_entity('Class2').get_method('Method3')._params
    assert 'Param3' in load_dia.get_entity('Class2').get_method('Method3')._params