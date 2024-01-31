class Test:
    def __init__(self, name:str, func):
        self.func = func
        self.name = name

    '''Executes self.func, passing in all args in order provided.
        param detail - a short message about what specific case is being tested
        param expected - the expected outcome to compare to
        param *args - the list of params to mass to self.func
        returns a string in the form "self.name detail passed if the test was passed
        returns a string in the form "self.name detail expected {} actual {} if the test was failed
    '''
    def exec(self, detail:str, expected, *args):
        ret = self.name + ": " + detail + " - "
        output = str(self.func(*args))

        if(str(expected) == output):
            return ret + "passed"
        else:
            return ret + "\n\tExpected: " + str(expected) + "\n\tActual: " + output
