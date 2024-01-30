from CmdParser import parse

def testValidInput ():
    bool passed = (parse("help") == ["help"]) 