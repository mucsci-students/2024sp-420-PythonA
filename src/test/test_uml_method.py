from umleditor.mvc_model import UML_Method

def test_create_method():
    md1 = UML_Method("method1")
    assert md1

def test_get_method_name():
    md1 = UML_Method("method1")
    md2 = UML_Method("method2")
    assert md1.get_method_name() == "method1"
    assert md1.get_method_name() != "method2"
    assert md2.get_method_name() != "method1"
    assert md2.get_method_name() == "method2"

def test_set_method_name():
    md1 = UML_Method("method1")
    assert md1.get_method_name() == "method1"
    assert md1.get_method_name() != "method2"
    md1.set_method_name("method2")
    assert md1.get_method_name() != "method1"
    assert md1.get_method_name() == "method2"