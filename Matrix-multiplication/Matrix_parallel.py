from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

mat_len = 0
if rank == 0:
    mat_len = int(input("enter size of matrices : "))

mat_len = comm.bcast(mat_len, root = 0)


f = open(str(mat_len)+"_"+str(size)+"/"+"input_data_row_" + str(rank) + ".txt","r")
rows = f.readlines()
f.close()
for a in range(len(rows)):
    rows[a] = [int(x) for x in rows[a].split()]


f = open(str(mat_len)+"_"+str(size)+"/"+"input_data_col_" + str(rank) + ".txt","r")
cols = f.readlines()
f.close()
for a in range(len(cols)):
    cols[a] = [int(x) for x in cols[a].split()]

cols = [[cols[j][i] for j in range(len(cols))] for i in range(len(cols[0]))]

send_data = cols
result = [[0 for x in range(len(rows[0]))] for y in range(len(rows))]

starti=0
startj=0
index_i=0
index_j=0

stt = time.time()
for n in range(size):
    index_j+=starti
    starti=0
    for i in range(len(rows)):
        starti+=1
        for j in range(len(cols[0])):
            for k in range(len(cols)):
                print(j+index_j,rank)
                result[i][j+index_j] += rows[i][k] * cols[k][j]

    if rank == 0:
        comm.send(send_data,dest=(rank-1)%size)
    if rank > 0:
        cols = comm.recv(source=(rank+1)%size)
        comm.send(send_data, dest=(rank - 1)%size)
    if rank == 0:
        cols = comm.recv(source=1)
    send_data = cols

print("time ends"+str(time.time())+":"+str(time.time()-stt))

if rank == 0:
    f = open('output.txt','a')
    lines = str(len(result[0]))+'_'+str(size)+' : '+str(time.time()-stt)+'\n'
    f.write(lines)
    f.close()
