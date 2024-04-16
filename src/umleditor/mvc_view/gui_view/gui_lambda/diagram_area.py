from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QUrl
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel, QFrame,
                             QFileDialog)
from PyQt6.QtGui import QAction, QPainter, QPen, QColor,QDesktopServices
from umleditor.mvc_view.gui_view.gui_lambda.GUIV2_class_card import ClassCard

class DiagramArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.classCards = {}  # Dictionary to track class cards
        self.lastCardPosition = QPoint(10, 10)  # Initial position for the first card
        self.offsetIncrement = QPoint(15, 15)  # Offset for the next card position
        self.relationships = []

    def initUI(self):
        self.setFixedSize(650, 850)  # Adjust size as necessary
        self.setStyleSheet("background-color: white;")

    def addClassCard(self, classCard, className):
        classCard.setParent(self)
        classCard.move(self.lastCardPosition)
        classCard.show()
        self.lastCardPosition += self.offsetIncrement
        if self.lastCardPosition.x() > self.width() - 100 or self.lastCardPosition.y() > self.height() - 100:
            self.lastCardPosition = QPoint(10, 10)
        self.classCards[className] = classCard  # Store the class card with its name as the key
        classCard.cardMoved.connect(self.update)

    def removeClassCard(self, className):
        if className in self.classCards:
            classCard = self.classCards.pop(className)  
            classCard.deleteLater() 
            
    def renameClassCard(self, old_name, new_name):
        for classCard in self.findChildren(ClassCard):
            if classCard._name == old_name:
                classCard.set_name(new_name)
                
    def clearAll(self):
        """Clears all visual elements from the diagram area."""
        for classCard in self.findChildren(ClassCard):
            classCard.deleteLater()  # Removes the widget and schedules it for deletion
        self.classCards.clear()  # Clear the tracking dictionary
        self.relationships.clear()  # Clear any stored relationships
        self.update()  # Redraw the area
                
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # Set the pen with the correct QColor usage
        painter.setPen(QPen(QColor('black'), 2)) 
        for src, dest in self.relationships:
            if src in self.classCards and dest in self.classCards:
                src_pos = self.classCards[src].centerPos()
                dest_pos = self.classCards[dest].centerPos()
                painter.drawLine(src_pos, dest_pos)

    def addRelationship(self, src_class_name, dest_class_name):
        self.relationships.append((src_class_name, dest_class_name))
        self.update()  # Request a repaint to draw the new line
        
    def removeRelationship(self, src_class_name, dest_class_name):
        self.relationships.remove((src_class_name, dest_class_name))
        self.update()  # Request a repaint to draw the new line