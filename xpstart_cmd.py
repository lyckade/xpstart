
import xpstart.layergroup
import xpstart.xpstart
import os.path

b = xpstart.xpstart.Base()

xppath = os.path.dirname(__file__) # Can be set, if xpstart is installed outside of the XP installation

layerOutputFile = "xpstart/scenerypacks_info.txt"

lo = open(layerOutputFile,"w")

lg = xpstart.layergroup.Layergroup(xppath)
sceneries = []
for lname in lg.order:
    lo.write("\nLayer: %s\n" % (lname))
    l = lg.layers[lname]
    if len(l['sceneries'])== 0:
        continue
    for s in sorted(l['sceneries']):
        sceneries.append(s)
        b.echo(s)
        lo.write("%s\n"%(s))
import xpstart.scenerypacks
sp = xpstart.scenerypacks.Scenerypacks(xppath)
sp.order = sceneries
sp.writeIniFile()