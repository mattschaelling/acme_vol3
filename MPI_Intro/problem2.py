# Problem 2
"""Pass a random NumPy array of shape (n,) from the root process to process 1,
where n is a command-line argument. Print the array and process number from
each process.

Usage:
    # This script must be run with 2 processes.
    $ mpiexec -n 2 python problem2.py 4
    Process 1: Before checking mailbox: vec=[ 0.  0.  0.  0.]
    Process 0: Sent: vec=[ 0.03162613  0.38340242  0.27480538  0.56390755]
    Process 1: Recieved: vec=[ 0.03162613  0.38340242  0.27480538  0.56390755]
"""

from mpi4py import MPI
from sys import argv
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n = int(argv[1])
if rank == 0:
    random_vals = np.random.random(n)
    comm.Send(random_vals, dest=1)
    print("Process 0:\t{}".format(random_vals))
elif rank == 1:
    random_vals = np.zeros(n)
    comm.Recv(random_vals, source=0)
    print("Process 1:\t{}".format(random_vals))
