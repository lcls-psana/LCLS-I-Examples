
from psana import *
import matplotlib.pyplot as plt

ds = DataSource('exp=xpptut15:run=54:smd')
det = Detector('cspad')
for nevent, evt in enumerate(ds.events()):
    img = det.image(evt)
    # NOTE: non-contiguous array must be copied before using with MPI
    roi_var = img[135:140, 150:160]
    break


plt.imshow(roi_var, interpolation='none')
plt.show()
