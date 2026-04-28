from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from core.MayaWidget import MayaWidget
import maya.cmds as mc

class QuickSelectSet():
    def __init__(self):
        pass

    def SelectControls(self):
        # grabs controls that are selected and keeps it in memory
        pass

    def SelectionSet(self):
        # has it so that when you click the button, it grabs SelectControls()
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
        self.controlSelectLineEdit = QLineEdit() # CHANGE THIS (for widget not controls)
        self.controlSelectLineEdit.setEnabled(False)
        controlSelectLayout.addWidget(self.controlSelectLineEdit)
        controlSelectBtn = QPushButton("<<<")
        controlSelectLayout.addWidget(controlSelectBtn)
        controlSelectBtn.clicked.connect(self.ControlSelectBtnClicked)

        self.setNameBtn = QPushButton("Create Selection Set")
        self.setNameBtn.clicked.connect(self.SetNameBtnClicked)
        self.masterLayout.addWidget(self.setNameBtn)

    def GetWidgetHash(self):
        return "3e4ad28da57f3aff2c91972c083aabecbe5cd75559d58f77a8fce537d22908cc"

    def SetNameBtnClicked(self):
        self.name = self.nameLineEdit.text()

        if not self.name(self, "selectedControls"):
            return
        
        controls = self.selectedControls
        
        nameSelectBtn = QPushButton(self.name)
        self.masterLayout.addWidget(nameSelectBtn)
        nameSelectBtn.clicked.connect(lambda: mc.select(controls))


    def ControlSelectBtnClicked(self):
        selection = mc.ls(selection=True)

        if not selection:
            return
        
        self.selectedControls = selection

        self.controlSelectLineEdit.setText(", ".joint(selection))


def Run():
    quickSelectSetWidget = QuickSelectSetWidget()
    quickSelectSetWidget.show()

Run()
