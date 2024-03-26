from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMenuBar, QApplication
from PyQt6.QtGui import QAction
from umleditor.mvc_view.gui_view.class_card import ClassCard
from .class_input_dialog import CustomInputDialog
from umleditor.mvc_controller.gui_controller import ControllerGUI


class GuiV2(QMainWindow):
    def __init__(self, controller: ControllerGUI):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle("UML Editor - GUI V2")
        self.setGeometry(300, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.add_class_button = QPushButton("Add a New Class", self)
        self.add_class_button.clicked.connect(self.on_add_class_clicked)
        layout.addWidget(self.add_class_button)

        central_widget.setLayout(layout)

        # More GUI

    def on_add_class_clicked(self):
        # Do add class things
        dialog = CustomInputDialog("Add Class", self)
        if dialog.exec() == CustomInputDialog.Accepted:
            class_name = dialog.input_text.text()
            self.add_class_card(class_name)

    def add_class_card(self, class_name: str):
        # Class card stuff
        print(f"Class {class_name} added")


if __name__ == "__main__":
    app = QApplication([])
    controller = ControllerGUI()  # Ensure this is initialized correctly for your app
    gui = GuiV2(controller)
    gui.show()
    app.exec()
