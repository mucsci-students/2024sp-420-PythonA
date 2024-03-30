from src.umleditor.mvc_model import UML_Method

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

def test_method_equals():
    md1 = UML_Method("md1")
    md2 = UML_Method("md2")
    assert md1 == md1
    assert md1 != md2
    assert md2 == md2
    assert md2 != md1

def test_add_parameter():
    md1 = UML_Method("md1")
    assert "prm1" not in md1._params
    md1.add_parameters(["prm1"])
    assert "prm1" in md1._params
    assert "prm2" not in md1._params
    md1.add_parameters(["prm2"])
    assert "prm2" in md1._params

def test_add_multiple_parameters():
    md1 = UML_Method("md1")
    assert "prm1" not in md1._params
    assert "prm2" not in md1._params
    assert "prm3" not in md1._params
    assert "prm4" not in md1._params
    md1.add_parameters(["prm1", "prm2", "prm3"])
    assert "prm1" in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" not in md1._params
    assert "prm5" not in md1._params
    md1.add_parameters(["prm4", "prm5"])
    assert "prm1" in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    assert "prm5" in md1._params

def test_add_one_remove_one_parameter():
    md1 = UML_Method("md1")
    md1.add_parameters(["prm1"])
    assert "prm1" in md1._params
    md1.remove_parameters(["prm1"])
    assert "prm1" not in md1._params

def test_add_multiple_remove_one_parameter_at_a_time():
    md1 = UML_Method("md1")
    md1.add_parameters(["prm1", "prm2", "prm3", "prm4"])
    assert "prm1" in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    md1.remove_parameters(["prm1"])
    assert "prm1" not in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    md1.remove_parameters(["prm4"])
    assert "prm1" not in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" not in md1._params
    md1.remove_parameters(["prm2"])
    assert "prm1" not in md1._params
    assert "prm2" not in md1._params
    assert "prm3" in md1._params
    assert "prm4" not in md1._params
    md1.remove_parameters(["prm3"])
    assert "prm1" not in md1._params
    assert "prm2" not in md1._params
    assert "prm3" not in md1._params
    assert "prm4" not in md1._params

def test_add_multiple_remove_many_params_at_a_time():
    md1 = UML_Method("md1")
    md1.add_parameters(["prm1", "prm2", "prm3", "prm4", "prm5", "prm6", "prm7", "prm8"])
    assert "prm1" in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    assert "prm5" in md1._params
    assert "prm6" in md1._params
    assert "prm7" in md1._params
    assert "prm8" in md1._params
    md1.remove_parameters(["prm1", "prm2"])
    assert "prm1" not in md1._params
    assert "prm2" not in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    assert "prm5" in md1._params
    assert "prm6" in md1._params
    assert "prm7" in md1._params
    assert "prm8" in md1._params
    md1.remove_parameters(["prm3", "prm5", "prm7"])
    assert "prm1" not in md1._params
    assert "prm2" not in md1._params
    assert "prm3" not in md1._params
    assert "prm4" in md1._params
    assert "prm5" not in md1._params
    assert "prm6" in md1._params
    assert "prm7" not in md1._params
    assert "prm8" in md1._params

def test_change_one_param():
    md1 = UML_Method("md1")
    md1.add_parameters(["prm1"])
    assert "prm1" in md1._params
    assert "prm2" not in md1._params
    md1.change_parameters(["prm1"], ["prm2"])
    assert "prm1" not in md1._params
    assert "prm2" in md1._params

def test_change_multiple_params():
    md1 = UML_Method("md1")
    md1.add_parameters(["prm1", "prm2", "prm3", "prm4"])
    assert "prm1" in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    assert "prm5" not in md1._params
    assert "prm6" not in md1._params
    assert "prm7" not in md1._params
    assert "prm8" not in md1._params
    md1.change_parameters(["prm1", "prm2"], ["prm5", "prm6"])
    assert "prm1" not in md1._params
    assert "prm2" not in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    assert "prm5" in md1._params
    assert "prm6" in md1._params
    assert "prm7" not in md1._params
    assert "prm8" not in md1._params
    md1.change_parameters(["prm3", "prm4", "prm5"], ["prm7", "prm8", "prm1"])
    assert "prm1" in md1._params
    assert "prm2" not in md1._params
    assert "prm3" not in md1._params
    assert "prm4" not in md1._params
    assert "prm5" not in md1._params
    assert "prm6" in md1._params
    assert "prm7" in md1._params
    assert "prm8" in md1._params