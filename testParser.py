import CustomParser as P
from CustomParser import parse, __findFunction, __checkArgs
#because parser needs to be able to see every command, test needs to as well.
from Diagram import Diagram
from Entity import Entity
from CustomExceptions import CustomExceptions as CE
from Relation import Relation
from Test import Test
import Controller

def main():
    invalidArgs = Test("Invalid Arg Input", P.parse)
    print(invalidArgs.exec("",[CE.InvalidArgumentError("%"),"%"],"class -a %"))

    invalidCommand = Test("Invalid Command Input", P.parse)
    print(invalidCommand.exec("", [CE.CommandNotFoundError("test")],"test"))

    entityTests = Test("Entity Methods", P.parse)
    print(entityTests.exec("add", [Diagram.addEntity, "test"],"class -a test"))
    print(entityTests.exec("delete", [Diagram.deleteEntity, "test"], "class -d test"))
    print(entityTests.exec("set name", [Entity.setName, "test"], "class -r test"))
    #print(entityTests.exec("select entity", [CLASS.METHOD, "test"], "class -s test"))
    print(entityTests.exec("invalid flag", [CE.InvalidFlagError("z","class"), "test"], "class -z test"))

    listTests = Test("List Methods", P.parse)
    #print(listTests.exec("everything",[CLASS.METHOD],"list -a"))
    print(listTests.exec("all entities",[Diagram.listEntities],"list -c"))
    #print(listTests.exec("all relationships",[CLASS.METHOD],"list -r"))
    #print(listTests.exec("all class data",[CLASS.METHOD, "test"],"list -c test"))
    print(listTests.exec("invalid flag",[CE.InvalidFlagError("z","list")],"list -z"))

    saveTests = Test("Save Methods", P.parse)
    #print(saveTests.exec("with name", [CLASS.METHOD, "test"], "save -n test"))
    #print(saveTests.exec("no name", [CLASS.METHOD], "save"))
    print(saveTests.exec("invalid flag",[CE.InvalidFlagError("z","save")],"save -z"))

    loadTests = Test("Load Methods", P.parse)
    #print (loadTests.exec("with name", [CLASS.METHOD, "test"], "load -f test"))
    print(loadTests.exec("invalid flag",[CE.InvalidFlagError("z","load")],"load -z"))

    attributeTests = Test("Attribute Methods", P.parse)
    #print(attributeTests.exec("add", [CLASS.METHOD, "test"],"att -a test"))
    #print(attributeTests.exec("delete", [CLASS.METHOD, "test"],"att -d test"))
    #print(attributeTests.exec("rename", [CLASS.METHOD, "test", "test2"],"att -r test test2"))
    print(attributeTests.exec("invalid flag",[CE.InvalidFlagError("z","att")],"att -z"))

    relationTests = Test("Relation Methods", P.parse)
    #print(relationTests.exec("add", [CLASS.METHOD, "test"], "rel -a test"))
    #print(relationTests.exec("delete", [CLASS.METHOD, "test"], "rel -d test"))
    print(relationTests.exec("invalid flag",[CE.InvalidFlagError("z","rel")],"rel -z"))

main()