from maya import cmds

def createGear(teeth=10, length=0.3):
    """
    This function will create a gear with the given parameters
    Args:
        teeth: The number of teeth to create
        length: The length of the teeth

    Returns:
        A tuple of the transform, constructor, and extrude node
    """

    # Teeth are every alternate face, so spans x 2
    spans = teeth * 2

    # Create a pipe with the specified number of teeth
    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    # Find every other face on pipe
    sideFaces = range(spans*2, spans*3, 2)

    cmds.select(clear=True)

    # Select every other face on pipe
    for face in sideFaces:
        cmds.select('%s.f[%s]' % (transform, face), add=True)

    # Extrude the selected faces
    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
    return transform, constructor, extrude

def changeTeeth(constructor, extrude, teeth=10, length=0.3):

    # Change the number of faces on the polyPipe
    spans = teeth*2

    cmds.polyPipe(constructor, edit=True, subdivisionsAxis=spans)

    # Create a list to store all our faces
    sideFaces = range(spans*2, spans*3, 2)
    faceNames = []

    for face in sideFaces:
        faceName = 'f[%s]' % (face)
        faceNames.append(faceName)

    # Extrude the correct faces
    cmds.setAttr('%s.inputComponents' % (extrude),
                 len(faceNames),
                 *faceNames,
                 type="componentList")

    # Change the length of the teeth
    # ltz is the short form of localTranslateZ
    cmds.polyExtrudeFacet(extrude, edit=True, ltz=length)
