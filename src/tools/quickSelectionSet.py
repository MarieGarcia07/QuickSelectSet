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
        self.nameLayout.addWidget(QLabel("Name Base:"))

        self.nameLineEdit = QLineEdit()
        self.nameLayout.addWidget(self.nameLineEdit)

        self.setNameBtn = QPushButton("Set Name of Selection")
        self.setNameBtn.clicked.connect(self.SetNameBtnClicked)
        self.nameLayout.addWidget(self.setNameBtn)

        selectSetLayout = QHBoxLayout()
        self.masterLayout.addLayout(selectSetLayout)
        selectSetLayout.addWidget(QLabel("Select Group:"))
        self.selectSetLineEdit = QLineEdit()
        self.selectSetLineEdit.setEnabled(False)
        selectSetLayout.addWidget(self.selectSetLineEdit)
        controlSelectBtn = QPushButton("<<<")
        selectSetLayout.addWidget(controlSelectBtn)
        controlSelectBtn.clicked.connect(self.ControlSelectBtnClicked)

    def SetNameBtnClicked(self):
        name = self.nameLineEdit.text()

        if not name:
            return
        
        nameSelectBtn = QPushButton(name)
        self.quickSelectLayout.addWidget(nameSelectBtn)


    def ControlSelectBtnClicked(self):
        pass


def Run():
    quickSelectSetWidget = QuickSelectSetWidget()
    quickSelectSetWidget.show()

Run()
