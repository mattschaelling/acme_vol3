# Problem 4
"""The n-dimensional open unit ball is the set U_n = {x in R^n : ||x|| < 1}.
Estimate the volume of U_n by making N draws on each available process except
for the root process. Have the root process print the volume estimate.

Command line arguments:
    n (int): the dimension of the unit ball.
    N (int): the number of random draws to make on each process but the root.

Usage:
    # Estimate the volume of U_2 (the unit circle) with 2000 draws per process.
    $ mpiexec -n 4 python problem4.py 2 2000
    Volume of 2-D unit ball: 3.13266666667      # Results will vary slightly.
"""

from mpi4py import MPI
import numpy as np
from sys import argv
import scipy.linalg as la

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n, N = int(argv[1]), int(argv[2])

if rank != 0:
    sample = np.random.uniform(-1,1,(n,N))
    lengths = la.norm(sample, axis=0)
    num_within = np.array([np.float(np.count_nonzero(lengths < 1))])
    comm.Send(num_within, dest=0)
else:
    total_num_within = 0.
    for i in range(1,size):
        receiving_count = np.zeros(1)
        comm.Recv(receiving_count, source=i)
        total_num_within += receiving_count[0]
    estimate = 2**n * (np.float(total_num_within) / ((size-1)*N))
    print("Volume of {}-D unit ball: {}".format(n, estimate))
