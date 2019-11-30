from maya import cmds

class Gear(object):

    """
    This is a Gear object that allows us to create and modify a gear.
    """

    def __init__(self):

        # The __init__ method lets us set default values
        self.transform = None
        self.extrude = None
        self.constructor = None

    def createGear(self, teeth=10, length=0.3):

        """
        This method creates a gear
        Args:
            teeth: The number of teeth the gear should have
            length: The length of the teeth

        """

        # Teeth are every alternate face, so spans x 2
        spans = teeth * 2

        # Create a pipe with the specified number of teeth
        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)

        # Find every other face on pipe
        sideFaces = range(spans*2, spans*3, 2)

        cmds.select(clear=True)

        # Select every other face on pipe
        for face in sideFaces:
            cmds.select('%s.f[%s]' % (self.transform, face), add=True)

        # Extrude the selected faces
        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    def changeTeeth(self, teeth=10, length=0.3):

        """
        This method changes the existing gear in the scene
        Args:
            teeth: The new number of teeth the gear should have
            length: The new length of the teeth

        """

        # Change the number of faces on the polyPipe
        spans = teeth*2

        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        # Create a list to store all our faces
        sideFaces = range(spans*2, spans*3, 2)
        faceNames = []

        for face in sideFaces:
            faceName = 'f[%s]' % (face)
            faceNames.append(faceName)

        # Extrude the correct faces
        cmds.setAttr('%s.inputComponents' % (self.extrude),
                     len(faceNames),
                     *faceNames,
                     type="componentList")

        # Change the length of the teeth
        # ltz is the short form of localTranslateZ
        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)
