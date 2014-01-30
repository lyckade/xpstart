import os.path

class Scenerypacks():
    """Reads and writes the scenery_packs.ini file
    """
    
    def __init__(self,xpPath):
        """
        @type xpPath: string
        @param xpPath: Path to the X-Plane root folder
        """
        if xpPath.endswith("/") or xpPath.endswith("\\"):
            xpPath = xpPath[:-1]
        self.xpPath = xpPath #:Path to the X-Plane root folder
        
        self.__sceneryFolder = "Custom Scenery" #: The name of the sceneryFolder !Don't change!
        
        self.__iniFile = "scenery_packs.ini" #: The filename of the ini File !Don't change!
        
        self.pathIniFile = "%s/%s/%s" % (self.xpPath,self.__sceneryFolder,self.__iniFile)
        
        self.__iniHeader = ["I",
                            "1000 version",
                            "SCENERY",
                            ]
        """Header of the ini file. Is used for the output"""
        
        self.__iniCmds = ["SCENERY_PACK",
                          "SCENERY_PACK_DISABLED"]
        """Allowed commands in that ini file"""
        
        self.__defaultCmd = "SCENERY_PACK" #: Default command is used, when no other command is given to thas scenery
        
        
        self.packs = {} 
        """Dictionary for all packs in the ini file. The logic for the dict is:
        key: name of the scenery   
        value: command of the ini file   
        """
        
        self.order = []
        """Simple list with the names of the sceneries. That order will be used for the output."""
        
        if not os.path.exists(self.pathIniFile):
            # Touch the file if it does not exist
            #open(self.pathIniFile,"a").close()
            self.order = self.getInstalledSceneries()
            self.writeIniFile()
        
        
        
    def getInstalledSceneries(self):
        """Reads all titles out of the Custom Scenery folder and returns a list with the titles"""
        sceneryPath = "%s/%s" % (self.xpPath,self.__sceneryFolder)
        sceneries = []
        
        for entry in os.listdir(sceneryPath):
            # Path to the entry
            abspath = "%s/%s" % (sceneryPath,entry)
            # A scenery has to be a directory
            if os.path.isdir(abspath):
                sceneries.append(entry)
        return sceneries
        
    def parseLine(self,line):
        """
        @type line: string
        @param line: one command line of the ini file
        """
        line = line.strip()
        if line in self.__iniHeader:
            return ("","")
        c = line.split(" ")
        cmd = c[0]
        val = " ".join(c[1:])
        return (cmd,val)
    
    def readIniFile(self,path=""):
        if path == "":
            path = self.pathIniFile
        f = open(path,"r")
        for l in f:
            cmd,sceneryTitle = self.parseLine(l)
            if sceneryTitle is not "":
                self.packs[sceneryTitle] = cmd
                if sceneryTitle not in self.order:
                    self.order.append(sceneryTitle)
        f.close()
        
    def writeIniFile(self,path=""):
        if path == "":
            path = self.pathIniFile
        iniFile = open(self.pathIniFile,"w")
        for l in self.__iniHeader:
            iniFile.write("%s\n" % (l))
        for sceneryTitle in self.order:
            cmd = ""
            val = ""
            if sceneryTitle in self.packs:
                cmd = self.packs[sceneryTitle]
                val = sceneryTitle
            else:
                cmd = self.__defaultCmd
                val = sceneryTitle
            iniFile.write("%s %s/%s/\n" % (cmd,self.__sceneryFolder,val))
            
        iniFile.close()