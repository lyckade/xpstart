import os

class Scenery():
    """
    The scenery class holds informations about a x-plane scenery. To create a scenery object
    just the path to the scenery goes to the constructor. 
    """
    #===========================================================================
    # 
    # @type path: string
    # @param path: the path to the scenery without ending "/"
    #===========================================================================
    def __init__(self,path):
        # Path to the apt.dat File begining at scenery folder
        self.__pathAptDat = "/Earth nav data/apt.dat"
        # Object Types
        self.__objTypes = ["fac","for","lin","obj","pol"]
        
        # The path to the scenery
        if path.endswith("/") or path.endswith("\\"):
            path = path[:-1]
        self.path = path
        # The path to the apt.dat file
        self.aptDatPath = "%s/%s" % (self.path,self.__pathAptDat)
        # If there is an apt.dat file
        self.aptDat = os.path.exists(self.aptDatPath)
        # How many objects are inside the scenery
        self.counterObjects = self.countObjects()
        # Icao codes of the scenery (if there is an apt.dat)
        self.icaoCodes = self.searchIcaoCodes()
        
        
 
    
    
    #===========================================================================
    # Searches the scenery for objects
    #===========================================================================
    def countObjects(self):
        """
        Counts all objects of the scenery and returns a dictionary with all
        the defined object types.
        """
        counter = {}
        exceptionDirs = ["opensceneryx"]
        exceptionFiles = ["placeholder"]
        for objType in self.__objTypes:
            counter[objType] = 0
        for path,dirs,files in os.walk(self.path):
            if os.path.basename(path) in exceptionDirs:
                continue
            if len(files)== 0:
                continue
            for objFile in files:
                fileElements = objFile.split(".")
                if fileElements[1] in self.__objTypes and fileElements[0] not in exceptionFiles:
                    counter[fileElements[1]] = counter[fileElements[1]] + 1
        return counter
    
    #===========================================================================
    # Searches the icao codes in the apt.dat
    #===========================================================================
    def searchIcaoCodes(self):
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
    