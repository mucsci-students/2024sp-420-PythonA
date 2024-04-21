import math

from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QUrl
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel, QFrame,
                             QFileDialog)
from PyQt6.QtGui import QAction, QPainter, QPen, QColor, QDesktopServices, QPixmap, QPolygon
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
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # For smoother lines

        for src, dest, rel_type in self.relationships:
            if src in self.classCards and dest in self.classCards:
                src_pos = self.classCards[src].centerPos()
                dest_pos = self.classCards[dest].centerPos()

                # Set styles based on relationship type
                if rel_type == 'realization':
                    painter.setPen(QPen(QColor('black'), 2, Qt.PenStyle.SolidLine))
                elif rel_type == 'aggregation':
                    painter.setPen(QPen(QColor('blue'), 2, Qt.PenStyle.DashLine))
                    self.drawArrow(painter, src_pos, dest_pos, QColor('blue'))
                elif rel_type == 'composition':
                    painter.setPen(QPen(QColor('green'), 3, Qt.PenStyle.DashDotLine))
                    self.drawArrow(painter, src_pos, dest_pos, QColor('green'))
                elif rel_type == 'inheritance':
                    painter.setPen(QPen(QColor('red'), 2, Qt.PenStyle.DotLine))
                    self.drawArrow(painter, src_pos, dest_pos, QColor('red'))

                painter.drawLine(src_pos, dest_pos)

    def drawArrow(self, painter, src_pos, dest_pos, color):
        # Arrowhead drawing
        arrow_size = 10
        painter.setBrush(color)

        angle = math.atan2(-(dest_pos.y() - src_pos.y()), dest_pos.x() - src_pos.x())
        arrow_p1 = dest_pos + QPoint(math.sin(angle - math.pi / 3) * arrow_size,
                                     math.cos(angle - math.pi / 3) * arrow_size)
        arrow_p2 = dest_pos + QPoint(math.sin(angle - math.pi + math.pi / 3) * arrow_size,
                                     math.cos(angle - math.pi + math.pi / 3) * arrow_size)

        arrow_head = QPolygon([dest_pos, arrow_p1, arrow_p2])
        painter.drawPolygon(arrow_head)

    def addRelationship(self, src_class_name, dest_class_name, rel_type):
        self.relationships.append((src_class_name, dest_class_name, rel_type))
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