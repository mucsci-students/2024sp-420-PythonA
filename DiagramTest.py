from Diagram import Diagram
from CustomExceptions import CustomExceptions

# Instantiate the Diagram class
diagram = Diagram()

# Add some classes to the diagram
try:
    diagram.addClass("Class1")
    diagram.addClass("Class1")
    diagram.addClass("Class2")
    print("Classes added successfully!")
except ValueError as ve:
    print(ve)
except CustomExceptions.EntityExistsError as ee:
    print(ee)
# Print the entities in the diagram
print("Entities in the diagram:")
for name, entity in diagram._entities.items():
    print(name)
