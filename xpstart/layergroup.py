import os

import scenery
import xpstart


class Layer(xpstart.Base):
    """
    The model for a scenery layer
    """

    def __init__(self, title, gui=None):
        xpstart.Base.__init__(self, gui)

        self.gui = gui

        self.title = title
        # =======================================================================
        # Description will displayed in the gui to help the user
        # =======================================================================
        self.description = ""

        self.dataFile = "xpstart/layer_definitions.txt"
        # self.writeData("dataname", "Test")
        # =======================================================================
        # The logik for defaultRules is to store them in a dictionary
        # Entity -> Rule -> Value
        # defaultRules['obj']['min'] = 1
        #=======================================================================
        self.defaultRules = {}

        self.loadDefaultRules()

    def addDefaultRule(self, cmd):
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

    def checkEntities(self, entities):
        """
        Checks the entities with the defaultRules
        @param entities: entityName:Value
        @type entities: dict
        @return: If the entities match into the defaultRules True else False
        """
        if len(self.defaultRules) == 0:
            return False
        for entity, rules in self.defaultRules.items():
            if entity not in entities:
                return False
            for rule, val in rules.items():
                if rule == "min" and int(val) > int(entities[entity]):
                    return False
                elif rule == "max" and int(val) < int(entities[entity]):
                    return False
                elif rule == "is" and str(val) != str(entities[entity]):
                    return False
                elif rule == "not" and str(val) == str(entities[entity]):
                    return False
                elif rule == "in" or "not_in":
                    if "|" in str(val):
                        l = str(val).split("|")
                    else:
                        l = [str(val)]
                    if rule == "in" and str(entities[entity]) not in l:
                        return False
                    elif rule == "not_in" and str(entities[entity]) in l:
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

    def __init__(self, xpPath, gui=None):
        xpstart.Base.__init__(self, gui)
        self.gui = gui
        if xpPath.endswith("/") or xpPath.endswith("\\"):
            xpPath = xpPath[:-1]
        self.xpPath = xpPath

        self.title = "Default"
        """
        Title is important for the read and write methods and specify the
        instance. If not changed it will be the Default instance
        """

        self.defaultLayer = "new add-ons"

        self.layers = {}
        """
        Dict to store the layers object and other data
        The object is always found at self.layers[title]['object']
        """

        self.order = []
        """
        List to get the Layers in the right order
        """

        self.layerDefFile = "xpstart/layer_definitions.txt"
        """File were all the definitions to the layers are stored """

        self.sceneryFolder = "Custom Scenery"  # : The name of the sceneryFolder !Don't change!

        self.defaultSceneryLayer = self.readData("defaultSceneryLayer", self.layerDefFile)[:-1]
        """The layer which contains the default scenery"""

        self.loadLayers()
        """All the Layers needs to be loaded"""

        self.sceneries = self.loadXpSceneries()
        """All active sceneries of the XP installation are loaded as scenery objects"""


    def checkIcaos(self):
        """
        Walks over all layers and returns a dict with the layername icao an scenerynames
        """
        warnings = {}  # : Dictionary where all the warnings are collected
        icaos = {}
        for layer in self.order:
            # for layer in self.layers:
            if layer not in self.layers:
                continue
            for icao in self.layers[layer]['icaos']:
                if icao not in icaos:
                    icaos[icao] = []
                for sc in self.layers[layer]['icaos'][icao]:
                    icaos[icao].append({"title": sc, "layer": layer})
                    # icaos[icao] = icaos[icao] + self.layers[layer]['icaos'][icao]
        for icao in icaos:
            if len(icaos[icao]) > 1:
                warnings[icao] = icaos[icao]
        return warnings

        # for layer in self.layers:

    #
    # for icao in self.layers[layer]['icaos']:
    # if len(self.layers[layer]['icaos'][icao])>1:
    # if layer not in warnings:
    # warnings[layer] = {}
    #                    warnings[layer][icao] = self.layers[layer]['icaos'][icao]
    #        return warnings

    def loadLayers(self):
        """Loads the defined layers out of the dataFile and adds an Layer object
        to the self.layers list. 
        """
        #self.writeData("layers","libraries;ground;texture;", self.layerDefFile)
        layersData = self.readData("layers", self.layerDefFile)
        layersTitles = layersData.split(self.dataDelimiterEntry)
        self.order = []
        for title in layersTitles:
            if title == "":
                continue
            self.order.append(title)
            self.layers[title] = {}
            self.layers[title]['object'] = Layer(title, self.gui)
            # Make instance here for easy append later
            self.layers[title]['sceneries'] = []
            self.layers[title]['icaos'] = {}


    def loadXpSceneries(self):
        """
        Loads all sceneries and orders it in the self.layers[title]['sceneries'] dict
        """
        sceneryPath = "%s/%s" % (self.xpPath, self.sceneryFolder)
        sceneries = {}

        for entry in os.listdir(sceneryPath):
            # Path to the entry
            abspath = "%s/%s" % (sceneryPath, entry)
            # A scenery has to be a directory
            if os.path.isdir(abspath):
                sceneryObj = scenery.Scenery(abspath, self.gui)
                sceneries[sceneryObj.title] = sceneryObj
                # First the userLayer than authLayergoup than default
                if sceneryObj.userLayer in self.layers:
                    layerTitle = sceneryObj.userLayer
                elif sceneryObj.authLayergroup in self.layers:
                    layerTitle = sceneryObj.authLayergroup
                else:
                    layerTitle = self.searchDefaultLayer(sceneryObj)
                if layerTitle in self.layers:
                    # Add scenerie to layer
                    self.layers[layerTitle]['sceneries'].append(sceneryObj.title)
                    # Icao Codes for a layer are collected
                    # All is put into a dictionary
                    if len(sceneryObj.icaoCodes) > 0:
                        for icao in sceneryObj.icaoCodes:
                            if icao == "":
                                continue
                            # First time a list for every icao has to be defined
                            if icao not in self.layers[layerTitle]['icaos']:
                                self.layers[layerTitle]['icaos'][icao] = []
                            else:
                                # Give out a warning!
                                self.log(
                                    "Warning: %s in scenery %s is not the first apearance of that icao in that layer!" % (
                                        icao, sceneryObj.title))
                            self.layers[layerTitle]['icaos'][icao].append(sceneryObj.title)
                            # self.layers[layerTitle]['icaos'].append(sceneryObj.icaoCodes)
        return sceneries

    def makeSceneryEntities(self, scenery):
        """
        This method is called by loadDefaultRules. On this way additional entities
        can be added to the default layer definition.
        Makes one dictionary of a scenery object. This dict is used to check
        for layer default rules. If a new entity is needed at the default layer 
        definition it can added here.
        
        @type scenery: Instance of Scenery Object
        """
        #entities = {}
        counterObjects = scenery.getObjectCount()
        entities = counterObjects
        # polter is the sum of pol and ter it is needed to indentify photo sceneries
        entities['polter'] = counterObjects['pol'] + counterObjects['ter']
        entities['icaos'] = len(scenery.icaoCodes)
        entities['title'] = scenery.title
        if scenery.libraryTxt:
            entities['library'] = 1
        else:
            entities['library'] = 0

        if scenery.aptDat:
            entities['aptdat'] = 1
        else:
            entities['aptdat'] = 0
        return entities

    def searchDefaultLayer(self, sceneryObj):
        """
        Walks through the layers and make a check, if it is the defaultLayer to 
        the scenery object.
        Returns the title of the default layer
        """
        if len(self.layers) == 0:
            self.loadLayers()
        # If there is a entry in the default DB this is returned
        if sceneryObj.defaultDBLayer is not "" and sceneryObj.defaultDBLayer in self.layers:
            return sceneryObj.defaultDBLayer
        entities = self.makeSceneryEntities(sceneryObj)
        checkOrder = self.readData("checkOrder", self.layerDefFile)[:-1].split(";")
        defLayerTitle = self.defaultLayer
        for orderNr in checkOrder:
            layerTitle = self.order[int(orderNr)]
            if self.layers[layerTitle]['object'].checkEntities(entities):
                return layerTitle
        return defLayerTitle