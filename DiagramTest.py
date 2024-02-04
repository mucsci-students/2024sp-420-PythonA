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
    print(addTest.exec("Existing Name", "Object with name 'Entity1' already exists.", "Entity1")) #TYPO FIXED

    # renameClass Testing
    renameTest = Test("renameEntity", dia.renameEntity)
    print(renameTest.exec("Valid Rename", None, "Entity1", "NewEntity"))
    print(renameTest.exec("Invalid old name", "Entity with name 'Entity!' does not exists.", "Entity!", "NewEntity"))
    print(renameTest.exec("Invalid new name", "Name must contain only alphanumeric characters", "NewEntity", "NewEntity!"))
    
    # listEntities Testing
    listTest = Test("listEntities", dia.listEntities)
    print(listTest.exec("Entity exists", "NewEntity"))
    
    # add_relation Testing
    dia.addEntity("Entity2") #Need second to test relation
    add_relation_test = Test("add_relation", dia.add_relation)
    print(add_relation_test.exec("Valid input", "Entity1 -> Entity2", "Entity1", "Entity2"))
    print(add_relation_test.exec("Relation already exists.", "Relation between 'Entity1 -> Entity2' already exists.", "Entity1", "Entity2"))
    
    # delete_relation Testing
    delete_relation_test = Test("delete_relation", dia.delete_relation)
    print(delete_relation_test.exec("Valid input.", "Entity1 -> Entity2", "Entity1", "Entity2"))
    print(delete_relation_test.exec("No relation.", "Relation between 'Entity1 -> Entity2' does not exist.", "Entity1", "Entity2"))
    
    
main()
