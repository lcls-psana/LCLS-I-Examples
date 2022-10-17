import psana
from ImgAlgos.PyAlgos import PyAlgos


ds = psana.DataSource('exp=xpptut15:run=54:smd')
det = psana.Detector('cspad')
alg = PyAlgos()

for nevent, evt in enumerate(ds.events()):
    if nevent >= 2:
        break
    nda = det.calib(evt)
    if nda is None:
        continue

    thr = 20
    numpix = alg.number_of_pix_above_thr(nda, thr)
    totint = alg.intensity_of_pix_above_thr(nda, thr)
    print(f'{numpix:d} pixels have total intensity {totint:5.1f} above threshold {thr:5.1f}')


