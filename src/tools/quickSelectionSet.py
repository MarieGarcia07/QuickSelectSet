from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from core.MayaWidget import MayaWidget
import maya.cmds as mc
import maya.utils
from functools import partial

class QuickSelectSet():
    def __init__(self):
        pass

    def CreateSet(self, name, controls):
        if not controls:
            return
        
        if mc.objExists(name):
            mc.delete(name)
        
        mc.sets(controls, name=name)

    def SelectSet(self, name):
        if not mc.objExists(name):
            print(f"Set {name} does not exist")
            return
        
        members = mc.sets(name, q=True)

        if not members:
            print(f"Set {name} is empty")
            return

        mc.select(members)
    


class QuickSelectSetWidget(MayaWidget):
    def __init__(self):
        super().__init__()
        self.quickSelectSet = QuickSelectSet()  #
        self.setWindowTitle("QuickSelectSet")

        self.selectedControls = None
        self.selectionSets = []

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.nameLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.nameLayout)
        self.nameLayout.addWidget(QLabel("Name:"))

        self.nameLineEdit = QLineEdit() # have this not selected when clicking set
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

        self.resetSelectionBtn = QPushButton("Reset Selection")
        self.resetSelectionBtn.clicked.connect(self.ResetSelectionBtnClicked)
        self.masterLayout.addWidget(self.resetSelectionBtn)

        self.setNameBtn = QPushButton("Create Selection Set")
        self.setNameBtn.clicked.connect(self.SetNameBtnClicked)
        self.masterLayout.addWidget(self.setNameBtn)

    def GetWidgetHash(self):
        return "3e4ad28da57f3aff2c91972c083aabecbe5cd75559d58f77a8fce537d22908cc"

    def SetNameBtnClicked(self):
        name = self.nameLineEdit.text()

        if not name or not self.selectedControls:
            return

        controls = self.selectedControls

        self.quickSelectSet.CreateSet(name, controls)

        uiBtn = QPushButton(name)
        self.masterLayout.addWidget(uiBtn)

        uiBtn.clicked.connect(partial(self.quickSelectSet.SelectSet, name))
    
    def ResetSelectionBtnClicked(self):
        self.nameLineEdit.clear()
        self.controlSelectLineEdit.clear()
        self.selectedControls = None

    def ControlSelectBtnClicked(self):
        selection = mc.ls(selection=True)

        if not selection:
            return
        
        self.selectedControls = selection
        self.controlSelectLineEdit.setText(", ".join(selection))

    def SelectSet(self, controls):
        print("Selecting:", controls)

        if not controls:
            print("No valid controls stored")
            return
        
        controls = [c for c in controls if isinstance(c, str)]

        if not controls:
            print("All controls invalid")
            return
        
        mc.select(controls)

def Run():
    quickSelectSetWidget = QuickSelectSetWidget()
    quickSelectSetWidget.show()

Run()
