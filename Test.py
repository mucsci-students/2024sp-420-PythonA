class Test:
    def __init__(self, name:str, func):
        self.func = func
        self.name = name

    '''Executes self.func, passing in all args in order provided.
        param detail - a short message about what specific case is being tested
        param expected - the expected outcome to compare to
        param *args - the list of params to pass to self.func
        returns a string in the form "self.name detail - passed" if the test was passed
        returns a string in the form "self.name detail - expected {} actual {}" if the test was failed
    '''
    def exec(self, detail:str, expected, *args):
        output = self.func(*args)
        
        return self.__createOutput(detail, str(expected), str(output))

    '''Executes self.func, passing in all args in order provided
        param detail - a short message about what case is being tested specifically
        param expected - the expected outcome to compare to
        param searchLoc - the method to call to get the actual output
        returns a string in the form "self.name detail - passed" if the test was passed
        returns a string in the form "self.name detail - expected {} actual {}" if the test was failed

    '''
    def checkUpdate(self, detail:str, expected, searchLoc, *args):

        self.func(*args)

        return self.__createOutput(detail, str(expected), str(searchLoc()))
    
    '''Private helper that takes an expected and actual output, then checks and formats them. 
        param detail - a short message about what case is being tested specifically
        param expected - the expected outcome to compare to
        param actual - the actual outcome of the test
        returns a string in the form "self.name detail - passed" if the test was passed
        returns a string in the form "self.name detail - expected {} actual {}" if the test was failed
    '''
    def __createOutput(self, detail:str, expected:str, actual:str):
        output = self.name + ": " + detail + " - "

        if(expected == actual):
            return output + "passed"
        else:
            return output + "\n\tExpected: " + expected + "\n\tActual: " + output    

        
