from maya import cmds
import os
import json

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, 'controllerLibrary')


def createDirectory(directory=DIRECTORY):
    """
    Creates the given directory if it doesn't already exist
    Args:
        directory (str): The directory to create
    """
    if not os.path.exists(directory):
        os.mkdir(directory)


class ControllerLibrary(dict):

    def save(self, name, directory=DIRECTORY, screenshot=True,**info):
        """
        This saves a controller with the given name and takes a screenshot of the controller.
        It saves this to a dictionary located within a json file
        Args:
            name: The name of the item we want to save
            directory: The directory to save to
            screenshot: The screenshot of the item we want to save
            **info: Any Additional info we want to save to the json file

        """

        # Make sure the directory is created
        createDirectory(directory)

        # join the files name with the .ma file type to create correct file path
        path = os.path.join(directory, '%s.ma' % name)
        infoFile = os.path.join(directory, '%s.json' % name)

        # Information to write to JSON file
        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        # If there is an item selected, then only save that item
        # Else, just save the whole scene
        if cmds.ls(selection=True):
            cmds.file(force=True, type='mayaAscii', exportSelected=True)
        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        if screenshot:
            info['screenshot'] = self.saveScreenShot(name, directory=directory)

        # Write **info to the opened json file
        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        # Updates after save
        self[name] = info

    def find(self, directory=DIRECTORY):
        """
        Finds controllers on disk
        Args:
            directory: The directory to search in

        """
        self.clear()
        if not os.path.exists(directory):
            return

        # make a list of all the files in the directory
        files = os.listdir(directory)

        # Filter out all the non-Maya files
        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, extension = os.path.splitext(ma)
            # Reconstruct the full path name
            path = os.path.join(directory, ma)

            infoFile = '%s.json' % name
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                # read info from the json file
                # f represents the file stream we just opened
                with open(infoFile, 'r') as f:
                    info = json.load(f)
            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, name)

            # Load values into json file
            info['name'] = name
            info['path'] = path

            self[name] = info


    def load(self, name):
        """
        This loads in a controller with the given name
        Args:
            name: The name of the controller we want to find

        """
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def saveScreenShot(self, name, directory=DIRECTORY):
        """
        This saves a screenshot of the controller we are saving
        Args:
            name: The name of the controller
            directory: The directory we are saving the picture to

        """
        path = os.path.join(directory, '%s.jpg' % name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

        return path
