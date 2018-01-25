# Problem 3
"""In each process, generate a random number, then send that number to the
process with the next highest rank (the last process should send to the root).
Print what each process starts with and what each process receives.

Usage:
    $ mpiexec -n 2 python problem3.py
    Process 1 started with [ 0.79711384]        # Values and order will vary.
    Process 1 received [ 0.54029085]
    Process 0 started with [ 0.54029085]
    Process 0 received [ 0.79711384]

    $ mpiexec -n 3 python problem3.py
    Process 2 started with [ 0.99893055]
    Process 0 started with [ 0.6304739]
    Process 1 started with [ 0.28834079]
    Process 1 received [ 0.6304739]
    Process 2 received [ 0.28834079]
    Process 0 received [ 0.99893055]
"""

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

random_val = np.random.random(1)
print("Process {} started with {}".format(rank, random_val))
comm.Send(random_val, dest=(rank+1)%size)
comm.Recv(random_val, source=(rank-1)%size)
print("Process {} received {}".format(rank, random_val))
