class Test:
    def __init__(self, name:str, func):
        self.func = func
        self.name = name


    def exec(self, detail:str, expected, *args):
        """
            Executes self.func, passing in all args in the order provided

            Args:
                detail - a little extra info about what case is being tested
                expected - the expected output of this test. Can take any form with a defined __str__
                *args - a variadic list of all arguments that self.func needs to run

            Return:
                A string in the form "self.name detail - passed" if the test was passed
                A string in the form "self.name detail - expected {} actual {}" if the test was failed
        """
        try:
            output = self.func(*args)
        except Exception as e:
            return self.__createOutput(detail, str(expected), str(e))

        
        return self.__createOutput(detail, str(expected), str(output))


    def checkUpdate(self, detail:str, expected, searchLoc, *args):
        '''
            Executes self.func, passing in all args in the order provided

            Args:
                detail - a little extra info about what case is being tested
                expected - the expected output of this test. Can take any form with a defined __str__
                searchLoc - the function to call to search for the expected output
                *args - a variadic list of all arguments that self.func needs to run

            Return:
                A string in the form "self.name detail - passed" if the test was passed
                A string in the form "self.name detail - expected {} actual {}" if the test was failed

        '''
        try:
            self.func(*args)
        except Exception as e:
            return self.__createOutput(detail, str(expected), str(e))

        return self.__createOutput(detail, str(expected), str(searchLoc()))
    
    '''Private helper that takes an expected and actual output, then checks and formats them. 
        param detail - a short message about what case is being tested specifically
        param expected - the expected outcome to compare to
        param actual - the actual outcome of the test
        returns a string in the form "self.name detail - passed" if the test was passed
        returns a string in the form "self.name detail - expected {} actual {}" if the test was failed
    '''
    def __createOutput(self, detail:str, expected:str, actual:str):
        '''
            Private helper to create the output string returned from a call to any method that runs a test.

            Args:
                detail - a little extra info about what case is being tested
                expected - the expected output of this test, as a string
                actual - the actual output of this test, as a string

            Return:
                A string in the form "self.name detail - passed" if the test was passed
                A string in the form "self.name detail - expected {} actual {}" if the test was failed

        '''
        output = self.name + ": " + detail + " - "

        if(expected == actual):
            return output + "passed"
        else:
            return output + "\n\tExpected: " + expected + "\n\tActual: " + actual    

        
 