import os
import xpstart

class Scenery(xpstart.Base):
    """
    The scenery class holds informations about a x-plane scenery. To create a scenery object
    just the path to the scenery goes to the constructor. 
    """

    def __init__(self,path):
        """
        @type path: string
        @param path: the path to the scenery without ending "/"
        """
        
        xpstart.Base.__init__(self)
        
        #=======================================================================
        # Path to the apt.dat File begining at scenery folder
        #=======================================================================
        self.__pathAptDat = "/Earth nav data/apt.dat"
        
        
        #=======================================================================
        # The file were the data of the scenerie is cached
        # That parameter is overwritten
        # In one file there can be stored more data. The logic for storing is
        # classname:title:dataname:data
        #=======================================================================
        self.cacheFile = "cache_sceneries.txt"
        
        #=======================================================================
        # The path to the scenery
        # If there is a / at the end it will be removed. 
        #=======================================================================
        if path.endswith("/") or path.endswith("\\"):
            path = path[:-1]
        self.path = path
        
        #=======================================================================
        # The title of a scenery is defined by the folder name
        #=======================================================================
        self.title = os.path.basename(self.path)
        
        #=======================================================================
        # The path to the apt.dat file
        # Were the apt.dat file is, when a scenery has one
        #=======================================================================
        self.aptDatPath = "%s/%s" % (self.path,self.__pathAptDat)
        
        
        #=======================================================================
        # Is true, when there is a apt.dat file
        # If apt.dat data is requested that parameter is asked
        #=======================================================================
        self.aptDat = os.path.exists(self.aptDatPath)
        
        #=======================================================================
        # If there is a library.txt file
        #=======================================================================
        self.libraryTxt = os.path.exists("%s/library.txt" % (self.path))
        
        
        #=======================================================================
        # Counts the objects and stores them into that parameter
        # The parameter is a dictionary like the __objTypes
        #=======================================================================
        self.counterObjects = self.countObjects()
        
        
        #=======================================================================
        # Icao codes of the scenery if there is an apt.dat
        # One scenery can have many icao codes. The parameter is type list
        #=======================================================================
        self.icaoCodes = self.searchIcaoCodes()
        
        
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
        for path,dirs,files in os.walk(self.path):
            if os.path.basename(path) in exceptionDirs:
                continue
            if len(files)== 0:
                continue
            for objFile in files:
                fileElements = objFile.split(".")
                if "." in objFile and fileElements[1] in self.objTypes and fileElements[0] not in exceptionFiles:
                    counter[fileElements[1]] = counter[fileElements[1]] + 1
        self.writeCounter(counter)
        return counter
    
    def writeCounter(self,counter):
        data = ""
        for key,val in counter.items():
            data = "%s%s.%s;" % (data,key,val)
        print data    
        self.writeCache("counter", data)
        
    def readCounter(self):
        print "read"
    
    #===========================================================================
    # Searches the icao codes in the apt.dat
    #===========================================================================
    def searchIcaoCodes(self):
        """
        Returns a list with all the ICAO codes find in the apt.dat file of the
        scenery. If there is no apt.dat file the list will be empty []
        """
        # If there is no apt.dat an empty list is returned
        if not self.aptDat:
            return []
        aptDatFile = open(self.aptDatPath)
        icaoCodes = []
        for line in aptDatFile:
            if line.strip().startswith("1 "):
                entries = line.strip().split()
                icaoCode = entries[4]
                icaoCodes.append(icaoCode)
        aptDatFile.close()
        return icaoCodes
    

    