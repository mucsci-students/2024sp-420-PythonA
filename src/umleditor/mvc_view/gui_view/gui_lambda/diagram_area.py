from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QUrl
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel, QFrame,
                             QFileDialog)
from PyQt6.QtGui import QAction, QPainter, QPen, QColor,QDesktopServices, QPixmap
from umleditor.mvc_view.gui_view.gui_lambda.class_card_revamp import ClassCard

class DiagramArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.classCards = {}  # Dictionary to track class cards
        self.lastCardPosition = QPoint(10, 10)  # Initial position for the first card
        self.offsetIncrement = QPoint(15, 15)  # Offset for the next card position
        self.relationships = []

    def initUI(self):
        self.setStyleSheet("background-color: white;")

    def addClassCard(self, classCard, className):
        classCard.setParent(self)
        classCard.show()
        classCard.cardMoved.connect(lambda: self.updateEntityPosition(classCard))

        self.classCards[className] = classCard  
        
        if classCard._entity and hasattr(classCard._entity, '_location') and classCard._entity._location:
            classCard.move(classCard._entity._location[0], classCard._entity._location[1])

    def removeClassCard(self, className):
        if className in self.classCards:
            classCard = self.classCards.pop(className)  
            classCard.deleteLater() 
            
    def renameClassCard(self, old_name, new_name):
        for classCard in self.findChildren(ClassCard):
            if classCard._name == old_name:
                classCard.set_name(new_name)
    
    def updateEntityPosition(self, classCard):
        if classCard._entity:
            # Get the new position from the ClassCard
            newPosition = classCard.pos()
            # Update the entity's location
            classCard._entity._location = [newPosition.x(), newPosition.y()]
            
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
        
    def exportAsImage(self, filePath):
        # Create a QPixmap object with the same dimensions as the DiagramArea
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.white)  # Fill the pixmap with white background

        # Create a QPainter to draw on the pixmap
        painter = QPainter(pixmap)
        self.render(painter)  # This draws the entire content of the DiagramArea onto the pixmap
        painter.end()

        # Save the pixmap as a PNG file
        pixmap.save(filePath, "PNG")