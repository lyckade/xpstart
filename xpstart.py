import os.path
import Tkinter
from xpstart.xpstartgui import XpstartView


xppath = os.path.dirname(__file__) # Can be set, if xpstart is installed outside of the XP installation
  
root = Tkinter.Tk()
root.minsize(450, 400)
root.title("xpstart 0.90")
mainApp = XpstartView(root,xppath)
root.mainloop()  

