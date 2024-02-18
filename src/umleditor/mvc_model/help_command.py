'''Application help menu, to be called when user asks for help.'''
def help_menu():
    """
    Returns a string that contains the menu.
    
    Args:
        None.
        
    Raises:
        None.
        
    Returns:
        str(): The help list to be printed.
    """
    menu = (
        #A general description
        "\nHelp menu:  For the best view, resize your window so that this message and the bar at the end are on one line.    |\n\n"
        "Below are the commands you can call and an explanation of what each does. Anything inside single quotes is decided\n"
        "by you! Enter the command, replacing anything in the single quotes, and the quotes themselves, with the name you\n"
        "want to use.\n\n"
        "A valid name is made up of any combination of letters and numbers.\n\n"
        #Class Commands
        "Class Commands: \n\t"
        "class -a 'name'  - adds a class with name 'name'. Cannot add classes with duplicate or invalid names\n\t"
        "class -d 'name'  - deletes a class with name 'name'\n\t"
        "class -r 'old' 'new' - renames class 'old' to 'new'. Cannot rename classes to duplicate or invalid names\n"
        #Attribute Commands
        "Attribute Commands: \n\t"
        "att -a class 'name' - adds an attribute with name 'name' to class 'class'\n\t"
        "att -d class 'name' - deletes an attribute with name 'name' from class 'class' if one exists\n\t"
        "att -r class 'old' 'new' - renames an attribute from name 'old' to name 'new' in class 'class'\n"
        #Relation Commands
        "Relation Commands:\n\t"
        "rel -a 'src' 'dest' - adds a relationship between class 'src' and class 'dest' assuming both are valid\n\t"
        "rel -d 'src' 'dest' - deletes a relationship between class 'src' and class 'dest' if one exists\n"
        #List Commands
        "List Flags: \n\t"
        "list -a   - list all classes and their contents in the UML Diagram\n\t"
        "list -c   - list all classes in the UML Diagram\n\t"
        "list -r   - list all relationships in the UML Diagram\n\t"
        "list -d 'name' - list all contents of class 'name'\n"
        #Save Commands
        "Save Flags: \n\t"
        "save 'name' - saves the UML Diagram as a JSON file with name 'name'\n"
        #Load Commands
        "Load Flags: \n\t"
        "load 'name' - loads the file with name 'name.json' if one exists.\n\n"
        #Exit Commands
        "Exit Commands: \n\t"
        "exit   - terminates the program.\n\t"
        "quit   - terminates the program.\n"
    )
    return menu
