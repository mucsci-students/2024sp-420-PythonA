'''Application help menu, to be called when user asks for help.'''

from CustomExceptions import CustomExceptions   #if an invalid command was entered after help

def basicHelp():
    #Shows the top layer help menu that details what more specific help commands work on
    #returns a string that contains the menu
    menu = "Use 'help [command]' for detailed information about command usage\n\t"
    menu += "class - displays all commands related to class creation and modification\n\t"
    menu += "att   - displays all commands related to attribute creation and modification\n\t"
    menu += "rel   - displays all comands related to relationship creation and modification\n\t"
    menu += "list  - displays all commands related to list creation and modification\n\t"
    menu += "save  - displays usage for the save command\n\t"
    menu += "load  - displays usage for the load command\n\t"
    menu += "exit  - displays usage for the exit\quit command\n\t"

    return menu

def cmdHelp(command:str):
    #parses a string that corresponds to one of the options in the outer level help menu
    #returns a string containing all options that correspond to the provided command
    menu = CustomExceptions.CommandNotFoundError(command)

    if("class" == command):
        menu = "-a name  - adds a class with name 'name'. Cannot add classes with duplicate or invalid names\n"
        menu += "-d name - deletes a class with name 'name'\n"
        menu += "-r old new - renames class 'old' to 'new'. Cannot rename classes to duplicate or invalid names\n"
    
    elif("att" == command):
        menu += "-a class name - adds an attribute with name 'name' to class 'class'\n\t"
        menu += "-d class name - deletes an attribute with name 'name' from class 'class' if one exists\n\t"
        menu += "-r old new - renames an attribute from name 'old' to name 'new' in the selected class\n"
    
    elif("rel" == command):
        menu += "-a src dest - adds a relationship between class 'src' and class 'dest' assuming both are valid\n\t"
        menu += "-d src dest - deletes a relationship between class 'src' and class 'dest' if one exists\n"
    
    elif("list" == command):
        menu = "-a   - list all classes and their contents in the UML Diagram\n"
        menu += "-c - list all classes in the UML Diagram\n"
        menu += "-r   - list all relationships in the UML Diagram\n"
        menu += "-c name - list all contents of class 'name'\n"
    
    elif("save" == command):
        menu = "-n name - saves the UML Diagram as a JSON file with name 'name'\n"
    
    elif("load" == command):
        menu = "name - loads the file with name 'name.json' if one exists\n"

    elif("exit" == command or "quit" == command):
        menu = "enter exit or quit to terminate the program\n"
    
    return menu
