import Tkinter as tk
import tkFont        
import ttk
from thread import start_new_thread

class XpstartView(tk.Frame):
    
    def __init__(self,parent,xppath):
        
        tk.Frame.__init__(self, parent)
        
        self.END = tk.END
        
        self.fontStyle = tkFont.Font(family="Helvetica", size=9)
        gridrowActions = 0
        self.actionsStep = 0
        self.actionsArea = tk.Frame(parent,borderwidth=1)
        self.actionsArea.pack(padx=10,pady=10)
        self.actionButton = tk.Button(
                    self.actionsArea,
                    text="Initialize Szeneries",
                    font=self.fontStyle,
                    command=self.clickActions,
                    )
        self.actionButton.grid(row=gridrowActions,column=0)
        gridrowLayers = 0
        self.layersArea = tk.Frame(parent,borderwidth=1)
        self.layersArea.pack(padx=10,pady=10)
        self.layersLabel = tk.Label(self.layersArea,text="Layers: ")
        self.layersLabel.grid(row=gridrowLayers,column=0)  
        
        gridrowLayers = gridrowLayers + 1
        self.layersScroll = tk.Scrollbar(self.layersArea, orient=tk.VERTICAL)
        self.layersScroll.grid(row=gridrowLayers,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
              
        self.layersBox = tk.Listbox(
                                    self.layersArea,
                                    yscrollcommand=self.layersScroll.set,
                                    height=10,
                                    width=15,
                                    font=self.fontStyle)
        self.layersBox.grid(row=gridrowLayers,column=0)
        
        self.layersBox.bind("<ButtonRelease-1>", self.setActiveLayer)
        
        #self.sceneriesArea = tk.Frame(parent,borderwidth=1)
        #self.sceneriesArea.pack(side=tk.LEFT,fill=tk.X,padx=10,pady=10)
        
        gridrowRight = 0

        self.sceneriesLabel = tk.Label(self.layersArea,text="Sceneries: ")
        self.sceneriesLabel.grid(row=gridrowRight,column=2)
        
        gridrowRight = gridrowRight + 1
        self.sceneriesyScroll = tk.Scrollbar(self.layersArea, orient=tk.VERTICAL)
        self.sceneriesyScroll.grid(row=gridrowRight,column=3,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.sceneriesBox = tk.Listbox(
                                    self.layersArea,
                                    yscrollcommand=self.sceneriesyScroll.set,
                                    height=10,
                                    width=50,
                                    font=self.fontStyle,
                                    )
        self.sceneriesBox.grid(row=gridrowRight,column=2)
        #self.sceneriesBox.pack(side=tk.LEFT)
        self.sceneriesyScroll.config(command = self.sceneriesBox.yview)
        
        self.sceneriesBox.bind("<ButtonRelease-1>", self.setActiveScenery)
        
        gridrowRight = gridrowRight + 1
        self.sceneriesDetailsNameLabel = tk.Label(self.layersArea,text="Scenery Name: ")
        self.sceneriesDetailsNameLabel.grid(row=gridrowRight,column=2)
        gridrowRight = gridrowRight + 1
        self.sceneriesDetailsName = tk.Text(
                                    self.layersArea,
                                    width=50,
                                    height=1,
                                    #state=tk.DISABLED,
                                    font=self.fontStyle,
                                            )
        
        self.sceneriesDetailsName.grid(row=gridrowRight,column=2)
        gridrowRight = gridrowRight + 1
        self.sceneriesDetailsUserlayerLabel = tk.Label(self.layersArea,text="Change Layer to: ")
        self.sceneriesDetailsUserlayerLabel.grid(row=gridrowRight,column=2)
        gridrowRight = gridrowRight + 1
        self.sceneriesDetailsUserlayer = ttk.Combobox(
                                    self.layersArea,
                                    state=tk.DISABLED,
                                    width=47,
                                    font=self.fontStyle)
        self.sceneriesDetailsUserlayer.bind('<<ComboboxSelected>>',self.setUserLayer)
        self.sceneriesDetailsUserlayer.grid(row=gridrowRight,column=2)
        gridrowInfo = 1
        self.infoArea = tk.Frame(parent,borderwidth=1)
        self.infoArea.pack()
        self.messageScroll = tk.Scrollbar(self.infoArea, orient=tk.VERTICAL)
        self.messageScroll.grid(row=gridrowInfo,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
        self.messageBox = tk.Text(
                                  self.infoArea,
                                  yscrollcommand=self.messageScroll.set,
                                  width=65,
                                  height=6,
                                  font=self.fontStyle,
                                  )
        self.messageBox.grid(row=gridrowInfo,column=0)
        self.messageScroll.config(command = self.messageBox.yview)      
        #self.messageBox.insert(tk.END, "Test")
        
        #------------------------------------------------ loading the controller
        self.controller = XpstartController(xppath,self)
        
        #----------------------------------------------- actions after the layer
        #self.loadLayers()
        #self.loadSceneries()  

        
    def echo(self,txt):
        self.messageBox.insert(self.END, "%s\n" % (txt))
        self.messageBox.see(self.END)
        
    def clickActions(self):
        
        if self.actionsStep == 0:
            self.actionButton.config(
                    text="Loading sceneries! Can take some time.",
                    state=tk.DISABLED,
                    )
            self.actionsStep = 1
            start_new_thread(self.clickActions,())
        elif self.actionsStep == 1:
            self.controller.initialize()
            self.actionButton.config(
                    text="Load sceneries",
                    state=tk.ACTIVE,
                    )
            self.actionsStep = 2
        elif self.actionsStep == 2:
            self.loadLayers()
            self.loadSceneries()
            self.doubleIcaos = self.controller.lg.checkIcaos()
            self.actionButton.config(text="Write scenery_packs.ini")
            self.actionsStep = 4
        elif self.actionsStep == 3:
            self.controller.initialize()
            self.loadLayers()
            self.loadSceneries()
            self.actionButton.config(text="Write scenery_packs.ini")
            self.actionsStep = 4
        elif self.actionsStep == 4:
            self.echo("Writing scenery_packs.ini")
            self.controller.writeSceneryPacksIni()
            self.echo("Ready")
            if len(self.doubleIcaos) == 0:
                #self.actionButton.config(state=tk.DISABLED)
                self.actionButton.config(text="Close xpstart")
                self.actionsStep = 6
            else:
                self.actionButton.config(text="Warnings: Open Report")
                self.actionsStep = 5
        elif self.actionsStep == 5:
            import webbrowser
            import os.path
            xps_root = os.path.abspath("")
            self.controller.makeReport(self.controller.lg.checkIcaos())
            report = os.path.join(xps_root,"xpstart","warnings.htm")
            
            webbrowser.open_new_tab(report)
            self.echo("Report generated")
            self.actionButton.config(text="Close xpstart")
            self.actionsStep = 6
            print self.controller.lg.checkIcaos()
        elif self.actionsStep == 6:
            exit()
             
        
    def loadLayers(self):
        self.layersBox.delete(0,tk.END)
        layers = self.controller.getLayers()
        self.sceneriesDetailsUserlayer['values'] = layers
        for lname in layers:
            self.layersBox.insert(tk.END,lname)
            self.echo("Loading Layer %s" % (lname))
            
    def loadSceneries(self):
        self.sceneriesBox.delete(0, tk.END)
        self.sceneries = self.controller.getSceneries()
        for s in self.sceneries:
            self.sceneriesBox.insert(tk.END,s)
            
    def setActiveLayer(self,data):
        self.controller.activeLayer = self.controller.lg.order[int(self.layersBox.curselection()[0])]
        #print self.controller.activeLayer
        #print self.controller.lg.order[int(self.layersBox.curselection()[0])]
        self.loadSceneries()
        #print self.layersBox.curselection()
        #print data
        
    def setActiveScenery(self,data):
        
        self.sceneries = self.controller.getSceneries()
        sceneryTitle = self.sceneries[int(self.sceneriesBox.curselection()[0])]
        self.sceneriesDetailsName.delete(0.0,tk.END)
        self.sceneriesDetailsName.insert(tk.END,sceneryTitle)
        self.sceneriesDetailsUserlayer.config(state=tk.ACTIVE)
        self.controller.setActiveScenery(sceneryTitle)
        self.sceneriesDetailsUserlayer.set(self.controller.activeScenery.getUserLayer())
        self.controller.activeScenery.getSceneyPackIniStatus()
    
    
    def setUserLayer(self,data):
        userLayer = self.sceneriesDetailsUserlayer.get()
        self.controller.activeScenery.writeUserLayer(userLayer)
        self.actionsStep = 3
        self.actionButton.config(text="Reload sceneries")
        

import layergroup
import xpstart  
      
class XpstartController:
    
    def __init__(self,xppath,gui):
        
        self.gui = gui

        self.activeLayer = ''
        self.xppath = xppath
        self.warningsFile = "xpstart/warnings.htm"
        
    def initialize(self):
        import scenerypacks
        self.lg = layergroup.Layergroup(self.xppath,self.gui)
        self.sceneries = self.getAllSceneries()
        self.scenerypacks = scenerypacks.Scenerypacks(self.xppath)
        
    
    def getActiveLayer(self):
        if self.activeLayer == '' or self.activeLayer not in self.lg.order:
            return self.lg.order[0]
        else:
            return self.activeLayer
    
    def getLayers(self):
        return self.lg.order
    
    def getAllSceneries(self):
        sceneries = []
        for lname in self.lg.order:
            l = self.lg.layers[lname]
            if len(l['sceneries'])== 0:
                continue
            for s in sorted(l['sceneries']):
                sceneries.append(s)
        return sceneries
        
    def getSceneries(self):
        l = self.lg.layers[self.getActiveLayer()]
        sceneries = []
        for s in sorted(l['sceneries']):
            sceneries.append(s)
        return sceneries
    
    def makeReport(self,doubleIcaos):
        f = open(self.warningsFile,"w")
        f.write("""<html><head><title>xpstart Report</title>
        </head><link rel='stylesheet' type='text/css' href='style.css' /><body>\n""")
        f.write("<h1>Not unique airport definitions</h1>\n")
        f.write("""
            <p>That report analyses the icao codes. The icao code is a
            identifier for each airport. If there is more than one scenery for one 
            airport, that could cause problems. Here the user should decide to remove or 
            disable one scenery.</p>
            <p>The icao codes in that report are linked to the apxp.info site. There you 
            can get more infos about that airport.
            </p>
            """)
        
        for icao in sorted(doubleIcaos):
            sceneries = doubleIcaos[icao]
            f.write("<p>Airport: <b><a href='http://apxp.info/airports/view/%s'>%s</a></b><br />" % (icao,icao))
            f.write("<ul>")
            for scenery in sceneries:
                cssClassDef = ""
                disabledTxt = ""
                if self.scenerypacks.packs[scenery["title"]] == "SCENERY_PACK_DISABLED":
                    cssClassDef = " class='disabled' "
                    disabledTxt = "<b>Scenery disabled:</b> "
                f.write("<li%s>%s%s (%s)</li>" % (cssClassDef,disabledTxt,scenery["title"],scenery["layer"]))
            f.write("</ul>")
            f.write("</p>")
                
        f.write("</body></html>")
    
    def setActiveScenery(self,sceneryTitle):
        import scenery
        path = "%s/Custom Scenery/%s" % (self.xppath,sceneryTitle)
        self.activeScenery = scenery.Scenery(path,self.gui)

    
    def writeSceneryPacksIni(self):
        self.scenerypacks.order = self.getAllSceneries()
        self.scenerypacks.writeIniFile()
        

        