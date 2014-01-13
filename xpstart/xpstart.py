
class Base():
    """
    The base class contains parameters and function which has to be used by all other
    classes. These are some global definitions
    """
    
    def __init__(self):
        #=======================================================================
        # Object Types
        # Used for counting the objects
        #=======================================================================
        self.objTypes = [
                           "ags",
                           "fac",
                           "for",
                           "lin",
                           "obj",
                           "pol",
                           "str"]
        
        #=======================================================================
        # A title will be filled in when there is an instance
        # That the cache functions work an empty title is created
        #=======================================================================
        self.title = ""
        
        #=======================================================================
        # The file were the data of the class is cached
        # In one file there can be stored more data. The logic for storing is
        # classname:title:dataname:data
        #=======================================================================
        self.cacheFile = "data/cache.ini"
    
        
    def parseCacheLine(self,line):
        """
        Parses a Cache line and returns a tuple 
        (classname,title,dataname,data)
        @param line: one line of the cache file
        @type line: string 
        """
        c = line.strip().split(":")
        return (c[0],c[1],c[2],c[3])
    
    def readCache(self,dataname):
        """
        """
        cf = open(self.cacheFile,"r")
        for l in cf:
            cclassname, ctitle, cdataname, cdata = self.parseCacheLine(l)
            if  cclassname == self.__class__.__name__ and ctitle == self.title and cdataname == dataname:
                cf.close()
                return cdata
        cf.close()
        return ""
    
    def writeCache(self,dataname,data):
        """
        Writes the given data into the cache file
        @param dataname: the name how the data can be found again
        @param data: the data to cache
        @type dataname: string
        @type data: string
        """
        oldCache = []
        cf = open(self.cacheFile,"r")
        datastring = "%s:%s:%s:%s" % (self.__class__.__name__,self.title,dataname,data)
        append = True
        for l in cf:
            cclassname, ctitle, cdataname, cdata = self.parseCacheLine(l)
            if  cclassname == self.__class__.__name__ and ctitle == self.title and cdataname == dataname:
                l = datastring
                append = False
            oldCache.append(l)
        if append:
            oldCache.append(datastring)
        cf.close()
        cf = open(self.cacheFile,"w")
        for l in oldCache:
            if len(l)>5:
                cf.write("%s\n" % (l.strip()))
        cf.close()