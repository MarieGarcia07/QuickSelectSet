from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from core.MayaWidget import MayaWidget
import maya.cmds as mc

class QuickSelectSet():
    def __init__(self):
        pass

class QuickSelectSetWidget(MayaWidget):
    def __init__(self):
        super().__init__()
        self.quickSelectSet = QuickSelectSet()
        self.setWindowTitle("QuickSelectSet")

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        selectSetLayout = QHBoxLayout()
        self.masterLayout.addLayout(selectSetLayout)

def Run():
    quickSelectSetWidget = QuickSelectSetWidget()
    quickSelectSetWidget.show()

Run()
