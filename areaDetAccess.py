
from psana import *
import matplotlib.pyplot as plt

ds = DataSource('exp=xpptut15:run=54:smd')
det = Detector('cspad')
for nevent, evt in enumerate(ds.events()):
    # includes pedestal subtraction, common-mode correction, bad-pixel
    # suppression, and returns an "un-assembled" 3D array of cspad panels
    calib_array = det.calib(evt)
    # this is the same as the above, but also uses geometry to
    # create an "assembled" 2D image (including "fake pixels" in gaps)
    img = det.image(evt)
    break

plt.imshow(img, vmin=-2, vmax=2)
plt.show()
