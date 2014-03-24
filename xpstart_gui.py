import Tkinter
from xpstart.xpstartgui import XpstartView


xppath = r"PathToXplane"
  
root = Tkinter.Tk()
root.minsize(450, 400)
root.title("xpstart 0.90")
mainApp = XpstartView(root,xppath)
root.mainloop()  

