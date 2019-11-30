# Maya-Tools

### ObjectRenamer.py
This tool scans through the existing items (Lights, Models, Joints, etc.) in the scene and applies a suffix to the end of each name. This establishes a common naming convention for the Maya project.

Lights &rarr; \_lgt \
Polygonal Model &rarr; \_geo \
Joints &rarr; \_jnt

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
