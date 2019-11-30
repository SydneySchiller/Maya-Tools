from maya import cmds

SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
    "ambientLight": "lgt"
}

DEFAULT_SUFFIX = "grp"

def rename(selection=False):
    """
    This function will rename any objects to have the correct suffix
    Args:
        selection: Whether or not we use the current selection

    Returns:
        A list of all the objects we operated on

    """
    #if there is nothing selected then list everything in the outliner
    objects = cmds.ls(selection=selection, dag=True, long=True)

    #This function cannot run if there is no selection and no objects
    if selection and not objects:
        raise RuntimeError("You don't have anything selected.")

    #sort selection list to be longest in length to shortest
    objects.sort(key=len, reverse=True)

    #iterate through sorted list
    #make each item a list, and tokenize it by "|"
    #then select the last item in each list
    for obj in objects:
        shortName = obj.split("|")[-1]

        #get object type of item.
        #if the item is not a list then make it a list
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        #find suffix in dictionary SUFFIX
        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

        if not suffix:
            continue

        #if the item already has a suffix, then do not add it again!
        if obj.endswith('_'+suffix):
            continue

        newName = "%s_%s" % (shortName, suffix)

        cmds.rename(obj, newName)

        #replace previous object names with new object names
        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)

    return objects
