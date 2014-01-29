

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
        
        self.__iniHeader = ["I",
                            "1000 version",
                            "SCENERY",
                            ""]
        """Header of the ini file. Is used for the output"""
        
        self.__iniCmds = ["SCENERY_PACK",
                          "SCENERY_PACK_DISABLED"]
        """Allowed commands in that ini file"""
    