from umleditor.mvc_model import Entity

def test_create_entity():
    ent1 = Entity("entity1")
    assert ent1

def test_get_name():
    ent1 = Entity("entity1")
    assert ent1.get_name() == "entity1"
    assert ent1.get_name() != "entity2"

def test_entity_equals():
    ent1 = Entity("entity1")
    ent2 = Entity("entity2")
    assert ent1 == ent1
    assert ent2 == ent2
    assert ent1 != ent2
    assert ent2 != ent1

def test_set_name():
    ent1 = Entity("entity1")
    assert ent1.get_name() == "entity1"
    assert ent1.get_name() != "entity2"
    ent1.set_name("entity2")
    assert ent1.get_name() != "entity1"
    assert ent1.get_name() == "entity2"

def test_add_field():
    ent1 = Entity("entity1")
    assert "field1" not in ent1._fields
    ent1.add_field("field1")
    assert "field1" in ent1._fields

def test_add_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field1")
    ent1.add_field("field2")
    ent1.add_field("field3")
    assert "field1" in ent1._fields
    assert "field2" in ent1._fields
    assert "field3" in ent1._fields
    assert "field4" not in ent1._fields

def test_delete_field():
    ent1 = Entity("entity1")
    assert "field1" not in ent1._fields
    ent1.add_field("field1")
    assert "field1" in ent1._fields
    ent1.delete_field("field1")
    assert "field1" not in ent1._fields

def test_delete_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field1")
    ent1.add_field("field2")
    ent1.add_field("field3")
    ent1.add_field("field4")
    assert "field1" in ent1._fields
    assert "field2" in ent1._fields
    assert "field3" in ent1._fields
    assert "field4" in ent1._fields
    ent1.delete_field("field1")
    ent1.delete_field("field2")
    ent1.delete_field("field3")
    assert "field1" not in ent1._fields
    assert "field2" not in ent1._fields
    assert "field3" not in ent1._fields
    assert "field4" in ent1._fields

def test_rename_field():
    ent1 = Entity("entity1")
    assert "field1" not in ent1._fields
    ent1.add_field("field1")
    assert "field1" in ent1._fields
    assert "field2" not in ent1._fields
    ent1.rename_field("field1", "field2")
    assert "field1" not in ent1._fields
    assert "field2" in ent1._fields

def test_rename_multiple_fields():
    ent1 = Entity("entity1")
    ent1.add_field("field1")
    ent1.add_field("field2")
    assert "field1" in ent1._fields
    assert "field2" in ent1._fields
    assert "field3" not in ent1._fields
    assert "field4" not in ent1._fields
    ent1.rename_field("field1", "field3")
    ent1.rename_field("field2", "field4")
    assert "field1" not in ent1._fields
    assert "field2" not in ent1._fields
    assert "field3" in ent1._fields
    assert "field4" in ent1._fields

def test_add_method():
    ent1 = Entity("entity1")
    assert not any("method1" == um.get_method_name() for um in ent1._methods)
    ent1.add_method("method1")
    assert any("method1" == um.get_method_name() for um in ent1._methods)

def test_add_mutliple_methods():
    ent1 = Entity("entity1")
    assert not any("method1" == um.get_method_name() for um in ent1._methods)
    assert not any("method2" == um.get_method_name() for um in ent1._methods)
    assert not any("method3" == um.get_method_name() for um in ent1._methods)
    assert not any("method4" == um.get_method_name() for um in ent1._methods)
    ent1.add_method("method1")
    ent1.add_method("method2")
    ent1.add_method("method3")
    assert any("method1" == um.get_method_name() for um in ent1._methods)
    assert any("method2" == um.get_method_name() for um in ent1._methods)
    assert any("method3" == um.get_method_name() for um in ent1._methods)
    assert not any("method4" == um.get_method_name() for um in ent1._methods)

def test_rename_method():
    ent1 = Entity("entity1")
    ent1.add_method("method1")
    assert any("method1" == um.get_method_name() for um in ent1._methods)
    assert not any("method2" == um.get_method_name() for um in ent1._methods)
    ent1.rename_method("method1", "method2")
    assert not any("method1" == um.get_method_name() for um in ent1._methods)
    assert any("method2" == um.get_method_name() for um in ent1._methods)

def test_rename_multiple_methods():
    ent1 = Entity("entity1")
    ent1.add_method("method1")
    ent1.add_method("method2")
    assert any("method1" == um.get_method_name() for um in ent1._methods)
    assert any("method2" == um.get_method_name() for um in ent1._methods)
    assert not any("method3" == um.get_method_name() for um in ent1._methods)
    assert not any("method4" == um.get_method_name() for um in ent1._methods)
    ent1.rename_method("method1", "method3")
    ent1.rename_method("method2", "method4")
    assert not any("method1" == um.get_method_name() for um in ent1._methods)
    assert not any("method2" == um.get_method_name() for um in ent1._methods)
    assert any("method3" == um.get_method_name() for um in ent1._methods)
    assert any("method4" == um.get_method_name() for um in ent1._methods)