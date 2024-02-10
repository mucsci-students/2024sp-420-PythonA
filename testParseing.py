import Input
import Output
import Serializer
from CustomExceptions import CustomExceptions as CE
from Controller import Controller
from Diagram import Diagram
from Test import Test
import os
import Help

#Parser Includes. These will be moved out when the parser is moved.
from Entity import Entity
from Relation import Relation

def main():
    c = Controller()
    print("----------------------------------------\nParser Unit Tests\n----------------------------------------")
    unit_tests(c)


def unit_tests(c:Controller):
    parseTest = Test("Parser Tests", c.parse)
    d = c._diagram

    #Class tests
    print(parseTest.exec("class add valid name", [d.add_entity, "test"], "class -a test"))
    print(parseTest.exec("class add invalid name", CE.InvalidArgumentError("%"), "class -a %"))
    print(parseTest.exec("class delete valid name", [d.delete_entity, "test"], "class -d test"))
    print(parseTest.exec("class delete invalid name", CE.InvalidArgumentError("%"), "class -d %"))
    print(parseTest.exec("class rename valid name", [d.rename_entity, "test", "test2"], "class -r test test2"))
    print(parseTest.exec("class delete invalid old name", CE.InvalidArgumentError("%"), "class -r % test"))
    print(parseTest.exec("class delete invalid new name", CE.InvalidArgumentError("%"), "class -r test %"))
    print(parseTest.exec("class invalid flag", CE.InvalidFlagError("-z", "class"), "class -z test"))

    #List tests
    print(parseTest.exec("list everything", [d.list_everything], "list -a"))
    print(parseTest.exec("list entities", [d.list_entities], "list -c"))
    print(parseTest.exec("list relations", [d.list_relations], "list -r"))
    print(parseTest.exec("list detail valid target", [d.list_entity_details, "test"], "list -d test"))
    print(parseTest.exec("list detail invalid target", CE.InvalidArgumentError("%"), "list -d %"))
    print(parseTest.exec("list invalid flag", CE.InvalidFlagError("-z", "list"), "list -z test"))

    #Attribute tests
    d.add_entity("cl")
    e = d.get_entity("cl")
    print(parseTest.exec("attribute add valid name", [e.add_attribute, "cl", "att1"], "att -a cl att1"))
    print(parseTest.exec("attribute add invalid class", CE.InvalidArgumentError("'"), "att -a ' att1"))
    print(parseTest.exec("attribute add invalid att name", CE.InvalidArgumentError("%"), "att -a cl %"))
    print(parseTest.exec("attribute delete valid target", [e.delete_attribute, "cl", "att1"], "att -d cl att1"))
    print(parseTest.exec("attribute delete invalid class", CE.InvalidArgumentError("'"), "att -d ' att1"))
    print(parseTest.exec("attribute delete invalid att name", CE.InvalidArgumentError("'"), "att -a cl '"))
    print(parseTest.exec("attribute rename valid", [e.rename_attribute, "cl","att1","att2"], "att -r cl att1 att2"))
    print(parseTest.exec("attribute rename invalid class", CE.InvalidArgumentError("'"), "att -r ' att1 att2"))
    print(parseTest.exec("attribute rename invalid old name", CE.InvalidArgumentError("'"), "att -r cl ' att2"))
    print(parseTest.exec("attribute rename invalid new name", CE.InvalidArgumentError("'"), "att -r cl att1 '"))
    print(parseTest.exec("attribute invalid flag", CE.InvalidFlagError("-z", "att"), "att -z test"))

    #Relation tests
    print(parseTest.exec("relation add valid args", [d.add_relation, "c1", "c2"], "rel -a c1 c2"))
    print(parseTest.exec("relation add invalid source", CE.InvalidArgumentError("'"), "rel -a ' c2"))
    print(parseTest.exec("relation add invalid destination", CE.InvalidArgumentError("'"), "rel -a c1 '"))
    print(parseTest.exec("relation delete valid args", [d.delete_relation, "c1", "c2"], "rel -d c1 c2"))
    print(parseTest.exec("relation delete invalid source", CE.InvalidArgumentError("'"), "rel -d ' c2"))
    print(parseTest.exec("relation add invalid destination", CE.InvalidArgumentError("'"), "rel -d c1 '"))
    print(parseTest.exec("relation invalid flag", CE.InvalidFlagError("-z", "rel"), "rel -z test"))

    #Controller Method tests
    print(parseTest.exec("save", [c.save], "save"))
    print(parseTest.exec("load", [c.load], "load"))
    print(parseTest.exec("quit", [c.quit], "quit"))
    print(parseTest.exec("help", [Help.help], "help"))
    print(parseTest.exec("command invalid", CE.CommandNotFoundError("z"), "z"))

    #cleanup from attribute tests
    d.delete_entity("c1")

def integration_tests (c:Controller):
    d = c._diagram


















main()