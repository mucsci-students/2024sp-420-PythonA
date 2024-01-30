from Entity import Entity
from Relation import Relation

class Diagram:
    def __init__(self) -> None:
        self._entities = dict()
        self._relations = []