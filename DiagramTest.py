from Test import Test
from Diagram import Diagram

def main():
    """
    Tests the add/rename/delete methods within the Diagram class
    """
    dia = Diagram()

    # listEntities Testing
    listTest = Test("listEntities", dia.listEntities)
    print(listTest.exec("No entities", ""))

    # addClass Testing
    addTest = Test("addEntity", dia.addEntity)
    print(addTest.exec("Valid Name", None, "Entity1"))
    print(addTest.exec("Invalid Name", "Name must contain only alphanumeric characters", "Entity 1"))
    print(addTest.exec("Existing Name", "Object with name 'Entity1' already exists.", "Entity1"))

    # renameClass Testing
    renameTest = Test("renameEntity", dia.renameEntity)
    print(renameTest.exec("Valid Rename", None, "Entity1", "NewEntity"))

    # listEntities Testing
    listTest = Test("listEntities", dia.listEntities)
    print(listTest.exec("Entity exists", "NewEntity"))
    
main()