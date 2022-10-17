from psana import *
import matplotlib.pyplot as plt

ds = DataSource('exp=amotut13:run=206')
det = Detector('AmoETOF.0:Acqiris.0')

for nevent, evt in enumerate(ds.events()):
    # waveforms are in Volts, times are in Seconds
    waveforms = det.waveform(evt)
    times = det.wftime(evt)
    # this shows there are 8 channels, each with 20000 samples
    print(f'{waveforms.shape} {times.shape}')
    break


plt.plot(times[0], waveforms[0])
plt.show()
