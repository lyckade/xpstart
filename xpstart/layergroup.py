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
        
        self.sceneryFolder = "Custom Scenery"
        
        self.sceneries = self.loadXpSceneries()
        
        
    
    def loadXpSceneries(self):
        """
        Loads all sceneries and returns a list of scenery objects
        """
        sceneryPath = "%s/%s" % (self.xpPath,self.sceneryFolder)
        sceneries = []
        print os.listdir(sceneryPath)
        
        return sceneries