# Quick Select Set Tool
## Overview
This maya tool allows users to quickly create, manage, and reselect groups of controls using simple UI.

## How To Install
1. Open Maya
2. Drag and drop the install file into the Maya viewport

## Tech Stack
|Tool  |Version|
|----  |------|
|Python| 3.12 |
|Pyside|  6   |
|Maya  |>=2025|

## Features

* Create named selection sets
* Prevents anything that aren't valid from being selected
* Prevents duplicated sets
* Quickly reselect controls
* Remembers and loads existing sets
* Reset UI inputs

## Structure

The tool is composed of the following major classes:

### Quick Select Set Class

The ```QuickSelectSet``` class has the following responsibilities:

* Validates input before creating sets
* Retrieves and selects stored set members

#### CreateSet method:
* Raises error if no controls are selected
* Applies the  ```QSS_``` prefix to the set name
* Prevents duplicate set
* Filters invalid objects
* Creates a maya set
```python
def CreateSet(self, name, controls):
        if not controls:
            raise Exception("No controls provided to create a set.")
        
        setName = f"{SET_PREFIX}{name}"

        if mc.objExists(setName):
            raise Exception("Set already exists.")
            mc.delete(setName)
        
        controls = [c for c in controls if mc.objExists(c)]

        if not controls:
            raise Exception("Controls do not exist.")
        
        mc.sets(controls, name=setName)
```

#### SelectSet method:
* Verifies the set exists
* Retrieves members using ```mc.sets(..., q=True)```
* Raises error if the set is empty
* Selects all members in maya
  
  ```Python
  def SelectSet(self, name):
        setName = f"{SET_PREFIX}{name}"

        if not mc.objExists(setName):
            raise Exception(f"Set {setName} does not exist")
        
        members = mc.sets(setName, q=True)

        if not members:
            raise Exception(f"Set {setName} is empty")

        mc.select(members)
  ```

### Quick Select Set Widget Class

The ```QuickSelectSetWidget``` class has the following responsibilities:

* Creates UI layout
* Handles user interaction

#### ControlSelectBtnClicked method:
* Reads current Maya selection
* Stores it
```Python
selection = mc.ls(selection=True)
...
self.selectedControls = selection
        self.controlSelectLineEdit.setText(", ".join(selection))
```
#### ResetSelectionBtnClicked method:
* Clears name input
* Clears selected controls
* Resets state
```Python
def ResetSelectionBtnClicked(self):
        self.nameLineEdit.clear()
        self.controlSelectLineEdit.clear()
        self.selectedControls = None
```
#### SetNameBtnClicked method:
* Validates name and selection
* Calls ```CreateSet```
* Adds new button for the set
* Resets UI afterward
```Python
self.quickSelectSet.CreateSet(name, self.selectedControls)
self.AddSetBtn(name)
self.ResetSelectionBtnClicked()
```
#### AddSetBtn method:
* Creates a button for a saved set
* Connects it to ```SelectSet```
* Allows reselection
```Python
def AddSetBtn(self, name):
        uiBtn = QPushButton(name)
        self.setsLayout.addWidget(uiBtn)
        uiBtn.clicked.connect(partial(self.quickSelectSet.SelectSet, name))
```
#### LoadExistingSets method:
* Finds all maya sets
* Filters by ```QSS_``` prefix
* Recreates UI buttons for existing sets
```Python
def LoadExistingSets(self):
        allSets = mc.ls(type="objectSet") or []

        for s in allSets:
            if not s.startswith(SET_PREFIX):
                continue

            displayName = s.replace(SET_PREFIX, "")
            self.AddSetBtn(displayName)
```

