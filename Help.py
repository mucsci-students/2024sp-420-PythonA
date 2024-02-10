'''Application help menu, to be called when user asks for help.'''

from CustomExceptions import CustomExceptions   #if an invalid command was entered after help

def help():
    #Shows the top layer help menu that details what more specific help commands work on
    #returns a string that contains the menu
    
    #Class Commands
    menu = "Class Commands: \n\t"
    menu += "-a name  - adds a class with name 'name'. Cannot add classes with duplicate or invalid names\n\t"
    menu += "-d name  - deletes a class with name 'name'\n\t"
    menu += "-r old new - renames class 'old' to 'new'. Cannot rename classes to duplicate or invalid names\n"

    #Attribute Commands
    menu += "Attribute Commands: \n\t"
    menu += "-a class name - adds an attribute with name 'name' to class 'class'\n\t"
    menu += "-d class name - deletes an attribute with name 'name' from class 'class' if one exists\n\t"
    menu += "-r class old new - renames an attribute from name 'old' to name 'new' in class 'class'\n"

    #Relation Commands
    menu += "Relation Commands:\n\t"
    menu += "-a src dest - adds a relationship between class 'src' and class 'dest' assuming both are valid\n\t"
    menu += "-d src dest - deletes a relationship between class 'src' and class 'dest' if one exists\n"

    #List Commands
    menu += "List Flags: \n\t"
    menu += "-a   - list all classes and their contents in the UML Diagram\n\t"
    menu += "-c   - list all classes in the UML Diagram\n\t"
    menu += "-r   - list all relationships in the UML Diagram\n\t"
    menu += "-d name - list all contents of class 'name'\n"

    #Save Commands
    menu += "Save Flags: \n\t"
    menu += "name - saves the UML Diagram as a JSON file with name 'name'\n"

    #Load Commands
    menu += "Load Flags: \n\t"
    menu += "name - loads the file with name 'name.json' if one exists\n\n"

    #Exit Commands
    menu += "enter exit or quit to terminate the program\n"

    return menu
