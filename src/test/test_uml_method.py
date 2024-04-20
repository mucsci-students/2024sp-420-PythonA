from umleditor.mvc_model import UML_Method, CustomExceptions
import pytest

def test_create_method( ):
    md1 = UML_Method("method1","int")
    assert md1

def test_get_method_name():
    md1 = UML_Method("method1", "int")
    md2 = UML_Method("method2", "float")
    assert md1.get_method_name() == "method1"
    assert md1.get_method_name() != "method2"
    assert md2.get_method_name() != "method1"
    assert md2.get_method_name() == "method2"

def test_set_method_name():
    md1 = UML_Method("method1", "int")
    assert md1.get_method_name() == "method1"
    assert md1.get_method_name() != "method2"
    md1.set_method_name("method2")
    assert md1.get_method_name() != "method1"
    assert md1.get_method_name() == "method2"

def test_get_return_type():
    md1 = UML_Method("method1", "int")
    assert md1.get_return_type() == "int"

# def test_check_duplicate_parameters():
#     md1 = UML_Method("method1", "int")
#     md1.add_parameters("param1")
#     with pytest.raises(CustomExceptions.DuplicateParametersError):
#         md1._check_duplicate_parameters("param1")


def test_method_equals():
    md1 = UML_Method("md1", "string")
    md2 = UML_Method("md2", "bool")
    assert md1 == md1
    assert md1 != md2
    assert md2 == md2
    assert md2 != md1

def test_add_parameter():
    md3 = UML_Method("md3", "int")
    assert "prm1" not in md3._params
    md3.add_parameters("prm1")
    assert "prm1" in md3._params
    assert "prm2" not in md3._params
    md3.add_parameters("prm2")
    assert "prm2" in md3._params

# def test_add_parameter_already_exists():
#     md3 = UML_Method("md3", "int")
#     md3.add_parameters("prm1")
#     assert "prm1" in md3._params
#     with pytest.raises(CustomExceptions.ParameterExistsError):
#         md3.add_parameters("prm1")

def test_add_one_remove_one_parameter():
    md1 = UML_Method("md1", "string")
    md1.add_parameters("prm1")
    assert "prm1" in md1._params
    md1.remove_parameters("prm1")
    assert "prm1" not in md1._params

def test_remove_parameter_doesnt_exist():
    md1 = UML_Method("md1", "string")
    with pytest.raises(CustomExceptions.ParameterNotFoundError):
        md1.remove_parameters("string")

def test_change_one_param():
    md1 = UML_Method("md1", "string")
    md1.add_parameters("prm1")
    assert "prm1" in md1._params
    assert "prm2" not in md1._params
    md1.change_parameters("prm1", "prm2")
    assert "prm1" not in md1._params
    assert "prm2" in md1._params

def test_change_duplicate_param():
    md4 = UML_Method("md4", "bool")
    md4.add_parameters("prm1")
    md4.add_parameters("prm2")
    with pytest.raises(CustomExceptions.ParameterExistsError):
        md4.change_parameters("prm1", "prm2")

def test_change_parameter_doesnt_exist():
    md4 = UML_Method("md4", "bool")
    with pytest.raises(CustomExceptions.ParameterNotFoundError):
        md4.change_parameters("parameter", "new_parameter")

def test_change_multiple_params():
    md1 = UML_Method("md1", "string")
    md1.add_parameters("prm1")
    md1.add_parameters("prm2")
    md1.add_parameters("prm3")
    md1.add_parameters("prm4")
    assert "prm1" in md1._params
    assert "prm2" in md1._params
    assert "prm3" in md1._params
    assert "prm4" in md1._params
    assert "prm5" not in md1._params
    assert "prm6" not in md1._params
    assert "prm7" not in md1._params
    assert "prm8" not in md1._params
    md1.change_parameters("prm1", "prm5")
    md1.change_parameters("prm2", "prm6")
    md1.change_parameters("prm3", "prm7")
    md1.change_parameters("prm4", "prm8")
    assert "prm1" not in md1._params
    assert "prm2" not in md1._params
    assert "prm3" not in md1._params
    assert "prm4" not in md1._params
    assert "prm5" in md1._params
    assert "prm6" in md1._params
    assert "prm7" in md1._params
    assert "prm8" in md1._params

def test_str():
    md1 = UML_Method("md1", "string")
    md1.add_parameters("parameter1")
    md1.add_parameters("parameter2")
    md1.add_parameters("parameter3")
    result = "\nmd1\n\tReturn Type: string\n\tmd1's Params: parameter1, parameter2, parameter3\n"
    assert md1.__str__() == result

def test_eq_success():
    md1 = UML_Method("method1", "float")
    md2 = UML_Method("method1", "float")
    md1.add_parameters("parameter1")
    md1.add_parameters("parameter2")
    md2.add_parameters("parameter1")
    md2.add_parameters("parameter2")
    assert md1.__eq__(md2) is True
    assert md2.__eq__(md1) is True

def test_eq_not_a_method():
    md1 = UML_Method("method1", "float")
    md1.add_parameters("parameter1")
    md1.add_parameters("parameter2")
    assert md1.__eq__("method") is False

def test_eq_names_not_equal():
    md1 = UML_Method("method1", "float")
    md2 = UML_Method("method2", "float")
    md1.add_parameters("parameter1")
    md1.add_parameters("parameter2")
    md2.add_parameters("parameter1")
    md2.add_parameters("parameter2")
    assert md1.__eq__(md2) is False
    assert md2.__eq__(md1) is False

def test_eq_number_of_params_not_equal():
    md1 = UML_Method("method1", "float")
    md2 = UML_Method("method1", "float")
    md1.add_parameters("parameter1")
    md1.add_parameters("parameter2")
    md2.add_parameters("parameter1")
    md2.add_parameters("parameter2")
    md2.add_parameters("parameter3")
    assert md1.__eq__(md2) is False
    assert md2.__eq__(md1) is False

def test_eq_params_not_equal():
    md1 = UML_Method("method1", "float")
    md2 = UML_Method("method1", "float")
    md1.add_parameters("parameter1")
    md1.add_parameters("parameter2")
    md2.add_parameters("parameter3")
    md2.add_parameters("parameter4")
    assert md1.__eq__(md2) is False
    assert md2.__eq__(md1) is False