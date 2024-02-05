import os

from Test import Test
from Diagram import Diagram
from Serializer import Serializer
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
    print(addTest.exec("Invalid Name", "Name must contain only alphanumeric characters", "Entity 1"))
    print(addTest.exec("Existing Name", "Object with name 'Entity1' already exists.", "Entity1")) #TYPO FIXED
    print(addTest.exec("Existing Name", "Entity with name 'Entity1' already exists.", "Entity1"))


    # renameClass Testing
    renameTest = Test("renameEntity", dia.renameEntity)
    print(renameTest.exec("Valid Rename", None, "Entity1", "NewEntity"))
    print(renameTest.exec("Invalid old name", "Entity with name 'Entity!' does not exists.", "Entity!", "NewEntity"))
    
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
    
    # Save/Load Testing
    toSave = Diagram()
    toSave.addEntity(name='First')
    toSave.addEntity(name='Second')
    toSave.addEntity(name='Third')
    serializer = Serializer()
    dirname = os.path.dirname(__file__)
    serializer.serialize(diagram=toSave, path=os.path.join(dirname, 'save.test'))
    toLoad = Diagram()
    serializer.deserialize(diagram=toLoad, path=os.path.join(dirname, 'save.test'))
    res = 'Save/Load - {}'
    print(res.format('Passed') if toSave.listEntities() == toLoad.listEntities() else res.format('Failed'))
    
if __name__ == '__main__':
    main()
