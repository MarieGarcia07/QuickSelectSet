from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from core.MayaWidget import MayaWidget
import maya.cmds as mc
import maya.utils

class QuickSelectSetWidget(MayaWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickSelectSet")

        self.selectedControls = None
        self.selectionSets = []

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

        self.resetSelectionBtn = QPushButton("Reset Selection")
        self.resetSelectionBtn.clicked.connect(self.ResetSelectionBtnClicked)
        self.masterLayout.addWidget(self.resetSelectionBtn)

        self.setNameBtn = QPushButton("Create Selection Set")
        self.setNameBtn.clicked.connect(self.SetNameBtnClicked)
        self.masterLayout.addWidget(self.setNameBtn)



    def GetWidgetHash(self):
        return "3e4ad28da57f3aff2c91972c083aabecbe5cd75559d58f77a8fce537d22908cc"

    def SetNameBtnClicked(self):
        self.name = self.nameLineEdit.text()

        if not self.name or not self.selectedControls:
            return
        
        controls = list(self.selectedControls)

        setData = {"name": self.name, "controls": controls}
        self.selectionSets.append(setData)
        
        rowLayout = QHBoxLayout()
        self.masterLayout.addLayout(rowLayout)

        selectBtn = QPushButton(self.name)
        rowLayout.addWidget(selectBtn)

        print("TYPE:", type(controls), controls)
        selectBtn.clicked.connect(lambda c=controls: self.SelectSet(c))

        addBtn = QPushButton("+")
        rowLayout.addWidget(addBtn)
        addBtn.clicked.connect(lambda _, s=setData: self.AddToSet(s))

        deleteBtn = QPushButton("Delete")
        rowLayout.addWidget(deleteBtn)
        deleteBtn.clicked.connect(lambda _, l=rowLayout, s=setData: self.DeleteSet(l, s))
    
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

    def AddToSet(self, setData):
        selection = mc.ls(selection=True)
        if not selection:
            return
        
        for obj in selection:
            if obj not in setData["controls"]:
                setData["controls"].append(obj)
    
    def DeleteSet(self, layout, setData):
        if setData in self.selectionSets:
            self.selectionSets.remove(setData)
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.masterLayout.removeItem(layout)

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
