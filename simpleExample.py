from psana import *
from mpi4py import MPI  # large-scale parallelization
import numpy as np
from pypsalg.AngularIntegrationM import *  # algorithms
from psmon import publish  # real time plotting
from psmon.plots import Image


ds = DataSource('exp=xpptut15:run=54:idx')  # run online/offline

det = Detector('cspad')  # simple detector interface


rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

img = None
for run in ds.runs():
    times = run.times()
    mylength = len(times) // size
    mytimes = times[rank * mylength:(rank + 1) * mylength]
    for n, t in enumerate(mytimes):
        evt = run.event(t)  # random access
        if img is None:
            img = det.image(evt)  # many complex run-dependent calibrations
        else:
            img += det.image(evt)
        if n > 5:
            break


img_all = np.empty_like(img)
MPI.COMM_WORLD.Reduce(img, img_all)

if rank == 0:

    ai = AngularIntegratorM()
    ai.setParameters(img_all.shape[0], img_all.shape[1],
                     mask=np.ones_like(img_all))
    bins, intensity = ai.getRadialHistogramArrays(img_all)


    publish.local = True
    img = Image(0, "CsPad", img_all)
    publish.send('image', img)

MPI.Finalize()
