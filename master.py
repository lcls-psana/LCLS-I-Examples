
from mpi4py import MPI
from mpidata import mpidata
from psmon import publish
import psmon.plots as psplt
import h5py
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def runmaster(nClients):
    while nClients > 0:
        # Remove client if the run ended
        md = mpidata()
        md.recv()
        if md.small.endrun:
            nClients -= 1
        else:
            plot(md)

def plot(md):
    print(f'Master received image with shape {md.img.shape} and intensity {md.small.intensity}')
