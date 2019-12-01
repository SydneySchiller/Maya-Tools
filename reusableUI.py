from tweenerUI import tween
from gearClassCreator import Gear
from maya import cmds


class BaseWindow(object):
    """
    This class creates a window that allows the user to easily alter the percentage in which they would like to tween.
    The window includes a slider to set tween percentage.
    """

    windowName = "BaseWindow"

    def show(self):
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()

        cmds.showWindow()

    def buildUI(self):
        pass

    def reset(self, *args):
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)


class TweenerWindow(BaseWindow):
    windowName = "TweenerWindow"

    def buildUI(self):
        column = cmds.columnLayout()

        cmds.text(label="Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)

        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)


class GearWindow(BaseWindow):
    windowName = "GearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the gear")

        cmds.rowLayout(numberOfColumns=4)

        self.label = cmds.text(label="10")

        # This slider type changes the gear in real time
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)
        cmds.button(label="Make Gear", command=self.makeGear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def makeGear(self, *args):
        teeth = cmds.intSlider(self.slider, query=True, value=True)

        self.gear = Gear()

        self.gear.createGear(teeth=teeth)

        # Delect the active faces
        cmds.select(clear=True)

    def modifyGear(self, teeth):
        if self.gear:
            self.gear.changeTeeth(teeth=teeth)

        cmds.text(self.label, edit=True, label=teeth)

    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, edit=True, value=10)
        cmds.text(self.label, edit=True, label=10)
