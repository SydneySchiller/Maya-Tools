# Maya-Tools

### ObjectRenamer.py
This tool scans through the existing items (Lights, Models, Joints, etc.) in the scene and applies a suffix to the end of each name. This establishes a common naming convention for the Maya project.

Lights &rarr; \_lgt \
Polygonal Model &rarr; \_geo \
Joints &rarr; \_jnt

Usage is as follows:
```python
import objectRenamer
reload(objectRenamer)
objectRenamer.rename()
```

_To Do: Add more suffixes_

### GearCreator.py and GearClassCreator.py
Both of these tools procedurally generates models of gears within the scene.\
_GearCreator.py_ is done using python functions.\
_GearClassCreator.py_ is done using classes within python.\
Both of these files have a _createGear_ method, which takes a _teeth_ variable and a _length_ variable. Teeth specifies the number of teeth the gear should have, while length specifies the length of the teeth.\
The files also contain a _changeTeeth_ method, which takes the same variables as before, but alters the existing specified gear.

Below is a sample use of the tool.
```python
import gearClassCreator
reload(gearClassCreator)

gear = gearClassCreator.Gear()
gear.createGear()
gear.changeTeeth(30, 0.75)
```

### TweenerUI.py
This tool helps animators to tween in between keyframes.

By entering the following code into the Maya scripting panel, a tweening window appears, which includes a slider and reset button. The slider, once adjusted, will set a new keyframe or set the existing keyframe at the specified percentage. The left side of the slider represents 0% and the right side represents 100%.

```python
import tweenerUI
reload(tweenerUI)

tweenerUI.TweenWindow().show()
```

After adjusting the slider, you can hit the reset button, which resets the slider back to 50% (the middle of the slider) without setting a new keyframe.

### reusableUI.py
This tool contains a base class to create a window. Inside this base class, called _BaseWindow_, there are methods for show, buildUI, reset, and close. If this class is used, an empty window will appear.

Following the base class, a child class called _TweenerWindow_ is specified. This window has the same functionality of TweenerUI.py.

Another child of BaseWindow is _GearWindow_, which uses the functionality of GearClassCreator.py within a window. If the user hits the _Make Gear_ button, a gear object will appear on screen. Then, you can move the slider to alter the amount of teeth in real time. If the _reset_ button is pressed, the gear will no longer be the active gear, and the slider is set back to its base amount.

_To Do: Make slider for GearWindow to alter teeth length_
