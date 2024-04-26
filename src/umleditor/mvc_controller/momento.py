import os
from umleditor.custom_exceptions import CustomExceptions as CE


class Momento:
    def __init__(self, controller):
        """
        Initializes the Momento with a reference to the controller.

        ## Parameters:
        - `controller`: The controller instance that manages application state.
        """
        self.controller = controller
        # Set guarantees no duplicates
        self.temp_files = set()

    def save_state(self, state_id):
        """
        Saves the current state of the application using a unique state identifier.

        ## Parameters:
        - `state_id` (str): A unique identifier for the state to be saved.
        """
        # Generate a unique filename for the state
        filename = f'state_{state_id}'
        # Use the controller's save method to serialize the state
        self.controller.save(filename)
        # Keep track of the temporary files
        self.temp_files.add(filename)

    def load_state(self, state_id):
        """
        Loads a previously saved state of the application using the state identifier.

        ## Parameters:
        - `state_id` (str): The identifier of the state to be loaded.

        ## Raises:
        - `RedoStateError`: If the specified state cannot be found or loaded.
        """
        # Generate the filename from the state_id
        filename = f'state_{state_id}'
        # Use the controller's load method to deserialize the state
        try:
            self.controller.load(filename)
        except Exception:
            raise CE.RedoStateError()

    def cleanup_states(self):
        """
        Cleans up all temporary state files created during the application's runtime.
        """
        # Remove all temporary JSON files
        save_path = os.path.join(os.path.dirname(__file__), '../', '../', '../', 'save')
        for filename in self.temp_files:
            try:
                os.remove(os.path.join(save_path, filename+'.json'))
            except OSError as e:
                print(f"Error deleting file {filename}: {e.strerror}")
        self.temp_files = set()

    def non_state_changing_commands(self)-> set[str]:
        """
        Returns a set of command names that do not change the application state.

        ## Returns:
        - `set[str]`: A set of command names.
        """
        return {"list_everything",
                "list_entity_details",
                "list_entities",
                "list_relations",
                "list_entity_relations",
                "undo",
                "redo",
                "save",
                "load",
                "exit",
                "quit",
                "help_menu"}
