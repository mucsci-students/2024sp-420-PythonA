import os

from Test import Test
from Diagram import Diagram
from Serializer import Serializer

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
    print(addTest.exec("Existing Name", "Entity with name 'Entity1' already exists.", "Entity1"))

    # renameClass Testing
    renameTest = Test("renameEntity", dia.renameEntity)
    print(renameTest.exec("Valid Rename", None, "Entity1", "NewEntity"))
    print(renameTest.exec("Invalid old name", "Entity with name 'Entity!' does not exists.", "Entity!", "NewEntity"))
    print(renameTest.exec("Invalid new name", "Name must contain only alphanumeric characters", "NewEntity", "NewEntity!"))
    
    # listEntities Testing
    listTest = Test("listEntities", dia.listEntities)
    print(listTest.exec("Entity exists", "NewEntity"))

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