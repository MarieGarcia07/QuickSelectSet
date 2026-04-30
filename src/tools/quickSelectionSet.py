from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from core.MayaWidget import MayaWidget
import maya.cmds as mc
from functools import partial

SET_PREFIX = "QSS_"

class QuickSelectSet():
    def __init__(self):
        pass

    def CreateSet(self, name, controls):
        if not controls:
            return
        
        setName = f"{SET_PREFIX}{name}"

        if mc.objExists(setName):
            mc.delete(setName)
        
        controls = [c for c in controls if mc.objExists(c)]

        if not controls:
            return
        
        mc.sets(controls, name=setName)

    def SelectSet(self, name):
        setName = f"{SET_PREFIX}{name}"

        if not mc.objExists(setName):
            print(f"Set {setName} does not exist")
            return
        
        members = mc.sets(setName, q=True)

        if not members:
            print(f"Set {setName} is empty")
            return

        mc.select(members)
    


class QuickSelectSetWidget(MayaWidget):
    def __init__(self):
        super().__init__()
        self.quickSelectSet = QuickSelectSet()  #
        self.setWindowTitle("QuickSelectSet")

        self.selectedControls = None

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

        self.setsLayout = QVBoxLayout()
        self.masterLayout.addLayout(self.setsLayout)

        self.LoadExistingSets()

    def GetWidgetHash(self):
        return "3e4ad28da57f3aff2c91972c083aabecbe5cd75559d58f77a8fce537d22908cc"

    def ControlSelectBtnClicked(self):
        selection = mc.ls(selection=True)

        if not selection:
            return
        
        self.selectedControls = selection
        self.controlSelectLineEdit.setText(", ".join(selection))

    def ResetSelectionBtnClicked(self):
        self.nameLineEdit.clear()
        self.controlSelectLineEdit.clear()
        self.selectedControls = None

    def SetNameBtnClicked(self):
        name = self.nameLineEdit.text()

        if not name or not self.selectedControls:
            return

        self.quickSelectSet.CreateSet(name, self.selectedControls)

        self.AddSetButton(name)

        self.ResetSelectionBtnClicked()
    
    def AddSetButton(self, name):
        uiBtn = QPushButton(name)
        self.setsLayout.addWidget(uiBtn)

        uiBtn.clicked.connect(partial(self.quickSelectSet.SelectSet, name))

    def LoadExistingSets(self):
        allSets = mc.ls(type="objectSet") or []

        for s in allSets:
            if not s.startswith(SET_PREFIX):
                continue

            displayName = s.replace(SET_PREFIX, "")
            self.AddSetButton(displayName)

def Run():
    quickSelectSetWidget = QuickSelectSetWidget()
    quickSelectSetWidget.show()

Run()
