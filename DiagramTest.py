from Test import Test
from Diagram import Diagram
from Entity import Entity

def main():
    """
    Tests the add/rename/delete methods within the Diagram class
    """
    dia = Diagram()
    entity = Entity("entityName")

    # listEntities Testing
    listTest = Test("listEntities", dia.listEntities)
    print(listTest.exec("No entities", ""))

    # addClass Testing
    addTest = Test("addEntity", dia.addEntity)
    print(addTest.exec("Valid Name", None, "Entity1"))
    print(addTest.exec("Existing Name", "Entity with name 'Entity1' already exists.", "Entity1"))

    # renameClass Testing
    renameTest = Test("renameEntity", dia.renameEntity)
    print(renameTest.exec("Valid Rename", None, "Entity1", "NewEntity"))
    print(renameTest.exec("Invalid old name", "Entity with name 'Entity!' does not exists.", "Entity!", "NewEntity"))
    
    # listEntities Testing
    listTest = Test("listEntities", dia.listEntities)
    print(listTest.exec("Entity exists", "NewEntity"))

    #addAttribute Testing
    addAttrTest = Test("addAttribute", entity.addAttributes)
    print(addAttrTest.exec("Valid attribute name", None, "Attribute1"))
    print(addAttrTest.exec("Existing attribute", "Attribute with name 'Attribute1' already exists." , "Attribute1" ))
    
    #renameAttribute Testing
    renameAttrTest = Test("renameAttribute", entity.renameAttributes)
    print(renameAttrTest.exec("Valid rename attribute", None, "Attribute1", "newAttribute"))
    print(renameAttrTest.exec("Invalid old attribute name", "Attribute with name 'Attribute-Name' does not exist.", "Attribute-Name", "newAttribute"))

    #deleteAttribute Testing
    deleteAtrrTest = Test("deleteAttribute", entity.deleteAttributes)
    print(deleteAtrrTest.exec("Delete existing attribute", None, "newAttribute"))
    print(deleteAtrrTest.exec("Attribute not found", "Attribute with name 'nonExistentAttribute' does not exist.", "nonExistentAttribute"))

main()