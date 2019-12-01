from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):
    """
    This method tweens an object.
    Args:
        percentage: The percentage to tween to
        obj: The object that we are tweening
        attrs: Which attributes to tween
        selection: The selection we want to tween

    """
    # Throw an error if there is no specified obj and no obj selected
    if not obj and not selection:
        raise ValueError("No object given to tween")

    # if no obj is specified, get it from the first selection
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)

    currentTime = cmds.currentTime(query=True)

    for attr in attrs:

        # Construct the full name of the attribute with its object
        attrFull = '%s.%s' % (obj, attr)

        # Get the keyframes off the attribute on this object
        keyframes = cmds.keyframe(attrFull, query=True)

        # If there are no keyframes then continue
        if not keyframes:
            continue

        # previousKeyframes = []
        # for frames in keyframes:
        #     if frames < currentTime:
        #         previousKeyframes.append(frames)

        # Makes a list of previous key frames
        # Can also be written like the code above
        previousKeyframes = [frame for frame in keyframes if frame < currentTime]

        # Makes a list of the later key frames
        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue


        # if previousKeyframes:
        #     previousFrame = max(previousKeyframes)
        # else:
        #     previousFrame = None

        # This goes through the entire previousKeyframes list, and finds the max out of all of them
        # This max is the keyframe closest to us
        # Can also be written like the code above
        previousFrame = max(previousKeyframes) if previousKeyframes else None
        nextFrame = min(laterKeyframes) if laterKeyframes else None

        if not previousFrame or not nextFrame:
            continue

        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)

        difference = nextValue - previousValue
        weightedDifference = (difference * percentage) / 100.0
        currentValue = previousValue + weightedDifference

        cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)


class TweenWindow(object):

    """
    This class creates a window that allows the user to easily alter the percentage in which they would like to tween.
    The window includes a slider to set tween percentage.
    """

    windowName = "TweenerWindow"

    def show(self):

        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()

        cmds.showWindow()

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

    def close(self, *args):
        cmds.deleteUI(self.windowName)
