import pprint
from maya import cmds
import controllerLibrary
reload(controllerLibrary)
from PySide2 import QtWidgets, QtCore, QtGui

class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The ControllerLibraryUI is a dialog that lets us save and import controllers
    """

    def __init__(self):
        # The 'super' class we are inheriting from is QtWidgets.QDialog
        # We use this so we don't have to specify where we are inheriting from
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library')

        # The library variable points to an instance of out controller library
        self.library = controllerLibrary.ControllerLibrary()

        # Every time we create a new instance we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """This method builds out the UI"""
        # Create Vertical Box Layout (Column layout)
        # This is the master layout
        layout = QtWidgets.QVBoxLayout(self)

        # ------------- CREATE UPPER SAVE LAYOUT OF UI -------------
        # This is a child horizontal widget
        saveWidget = QtWidgets.QWidget()
        # Lays out any children horizontally (Row Layout)
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        # Create Text Enter Field
        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        # Create Save Button
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # ------------- CREATE THUMBNAIL VIEW LAYOUT OF UI -------------
        # These are the parameters for our thumbnail size
        size = 64
        buffer = 12

        # This will create a grid list widget to display our controller thumbnails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        # Set size of icons
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        # Set Icon flow when window is resized
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        # Add buffer space in between icons
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))

        layout.addWidget(self.listWidget)

        # ------------- CREATE BOTTOM BUTTON LAYOUT OF UI -------------
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        # When the close button is clicked, connect it to the close method defined in QDialog
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        """This clears the list widget, and then repopulates it with the contents of our library"""
        # Clear out existing items in list widget, so when we add them in again, the amount doesn't double
        self.listWidget.clear()
        # Find all the existing controllers in the library
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)  # type: QListWidgetItem
            self.listWidget.addItem(item)


            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load(self):
        """This loads the currently selected controller"""
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """This saves the controller with the given file name"""
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name!")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')

def showUI():
    """
    This shows and returns a handle to the ui
    Returns:
        QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui
