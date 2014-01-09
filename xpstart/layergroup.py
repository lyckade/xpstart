import scenery
import os

class Layergroup():
    """
    All sceneries of an x-plane installation can be grouped into layers.
    That helps to sort the sceneries.
    """
    
    def __init__(self,xpPath):
        
        if xpPath.endswith("/") or xpPath.endswith("\\"):
            xpPath = xpPath[:-1]
        self.xpPath = xpPath
        # The name of the sceneryFolder !Don't change!
        self.sceneryFolder = "Custom Scenery"
        # All sceneries as an object
        self.sceneries = self.loadXpSceneries()
        
        
    
    def loadXpSceneries(self):
        """
        Loads all sceneries and returns a list of scenery objects
        """
        sceneryPath = "%s/%s" % (self.xpPath,self.sceneryFolder)
        sceneries = []
        
        for entry in os.listdir(sceneryPath):
            # Path to the entry
            abspath = "%s/%s" % (sceneryPath,entry)
            # A scenery has to be a directory
            if os.path.isdir(abspath):
                sceneries.append(scenery.Scenery(abspath))
        return sceneries