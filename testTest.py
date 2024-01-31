#Tests the class Test.py
from Test import Test

def addOne(number):
    return number + 1

def subtractOne(num1, num2):
    return num1 - num2

def fancyString(string):
    return string + " according to all known laws of aviation"

def main():
    adding = Test("Test addOne", addOne)
    print(adding.exec("add one", 2, 1))
    print(adding.exec("add two", 3, 2))

    subtracting = Test("Test subtract", subtractOne)
    print(subtracting.exec("5 - 3", 2, 5, 3))
    print(subtracting.exec("3 - 7", -4, 2, 7))

    stringmod = Test("fancyString", fancyString)
    print(stringmod.exec("idk", "idk according to all known laws of aviation", "idk"))


main()

