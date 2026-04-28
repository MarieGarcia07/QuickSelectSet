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

        self.nameLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.nameLayout)
        self.nameLayout.addWidget(QLabel("Name:"))

        self.nameLineEdit = QLineEdit()
        self.nameLayout.addWidget(self.nameLineEdit)

        controlSelectLayout = QHBoxLayout()
        self.masterLayout.addLayout(controlSelectLayout)
        controlSelectLayout.addWidget(QLabel("Controls:"))
        self.controlSelectLineEdit = QLineEdit()
        self.controlSelectLineEdit.setEnabled(False)
        controlSelectLayout.addWidget(self.controlSelectLineEdit)
        controlSelectBtn = QPushButton("<<<")
        controlSelectLayout.addWidget(controlSelectBtn)
        controlSelectBtn.clicked.connect(self.ControlSelectBtnClicked)

        self.setNameBtn = QPushButton("Create Selection Set")
        self.setNameBtn.clicked.connect(self.SetNameBtnClicked)
        self.masterLayout.addWidget(self.setNameBtn)

    def SetNameBtnClicked(self):
        self.name = self.nameLineEdit.text()
        self.control = self.controlSelectLineEdit()

        if not self.name & self.control:
            return
        
        nameSelectBtn = QPushButton(self.name)
        self.masterLayout.addWidget(nameSelectBtn)


    def ControlSelectBtnClicked(self):
        pass


def Run():
    quickSelectSetWidget = QuickSelectSetWidget()
    quickSelectSetWidget.show()

Run()
