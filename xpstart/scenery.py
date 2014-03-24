import os
import xpstart

class Scenery(xpstart.Base):
    """
    The scenery class holds informations about a x-plane scenery. To create a scenery object
    just the path to the scenery goes to the constructor. 
    """

    def __init__(self,path,gui=None):
        """
        @type path: string
        @param path: the path to the scenery without ending "/"
        """
        
        xpstart.Base.__init__(self,gui)
        

        self.__pathAptDat = "/Earth nav data/apt.dat"
        """Path to the apt.dat File begining at scenery folder"""
        
        
        self.dataFile = "xpstart/cache_sceneries.txt"
        """The file were the data of the scenerie is cached
        That parameter is overwritten
        In one file there can be stored more data. The logic for storing is
        classname:title:dataname:data"""
        
        #=======================================================================
        # The path to the scenery
        # If there is a / at the end it will be removed. 
        #=======================================================================
        if path.endswith("/") or path.endswith("\\"):
            path = path[:-1]
        self.path = path
        

        self.title = os.path.basename(self.path)
        """The title of a scenery is defined by the folder name"""

        self.aptDatPath = "%s/%s" % (self.path,self.__pathAptDat)
        """The path to the apt.dat file
        Were the apt.dat file is, when a scenery has one"""
        
        self.aptDat = os.path.exists(self.aptDatPath)
        """Is true, when there is a apt.dat file
        If apt.dat data is requested that parameter is asked"""
        

        self.libraryTxt = os.path.exists("%s/library.txt" % (self.path))
        """ If there is a library.txt file"""

        self.sceneryTxtFile = "scenery.txt"
        """The scenery.txt is a place where information about layergroup can
        be defined. This gives the developer the possibility to define when
        his scenery should be loaded by the system.
        """
        self.pathSceneryTxt = "%s/%s" % (self.path,self.sceneryTxtFile)
        self.sceneryTxt = os.path.exists(self.pathSceneryTxt)

        if self.sceneryTxt:
            self.authLayergroup = self.getTxtProperty("LAYERGROUP", self.pathSceneryTxt)
        else:
            self.authLayergroup = ""
        
        self.counterObjects = self.getObjectCount()
        """Counts the objects and stores them into that parameter
        The parameter is a dictionary like the __objTypes"""
        

        self.icaoCodes = self.searchIcaoCodes()
        """Icao codes of the scenery if there is an apt.dat
        One scenery can have many icao codes. The parameter is type list
        """
        
        
    def countObjects(self):
        """
        Counts all objects of the scenery and returns a dictionary with all
        the defined object types an the number how often they occur.
        """
        
        counter = {}
        exceptionDirs = ["opensceneryx"]
        exceptionFiles = ["placeholder"]
        
        for objType in self.objTypes:
            counter[objType] = 0
        # sum is for the sum() of all objects
        counter['sum'] = 0
        self.echo("Analysing objects from %s" % (self.title))
        for path,dirs,files in os.walk(self.path):
            if os.path.basename(path) in exceptionDirs:
                continue
            if len(files)== 0:
                continue
            for objFile in files:
                fileElements = objFile.split(".")
                if "." in objFile and fileElements[1] in self.objTypes and fileElements[0] not in exceptionFiles:
                    counter[fileElements[1]] = counter[fileElements[1]] + 1
                    counter['sum'] = counter['sum'] + 1
        return counter
    

    def getObjectCount(self):
        """
        Method to get the object count. For performance the cache is been used.
        If there is no entry in the file the count method is used and an entry
        is written into the file.
        """
        cacheStr = self.readData("counter")
        if cacheStr is not "":
            self.echo("Loading Data for %s from cache" % (self.title))
            self.log("Object count for %s" % (self.title))
            return self.makeDict(cacheStr)
        else:
            counter = self.countObjects()
            self.writeData("counter", self.makeString(counter))
            return counter
        
    def loadSceneryTxt(self):
        """Loads the scenery.txt file and sets the intern variables"""
        if self.sceneryTxt:
            f = open(self.pathSceneryTxt,"r")
            for l in f:
                if l.startswith("LAYERGROUP"):
                    print "H"
            f.close()
        
    def searchIcaoCodes(self):
        """
        Returns a list with all the ICAO codes find in the apt.dat file of the
        scenery. If there is no apt.dat file the list will be empty []
        """
        # If there is no apt.dat an empty list is returned
        if not self.aptDat:
            return []
        cacheStr = self.readData("icao")
        if cacheStr is not "":
            return cacheStr.split(self.dataDelimiterEntry)[:-1]
        aptDatFile = open(self.aptDatPath)
        icaoCodes = []
        for line in aptDatFile:
            if line.strip().startswith("1 "):
                entries = line.strip().split()
                icaoCode = entries[4]
                icaoCodes.append(icaoCode)
        aptDatFile.close()
        self.writeData("icao", self.makeString(icaoCodes))
        return icaoCodes
    

    