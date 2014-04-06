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
        self.sceneriesDetailsName = tk.Text(
                                    self.layersArea,
                                    width=50,
                                    height=1,
                                    #state=tk.DISABLED,
                                    font=self.fontStyle,
                                            )
        gridrowRight = gridrowRight + 1
        self.sceneriesDetailsName.grid(row=gridrowRight,column=2)
        
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
            
            self.actionButton.config(text="Loading sceneries! Can take some time.")

            self.actionsStep = 1

            start_new_thread(self.clickActions,())
        elif self.actionsStep == 1:

            self.controller.initialize()
            self.actionButton.config(text="Load sceneries")
            self.actionsStep = 2
        elif self.actionsStep == 2:

            self.loadLayers()
            self.loadSceneries()

            self.actionButton.config(text="Write scenery_packs.ini")
             
        
    def loadLayers(self):
        layers = self.controller.getLayers()
        for lname in layers:
            self.layersBox.insert(tk.END,lname)
            
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
        print self.sceneriesBox.curselection()[0]
        #self.controller.activeLayer = self.controller.lg.order[int(self.layersBox.curselection()[0])]
        self.sceneries = self.controller.getSceneries()
        print self.sceneries[int(self.sceneriesBox.curselection()[0])]
        #self.sceneriesDetailsName.insert(tk.END," ")
        self.sceneriesDetailsName.delete(0.0,tk.END)
        self.sceneriesDetailsName.insert(tk.END,self.sceneries[int(self.sceneriesBox.curselection()[0])])

import layergroup
import xpstart  
      
class XpstartController:
    
    def __init__(self,xppath,gui):
        
        self.gui = gui

        self.activeLayer = ''
        self.xppath = xppath
        

                
    def initialize(self):
        
        self.lg = layergroup.Layergroup(self.xppath,self.gui)
        
        self.sceneries = []
        for lname in self.lg.order:
            l = self.lg.layers[lname]
            if len(l['sceneries'])== 0:
                continue
            for s in sorted(l['sceneries']):
                self.sceneries.append(s)
    
    def getActiveLayer(self):
        if self.activeLayer == '' or self.activeLayer not in self.lg.order:
            return self.lg.order[0]
        else:
            return self.activeLayer
    
    def getLayers(self):
        return self.lg.order
    
    def getSceneries(self):
        l = self.lg.layers[self.getActiveLayer()]
        sceneries = []
        for s in sorted(l['sceneries']):
            sceneries.append(s)
        return sceneries
        

        