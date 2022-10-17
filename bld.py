
from psana import *


"""Beam Line Data is smaller data that can be delivered to all hutches
(i.e. not associated with the DAQ system in one hutch). """

ds = DataSource('exp=xpptut15:run=59:smd')
ebeamDet = Detector('EBeam')
for nevent, evt in enumerate(ds.events()):
    ebeam = ebeamDet.get(evt)
    if ebeam is None:
        continue  # This check is doing nothing (RM-debug)
    print(ebeam.ebeamPhotonEnergy())
    break

