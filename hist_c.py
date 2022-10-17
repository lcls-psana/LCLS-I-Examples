from psana import *
from pypsalg import Hist1D
import matplotlib.pyplot as plt

ds = DataSource('exp=xpptut15:run=54:smd')
det = Detector('cspad')

hist = Hist1D(5, -5., 5.0)
for nevent, evt in enumerate(ds.events()):
    if nevent >= 4:
        break
    calib_array = det.calib(evt)
    hist.fill(float(calib_array[0, 0, 0]), 1.0)


plt.bar(hist.xaxis(), hist.get())
plt.show()
