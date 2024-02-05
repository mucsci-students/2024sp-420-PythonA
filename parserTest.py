from CustomParser import parse
#because parser needs to be able to see every command, test needs to as well.
from Diagram import Diagram
from Entity import Entity
from CustomExceptions import CustomExceptions as CE
from Relation import Relation
from Test import Test

def main():
    d = Diagram()

    #Entity class parseing tests
    addEntities = Test("Add Entity", parse)
    