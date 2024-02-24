from PyQt6.QtWidgets import QLineEdit

class CustomLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def focusOutEvent(self, event):
        # Prevent the QLineEdit from losing focus
        pass
    
    def mousePressEvent(self, event):
        # Ensure the QLineEdit keeps the focus when clicked
        self.setFocus()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Ensure the QLineEdit keeps the focus when released
        self.setFocus()
        super().mouseReleaseEvent(event)