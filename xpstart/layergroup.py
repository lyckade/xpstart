import scenery
import xpstart
import os

class Layer(xpstart.Base):
    """
    The model for a scenery layer
    """
    
    def __init__(self,title):
        xpstart.Base.__init__(self)
        
        self.title = title
        #=======================================================================
        # Description will displayed in the gui to help the user
        #=======================================================================
        self.description = ""
        
        self.dataFile = "xpstart/layer_definitions.txt"
        #self.writeData("dataname", "Test")
        #=======================================================================
        # The logik for defaultRules is to store them in a dictionary
        # Entity -> Rule -> Value
        # defaultRules['obj']['min'] = 1
        #=======================================================================
        self.defaultRules = {}
        
        self.loadDefaultRules()
        print self.defaultRules
        
        #self.__ruleCommands = {}
        
    
    def addDefaultRule(self,cmd):
        c = cmd.split("->")
        if not c[0] in self.defaultRules:
            self.defaultRules[c[0]] = {}
        if not c[1] in self.defaultRules[c[0]]:
            self.defaultRules[c[0]][c[1]] = {}
        self.defaultRules[c[0]][c[1]] = c[2]
    
    def loadDefaultRules(self):
        data = self.readData("defaultRules")
        if data is not "":
            cmds = data.split(self.dataDelimiterEntry)
            for cmd in cmds:
                if cmd is not "":
                    self.addDefaultRule(cmd)
        
    
    

class Layergroup(xpstart.Base):
    """
    All sceneries of an x-plane installation can be grouped into layers.
    That helps to sort the sceneries.
    """
    
    def __init__(self,xpPath):
        xpstart.Base.__init__(self)
        if xpPath.endswith("/") or xpPath.endswith("\\"):
            xpPath = xpPath[:-1]
        self.xpPath = xpPath
        
        #=======================================================================
        # Title is important for the read and write methods and specify the
        # instance. If not changed it will be the Default instance
        #=======================================================================
        self.title = "Default"
        
        #=======================================================================
        # List to store the layers inside
        # Every entry will be a Layer object
        #=======================================================================
        self.layers = []
        
        #=======================================================================
        # File were all the definitions to the layers are stored 
        #=======================================================================
        self.layerDefFile = "xpstart/layer_definitions.txt"
        
        # The name of the sceneryFolder !Don't change!
        self.sceneryFolder = "Custom Scenery"
        # All sceneries as an object
        self.sceneries = self.loadXpSceneries()
        
        self.loadLayers()
        
        
    def loadLayers(self):
        #self.writeData("layers","libraries;ground;texture;", self.layerDefFile)
        layersData = self.readData("layers", self.layerDefFile)
        layersTitles = layersData.split(self.dataDelimiterEntry)
        for title in layersTitles:
            if title == "":
                continue
            self.layers.append(Layer(title))
        print layersTitles[:-1]
        
        
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