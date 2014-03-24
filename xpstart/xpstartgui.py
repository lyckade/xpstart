import Tkinter as tk
import tkFont        
class XpstartView(tk.Frame):
    
    def __init__(self,parent,xppath):
        
        tk.Frame.__init__(self, parent)
        
        self.END = tk.END
        
        self.fontStyle = tkFont.Font(family="Helvetica", size=9)

        self.layersArea = tk.Frame(parent,borderwidth=1)
        self.layersArea.pack(padx=10,pady=10)
        self.layersLabel = tk.Label(self.layersArea,text="Layers: ")
        self.layersLabel.grid(row=0,column=0)  
        
        self.layersScroll = tk.Scrollbar(self.layersArea, orient=tk.VERTICAL)
        self.layersScroll.grid(row=1,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
              
        self.layersBox = tk.Listbox(
                                    self.layersArea,
                                    yscrollcommand=self.layersScroll.set,
                                    height=10,
                                    width=15,
                                    font=self.fontStyle)
        self.layersBox.grid(row=1,column=0)
        
        self.layersBox.bind("<ButtonRelease-1>", self.setActiveLayer)
        
        #self.sceneriesArea = tk.Frame(parent,borderwidth=1)
        #self.sceneriesArea.pack(side=tk.LEFT,fill=tk.X,padx=10,pady=10)

        self.sceneriesLabel = tk.Label(self.layersArea,text="Sceneries: ")
        self.sceneriesLabel.grid(row=0,column=2)
        
        self.sceneriesyScroll = tk.Scrollbar(self.layersArea, orient=tk.VERTICAL)
        self.sceneriesyScroll.grid(row=1,column=3,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.sceneriesBox = tk.Listbox(
                                    self.layersArea,
                                    yscrollcommand=self.sceneriesyScroll.set,
                                    height=10,
                                    width=50,
                                    font=self.fontStyle,
                                    )
        self.sceneriesBox.grid(row=1,column=2)
        #self.sceneriesBox.pack(side=tk.LEFT)
        self.sceneriesyScroll.config(command = self.sceneriesBox.yview)
        
        
        
        self.infoArea = tk.Frame(parent,borderwidth=1)
        self.infoArea.pack()
        self.messageScroll = tk.Scrollbar(self.infoArea, orient=tk.VERTICAL)
        self.messageScroll.grid(row=1,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
        self.messageBox = tk.Text(
                                  self.infoArea,
                                  yscrollcommand=self.messageScroll.set,
                                  width=65,
                                  height=6,
                                  font=self.fontStyle,
                                  )
        self.messageBox.grid(row=1,column=0)
        self.messageScroll.config(command = self.messageBox.yview)      
        #self.messageBox.insert(tk.END, "Test")
        
        #------------------------------------------------ loading the controller
        self.controller = XpstartController(xppath,self)
        
        #----------------------------------------------- actions after the layer
        self.loadLayers()
        self.loadSceneries()  

        
    def loadLayers(self):
        layers = self.controller.getLayers()
        for lname in layers:
            self.layersBox.insert(tk.END,lname)
            
    def loadSceneries(self):
        self.sceneriesBox.delete(0, tk.END)
        sceneries = self.controller.getSceneries()
        for s in sceneries:
            self.sceneriesBox.insert(tk.END,s)
            
    def setActiveLayer(self,data):
        self.controller.activeLayer = self.controller.lg.order[int(self.layersBox.curselection()[0])]
        #print self.controller.activeLayer
        #print self.controller.lg.order[int(self.layersBox.curselection()[0])]
        self.loadSceneries()
        #print self.layersBox.curselection()
        #print data

import layergroup
import xpstart  
      
class XpstartController:
    
    def __init__(self,xppath,gui):
        
        self.gui = gui

        self.activeLayer = ''
        self.xppath = xppath
        
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
        

        