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
        
        
    
    def addDefaultRule(self,cmd):
        """
        Adds one comand to the defaultRules. Every command is in the logik
        "Entity->Rule->Value;"
        """
        c = cmd.split("->")
        if not c[0] in self.defaultRules:
            self.defaultRules[c[0]] = {}
        if not c[1] in self.defaultRules[c[0]]:
            self.defaultRules[c[0]][c[1]] = {}
        self.defaultRules[c[0]][c[1]] = c[2]
        
    def checkEntities(self,entities):
        """
        Checks the entities with the defaultRules
        @param entities: entityName:Value
        @type entities: dict
        @return: If the entities match into the defaultRules True else False
        """
        for entity,rules in self.defaultRules.items():
            if entity not in entities:
                return False
            for rule,val in rules.items():
                if rule == "min" and val < entities[entity]:
                    return False
                elif rule == "max" and val > entities[entity]:
                    return False
                elif rule == "is" and val is not entities[entity]:
                    return False
        return True
                    
            
    
    
    def loadDefaultRules(self):
        """
        Loads the rules
        These are defined over the layer_definitions.txt file. The rules are defined
        with several commands, which are separated with ; inside that file. The rules
        will be added to the DefaultRules
        """
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
        # Dict to store the layers object and other data
        #=======================================================================
        self.layers = {}
        
        #=======================================================================
        # File were all the definitions to the layers are stored 
        #=======================================================================
        self.layerDefFile = "xpstart/layer_definitions.txt"
        
        #=======================================================================
        # All the Layers needs to be loaded
        #=======================================================================
        self.loadLayers()
        
        # The name of the sceneryFolder !Don't change!
        self.sceneryFolder = "Custom Scenery"
        
        #=======================================================================
        # All active sceneries of the XP installation are loaded as scenery
        # objects
        #=======================================================================
        self.sceneries = self.loadXpSceneries()
        
        
        
        
    def loadLayers(self):
        #self.writeData("layers","libraries;ground;texture;", self.layerDefFile)
        layersData = self.readData("layers", self.layerDefFile)
        layersTitles = layersData.split(self.dataDelimiterEntry)
        for title in layersTitles:
            if title == "":
                continue
            self.layers[title] = {}
            self.layers[title]['object'] = Layer(title)
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
                sceneryObj = scenery.Scenery(abspath)
                sceneries.append(sceneryObj)
                print self.makeSceneryEntities(sceneryObj)
        return sceneries
    
    def makeSceneryEntities(self,scenery):
        """
        Makes one dictionary of a scenery object. This dict is used to check
        for layer default rules
        @type scenery: Instance of Scenery Object
        """
        #entities = {}
        entities = scenery.counterObjects
        entities['icaos'] = len(scenery.icaoCodes)
        entities['title'] = scenery.title
        
        if scenery.aptDat:
            entities['aptdat'] = 1
        else:
            entities['aptdat'] = 0
        return entities
    
    def searchDefaultLayer(self):
        return "layertitle"