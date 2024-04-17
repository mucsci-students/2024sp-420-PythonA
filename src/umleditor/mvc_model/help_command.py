# Primary: Danish
# Secondary: Zhang

"""Application help menu, to be called when user asks for help."""
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
        "\nHelp menu:  For the best view, resize your window so that this message and the bar at the end are on one line.        |\n\n"
        "Below are the commands you can call and an explanation of what each does. Anything inside single quotes is decided\n"
        "by you! Enter the command, replacing anything in the single quotes, and the quotes themselves, with the name you\n"
        "want to use.\n\n"
        "- A valid name is made up of any combination of alphnumeric characters, -, and _.\n"
        "- Duplicates names are not allowed for an classes or attributes within a class.\n\n"
        #Class Commands
        "Class Commands:\n\t"
        "class -a 'name' - adds a class with name 'name'\n\t"
        "class -d 'name' - deletes a class with name 'name'\n\t"
        "class -r 'old' 'new' - renames the class named 'old' to 'new'\n"
        #Field Commands
        "Field Commands: \n\t"
        "fld -a 'class' 'name' 'type'- adds a field named 'name' and it's type 'type' to the class named 'class'\n\t"
        "fld -d 'class' 'name'  - deletes a field named 'name' and it's type 'type' from the class named 'class'\n\t"
        "fld -r 'class' 'old' 'old_type' 'new' 'new_type' - renames a field named 'old' to name 'new' in the class 'class'\n"
        #Method Commands
        "Method Commands:\n\t"
        "mthd -a 'class' 'name' 'returnType' - adds a method with the name 'name' and returnType 'returnType' to the class 'class'\n\t"
        "mthd -d 'class' 'name' - deletes a method with name 'name' from class 'class'\n\t"
        "mthd -r 'class' 'old' 'new' - renames a method form name 'old' to name 'new' in class 'class'\n"
        #Paramater Commands
        "Parameter Commands:\n\t"
        "prm -a 'class' 'mthd' 'prm'  - adds a param to a method \n\t"
        "prm -d 'class' 'mthd' 'prm'  - deletes the param from the method if it exists\n\t"
        "prm -r 'class' 'mthd' 'old' 'new'  - replaces the 'old' param in the method with the 'new' param\n"
        #Relation Commands
        "Relation Commands:\n\t"
        "rel -a 'src' 'dest' 'type' - adds a relationship between class 'src' and class 'dest' of type 'type'\n\t"
        "\tRelationship types: 'aggregation', 'composition', 'inheritance', 'realization'\n\t"
        "rel -t 'src' 'dest' 'type' - changes the type of the relationship between class 'src' and class 'dest' to 'new type'\n\t"
        "rel -d 'src' 'dest' - deletes a relationship between class 'src' and class 'dest'\n"
        #List Commands
        "List Flags: \n\t"
        "list -a   - list all classes and their contents in the UML Diagram\n\t"
        "list -c   - list all classes in the UML Diagram\n\t"
        "list -r   - list all relationships in the UML Diagram\n\t"
        "list -d 'name' - list all contents of class 'name'\n"
        #Redo&Undo Commands
        "Undo and Redo Commands:\n\t"
        "undo - reverts the last change made to the UML Diagram\n\t"
        "redo - reapplies the last change that was undone\n"
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
