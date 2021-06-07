from mpi4py import MPI;
import numpy as np
#import pandas as pd
from matplotlib import pyplot as plt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
root = 0

data = []
centers_new = []
centers_old = []
chunks = []
# Number of clusters
k = 3

#print ("Hello, world! My rank is " + str(comm.rank))
if(rank == 0) :
    centers_1 = np.array([1,1])
    centers_2 = np.array([5,5])
    centers_3 = np.array([8,1])

    data_1 = np.random.randn(100,2) + centers_1
    data_2 = np.random.randn(100,2) + centers_2
    data_3 = np.random.randn(100,2) + centers_3


    data = np.concatenate((data_1, data_2, data_3), axis=0)
    chunks = [[] for _ in range(size)]
    for i, chunk in enumerate(data):
        chunks[i % size].append(chunk)
    #data = np.random.randn(size,200)
    #plt.scatter(data[:,0], data[:,1], s=7)


    # Number of features in the data
    c = data.shape[1]

    # Generate random centers, here we use sigma and mean to ensure it represent the whole data
    mean = np.mean(data, axis = 0)
    std = np.std(data, axis = 0)
    centers_new = np.random.randn(k,c)*std + mean


local_data = comm.scatter(chunks, root)
def recenter():
    local_centers = comm.bcast(centers_new,root)
    print(str(rank) + " received centers ")
    print(local_centers)
    print(len(local_centers))

    n = local_data.shape[0]
    distances = np.zeros((n, k))
    clusters = np.zeros(n)

    for i in range(k):
        distances[:, i] = np.linalg.norm(data - local_centers[i], axis=1)
        # Assign all training data to closest center
    clusters = np.argmin(distances, axis=1)



    error = np.linalg.norm(centers_new - centers_old)

    error = 0
    if(rank == 0 and error != 0) :
        recenter()

recenter()




