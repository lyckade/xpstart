import xpstart.layergroup
import os.path

xppath = os.path.dirname(__file__) # Can be set, if xpstart is installed outside of the XP installation

lg = xpstart.layergroup.Layergroup(xppath)
sceneries = []
for lname in lg.order:
    l = lg.layers[lname]
    if len(l['sceneries'])== 0:
        continue
    for s in sorted(l['sceneries']):
        sceneries.append(s)
        print s
import xpstart.scenerypacks
sp = xpstart.scenerypacks.Scenerypacks(xppath)
sp.order = sceneries
sp.writeIniFile()