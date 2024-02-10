'''Application help menu, to be called when user asks for help.'''

from CustomExceptions import CustomExceptions   #if an invalid command was entered after help

def help():
    #Shows the top layer help menu that details what more specific help commands work on
    #returns a string that contains the menu
    menu = "\nHelp menu:  For the best view, resize your window so that this message and the bar at the end are on one line.    |\n\n"
    menu += "Below are the commands you can call and an explanation of what each does. Anything inside single quotes is decided\n"
    menu += "by you! Enter the command, replacing anything in the single quotes, and the quotes themselves, with the name you\n"
    menu += "want to use.\n\n"
    menu += "A valid name is made up of any combination of letters and numbers.\n\n"
    #Class Commands
    menu += "Class Commands: \n\t"
    menu += "class -a 'name'  - adds a class with name 'name'. Cannot add classes with duplicate or invalid names\n\t"
    menu += "class -d 'name'  - deletes a class with name 'name'\n\t"
    menu += "class -r 'old' 'new' - renames class 'old' to 'new'. Cannot rename classes to duplicate or invalid names\n"

    #Attribute Commands
    menu += "Attribute Commands: \n\t"
    menu += "att -a class 'name' - adds an attribute with name 'name' to class 'class'\n\t"
    menu += "att -d class 'name' - deletes an attribute with name 'name' from class 'class' if one exists\n\t"
    menu += "att -r class 'old' 'new' - renames an attribute from name 'old' to name 'new' in class 'class'\n"

    #Relation Commands
    menu += "Relation Commands:\n\t"
    menu += "rel -a 'src' 'dest' - adds a relationship between class 'src' and class 'dest' assuming both are valid\n\t"
    menu += "rel -d 'src' 'dest' - deletes a relationship between class 'src' and class 'dest' if one exists\n"

    #List Commands
    menu += "List Flags: \n\t"
    menu += "list -a   - list all classes and their contents in the UML Diagram\n\t"
    menu += "list -c   - list all classes in the UML Diagram\n\t"
    menu += "list -r   - list all relationships in the UML Diagram\n\t"
    menu += "list -d 'name' - list all contents of class 'name'\n"

    #Save Commands
    menu += "Save Flags: \n\t"
    menu += "save 'name' - saves the UML Diagram as a JSON file with name 'name'\n"

    #Load Commands
    menu += "Load Flags: \n\t"
    menu += "load 'name' - loads the file with name 'name.json' if one exists.\n\n"

    #Exit Commands
    menu += "Exit Commands: \n\t"
    menu += "exit   - terminates the program.\n\t"
    menu += "quit   - terminates the program.\n"

    return menu
