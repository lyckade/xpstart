
class Base():
    """
    The base class contains parameters and function which has to be used by all other
    classes. These are some global definitions
    """
    
    
    def __init__(self,gui=None):
        #=======================================================================
        # Object Types
        # Used for counting the objects
        #=======================================================================
        self.objTypes = [
                           "ags",
                           "dsf",
                           "fac",
                           "for",
                           "lin",
                           "obj",
                           "pol",
                           "str",
                           "ter"]
        
        #=======================================================================
        # A title will be filled in when there is an instance
        # That the cache functions work an empty title is created
        #=======================================================================
        self.title = ""
        
        #=======================================================================
        # Possibility to store a object for the gui to send messages
        #=======================================================================
        self.gui = gui
        
        #=======================================================================
        # The file were the data of the class is cached
        # In one file there can be stored more data. The logic for storing is
        # classname:title:dataname:data
        #=======================================================================
        self.dataFile = "xpstart/cache.ini"
        
        #=======================================================================
        # The delimiters are stored as parameter
        # dataDelimiterKey is to separate key and value from dictionaries
        # dataDelimiterEntry is to separate each entry
        #=======================================================================
        self.dataDelimiterKey = ","
        self.dataDelimiterEntry = ";"
        
        self.logFile = "xpstart/Log.txt"
    
    
    def echo(self,txt):
        """
        Method for sending text message to the user
        """
        if self.gui == None:
            print txt
        else:
            self.gui.echo(txt)
            
        
        
    def getTxtProperty(self,property,path):
        """
        Method to get the value of a property which is defined in a txt file
        """
        f = open(path,"r")
        for l in f:
            c = l.split()
            if c[0].strip() == property:
                f.close()
                return " ".join(c[1:])
        f.close()
        return ""
    
    def log(self,txt):
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lf = open(self.logFile,"a")
        lf.write("%s: %s\n" % (timestamp,txt))
        lf.close()
    
    def makeDict(self,s):
        """
        Makes a dictionary out of a string. The string should be made with the makeString() 
        method. 
        @param s: datastring from the cache
        """
        out = {}
        entries = s.split(self.dataDelimiterEntry)
        for e in entries:
            if e == "":
                continue
            c = e.split(self.dataDelimiterKey)
            out[c[0]] = c[1]
        return out
        
        
    def makeString(self,a):
        """
        Makes a string of a list or dictionary object. 
        The method is used to generate the data which will be written into the cache.
        @param a: dictionary which should be transformed to a string to write it into the cache
        """
        out = ""
        if type(a) is dict:
            for key,val in a.items():
                out = "%s%s%s%s%s" % (out,key,self.dataDelimiterKey,val,self.dataDelimiterEntry)
            return out
        elif type(a) is list:
            return "%s%s" % (self.dataDelimiterEntry.join(a),self.dataDelimiterEntry)
                
    def parseFileLine(self,line):
        """
        Parses a Cache line and returns a tuple 
        (classname,title,dataname,data)    
        @param line: one line of the cache file
        @type line: string 
        """
        c = line.strip().split(":")
        return (c[0],c[1],c[2],c[3])
    
    def readData(self,dataname,dataFile = ""):
        """
        Reads one entry out of the cache. To find the data the dataname is needed.
        @param dataname: the name how to find the data
        @type dataname: string
        """
        if dataFile == "":
            dataFile = self.dataFile
        try:
            cf = open(dataFile,"r")
            for l in cf:
                cclassname, ctitle, cdataname, cdata = self.parseFileLine(l)
                if  cclassname == self.__class__.__name__ and ctitle == self.title and cdataname == dataname:
                    cf.close()
                    return cdata
            cf.close()
            return ""
        except:
            return ""
    
    def writeData(self,dataname,data,dataFile = ""):
        """
        Writes the given data into the cache file
        @param dataname: the name how the data can be found again
        @param data: the data to cache
        @type dataname: string
        @type data: string
        """
        if dataFile == "":
            dataFile = self.dataFile
        oldCache = []
        # Touch the file that there is no error, if there is no file
        open(dataFile,"a").close()
        cf = open(dataFile,"r")
        #dataTuple = (self.__class__.__name__,self.title,dataname,data)
        #datastring = "%s:%s:%s:%s" % (self.__class__.__name__,self.title,dataname,data)
        datastring = ":".join((self.__class__.__name__,self.title,dataname,data))
        append = True
        for l in cf:
            cclassname, ctitle, cdataname, cdata = self.parseFileLine(l)
            if  cclassname == self.__class__.__name__ and ctitle == self.title and cdataname == dataname:
                l = datastring
                append = False
            oldCache.append(l)
        if append:
            oldCache.append(datastring)
        cf.close()
        cf = open(dataFile,"w")
        for l in oldCache:
            if len(l)>5:
                cf.write("%s\n" % (l.strip()))
        cf.close()
