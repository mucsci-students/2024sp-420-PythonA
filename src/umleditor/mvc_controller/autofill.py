import os
import glob
from prompt_toolkit.completion import Completer, Completion
from abc import ABC, abstractmethod
from umleditor.mvc_controller.uml_lexer import _command_flag_map
from umleditor.mvc_model.diagram import Diagram


class Strategy(ABC):
    @abstractmethod
    def get_completions(self, words, text, completer):
        pass


class InitialStrategy(Strategy):
    def get_completions(self, words, text, completer):
        if not text or (len(words) == 1 and not text.endswith(' ')):
            for command in completer.commands.keys():
                if not text or command.startswith(words[0]):
                    yield Completion(command, start_position=-len(words[0]) if words else 0)
        else:
            pass


class LoadFilesStrategy(Strategy):
    def get_completions(self, words, text, completer):
        if words[0] == 'load':
            yield from completer.get_files()
        else:
            pass


class FlagStrategy(Strategy):
    def get_completions(self, words, text, completer):
        if text.endswith('-'):
            yield from completer.flag_handler(words[0])
        else:
            pass


class DashCommandStrategy(Strategy):
    def get_completions(self, words, text, completer):
        if len(words) == 1 and text.endswith(' '):
            yield from completer.flag_handler(words[0], prepend_dash=True)
        else:
            pass


class TwoWordCommandStrategy(Strategy):
    def get_completions(self, words, text, completer):
        if len(words) == 2 and text.endswith(' '):
            if words[0] == 'class' and words[1] in ['-r', '-d']:
                yield from completer.class_args()
            elif words[0] in ['fld', 'mthd', 'prm']:
                yield from completer.class_args()
            elif words[0] == 'list'and words[1] == '-d':
                yield from completer.class_args()
            elif words[0] == 'rel':
                if words[1] == '-a':
                    yield from completer.class_args()
                else:
                    yield from completer.rel_args()
        else:
            pass

class ThreeWordCommandStrategy(Strategy):
    def get_completions(self, words, text, completer):
        if len(words) == 3 and text.endswith(' '):
            if words[0] in ['fld', 'mthd'] and words[1] in ['-r', '-d']:
                yield from completer.field_args(words) if words[0] == 'fld' else completer.method_args(words)
            elif words[0] == 'prm':
                yield from completer.method_args(words)
            elif words[0] == 'rel' and words[1] == '-a':
                yield from completer.class_args()


class ComplexCommandStrategy(Strategy):
    def get_completions(self, words, text, completer):
        if (len(words) == 4 or len(words) == 6) and text.endswith(' '):
            if words[0] == 'fld':
                if words[1] == '-a' or (words[1] == '-r' and len(words) == 6):
                    yield from completer.suggestion_type(words[2])
            elif words[0] == 'mthd' and words[1] == '-a':
                yield from completer.suggestion_return_type(words[2])
            elif words[0] == 'prm' and words[1] in ['-r', '-d']:
                yield from completer.prm_args(words)
            elif words[0] == 'rel' and words[1] in ['-a', '-t']:
                rel_types = ['aggregation', 'composition', 'inheritance', 'realization']
                for rel_type in rel_types:
                    yield Completion(rel_type, start_position=0)
        else:
            pass


class CommandCompleter(Completer):
    commands = _command_flag_map
    commands_without_flag = [key for key, values in _command_flag_map.items() if not any(values)]
    diagram = Diagram()

    def __init__(self):
        self.strategy = None

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()

        # Initialize the strategy based on the current state of text and words
        if not text or (len(words) == 1 and not text.endswith(' ')):
            self.strategy = InitialStrategy()
        elif len(words) == 1 and text.endswith(' '):
            self.strategy = LoadFilesStrategy() if words[0] == 'load' else DashCommandStrategy()
        elif len(words) == 2 and text.endswith('-'):
            self.strategy = FlagStrategy()
        elif len(words) == 2 and text.endswith(' '):
            self.strategy = TwoWordCommandStrategy()
        elif len(words) == 3 and text.endswith(' '):
            self.strategy = ThreeWordCommandStrategy()
        elif (len(words) == 4 or len(words) == 6) and text.endswith(' '):
            self.strategy = ComplexCommandStrategy()
        else:
            pass

        return self.strategy.get_completions(words, text, self)

    def get_files(self):
        save_path = os.path.join(os.path.dirname(__file__), '../', '../', '../', 'save')
        normalized_save_path = os.path.normpath(save_path)
        search_pattern = os.path.join(normalized_save_path, '*.json')
        json_files = glob.glob(search_pattern)
        files = [os.path.splitext(os.path.basename(file))[0] for file in json_files]
        for filename in files:
            if filename.startswith("state_"):
                continue
            yield Completion(filename, start_position=0)

    def flag_handler(self, command, prepend_dash=False):
        flags = self.commands.get(command, [])
        if command not in self.commands_without_flag:
            for flag in flags:
                if prepend_dash:
                    yield Completion('-' + flag, start_position=0)
                else:
                    yield Completion(flag, start_position=0)
        else:
            pass

    def class_args(self):
        classes = self.diagram._entities
        for cls in classes:
            yield Completion(str(cls), start_position=0, display_meta="(class)")

    def field_args(self, words):
        fields = self.diagram.get_entity(words[2])._fields
        if words[1] == '-r':
            for field in fields:
                yield Completion(field[0], start_position=0)
        else:
            for field in fields:
                yield Completion(field[0], start_position=0, display_meta="Type: " + field[1])

    def method_args(self, words):
        methods = self.diagram.get_entity(words[2])._methods
        for method in methods:
            yield Completion(method.get_method_name(), start_position=0, display_meta="(method)")

    def prm_args(self, words):
        params = self.diagram.get_entity(words[2]).get_method(words[3])._params
        for parm in params:
            yield Completion(parm, start_position=0, display_meta="(parameter)")

    def rel_args(self):
        relations = []
        for rel in self.diagram.list_relations():
            relations.append(rel.split(" -> "))
        for rel in relations:
            yield Completion(rel[0] + " " + rel[2], start_position=0, display_meta= rel[1])

    def suggestion_type(self, entity_name):
        types = self.diagram.get_entity(entity_name).allowed_types
        for type in types:
            yield Completion(type, start_position=0)

    def suggestion_return_type(self, entity_name):
        types = self.diagram.get_entity(entity_name).allowed_return_types
        for type in types:
            yield Completion(type, start_position=0)
