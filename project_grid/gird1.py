# step 1, create a grid and get a adjacent matrix
# step 2, get some MSTs from some start points on grid, combine them get a map
# step 3, reset weight of edge on the map
# step 4, calculate the APSP and get distance matrix
import numpy as np  
import random   
np.set_printoptions(threshold=np.inf)    
  
# not exist a edge  
inf = 0xfffffffffffffff 
# set grid's size  
N = 10  
# [north, east, south, west] if exist a path, then the value should be weight  
D = 4
# number of mst
num_start = 10    

def generate_mp(size=N, dime=D):  
	# init mp matrix
	# the first arg and second arg determine the path density
	e = np.random.random_integers(0,3,(N,N,D))

	# same edge has same weight
	for i in range(N-1):
		e[:, i, 1] = e[:, i+1, 3]
	for i in range(N-1):
		e[i, :, 2] = e[i+1, :, 0]

	#set edge value  
	#north  
	e[0,:,0] = inf  
	#east  
	e[:,N-1,1] = inf  
	#south  
	e[N-1,:,2] = inf  
	#west  
	e[:,0,3] = inf

	# transform a grid to a adjacent matrix
	adj_mat = np.zeros((N*N,N*N))
	adj_mat += inf
	for i in range(N*N):
		adj_mat[i, i] = inf
		ix = i / N
		iy = i % N
		if e[ix, iy, 1] != inf:
			adj_mat[i, i+1] = e[ix, iy, 1]
			adj_mat[i+1, i] = adj_mat[i, i+1]
		if e[ix, iy, 2] != inf:
			adj_mat[i, i+N] = e[ix, iy, 2]
			adj_mat[i+N, i] = adj_mat[i, i+N]
	# get a N*N by N*N adjacent matrix 
	return adj_mat

#find MST in a connected graph G, G is a adjacent matrix
# output a adjacent matrix where two points has a edge and the weight of edge is equal to 1
def MST(G, s):
	num_ver = G.shape[0]
	mst = np.zeros_like(G)
	mst += inf

	lowcost = np.zeros(num_ver)
	addvnew = np.zeros(num_ver)
	adjacent = np.zeros(num_ver, np.int32)

	for i in range(num_ver):
		lowcost[i] = G[s,i]
		adjacent[i] = s
	# add vertex start
	addvnew[s] = 1

	for i in range(num_ver):
		min_weight = inf
		v = -1
		# find the edge which has lowest weight adjacent to the visited vertexes set
		for j in range(num_ver):
			if addvnew[j] == 0 and lowcost[j] < min_weight:
				min_weight = lowcost[j]
				v = j
		if v != -1:
			addvnew[v] = 1 # append v in visited vertex set
			temp = adjacent[v]
			mst[temp,v] = 1
			mst[v,temp] = 1

			# update lowcost
			for j in range(num_ver):
				if addvnew[j] == 0 and G[v,j] < lowcost[j]:
					lowcost[j] = G[v,j]
					adjacent[j] = v
	return mst

# randomly choose some start points on the grid,
# then, get a MST for each point, 
# finally, combine these MST to get a sparse map which all points are connected  
def generate_MST(size = N, dim = D, num_start = num_start):
	e = np.zeros((num_start, N*N, N*N))
	for i in range(num_start):
		e[i] = generate_mp(N, D)
	# print e
	# print np.sum(e != inf)
	mst = np.zeros((num_start,N*N,N*N))
	# randomly generate num_start start points
	s = np.random.random_integers(0, N*N-1, num_start)

	# get a MST for each start point
	for i in range(num_start):
		mst[i] = MST(e[i], s[i])

	# combine these MSTs
	mst_out = np.min(mst, axis = 0)
	# a 10*10 grid has 180 edge, we can get 102~110 edge, density is approximately 0.567~0.611
	return mst_out

# reset weight 
def reset_weight(dist_mat):
	mask = 1*(dist_mat == 1)
	# get power exponent for every edge randomly, range from 1 to 9
	weight_exp = np.random.random_integers(1, 6, mask.shape)
	# base is 1.3
	weight_power = pow(1.5, weight_exp)
	# coefficient matrix product power matrix 
	weight_mat = np.random.uniform(low = 0.7, high = 1.1, size = mask.shape) * weight_power
	# keep values in weight_mat where dist_mat values are equal to 1 (have a edge) 
	weight = weight_mat * mask
	# add unreachable edge
	weight += inf*(weight == 0)
	return weight
	pass
# calculate every pair of points' distance,
def Folyed(adj_mat):
	num_nodes = adj_mat.shape[0]

	for k in range(num_nodes):
		for i in range(num_nodes):
			for j in range(num_nodes):
				if adj_mat[i,k] != inf and adj_mat[k,j] != inf and adj_mat[i,j] > adj_mat[i,k]+adj_mat[k,j] and i != j:
					adj_mat[i,j] = adj_mat[i,k]+adj_mat[k,j]
		adj_mat[k,k] = 0
	return adj_mat
	pass
# round distance matrix, approximate 10^n, errors range -0.25*10^n ~ +0.25*10^n,
# has 0~18, 19 classes in total
def round_dis_mat(dist_mat):
	# # deal with unreachable
	# mask = 1*(dist_mat != inf)
	# unreachable_label = 25*(mask == 0)
	dist_mat = 2 * np.log(dist_mat) / np.log(1.5)
	dist_mat = np.round(dist_mat)
	for i in range(dist_mat.shape[0]):
		dist_mat[i,i] = 21
	# # remove unreachable edge
	# dist_mat = dist_mat * mask
	# # add unreachable edge label, that is 20
	# dist_mat += unreachable_label
	return dist_mat
	pass
def get_graph_and_distmat(size = N, dim = D, num_start = num_start):
	# get combined MST
	comb_mst = generate_MST(N, D, num_start)
	# get adjacent matrix
	adj_mat = reset_weight(comb_mst)
	print adj_mat[1,1],adj_mat[40,40]
	# get distance matrix
	dist_mat = Folyed(adj_mat)
	print dist_mat[1,1], dist_mat[40,40]
	# get label matrix, where label is got from round with distance
	label_mat = round_dis_mat(dist_mat)

	# output adjacent matrix and label matrix
	return adj_mat, label_mat

# if __name__ == "__main__":
# 	adj_mat, label_mat = get_graph_and_distmat(size = 10, dim = 4, num_start = 10)
# 	print adj_mat[1,1]
# 	print label_mat
# 	count = 0
# 	for i in range(22):
# 		num = np.sum(label_mat == i)
# 		count += num
# 		print i, num
# 	print count
num = 0  
X = np.zeros((1,N**4))  
y = np.zeros((1,N**4))  
first = 1  
while(num<1000000):  
    adj_mat, label_mat = get_graph_and_distmat(N, D, num_start)  
    x_ = adj_mat.reshape(1,-1)
    y_ = label_mat.reshape(1,-1)
	if first == 1:  
	    X += x_  
	    y += y_  
	    first = 0  
	    num += 1  
	    continue  
	X = np.vstack((X, x_))  
	y = np.vstack((y, y_))  
	num += 1  
	if num%1000 == 0:  
	    print num  
	if num%10000== 0:  
	    np.save("X"+str(num/10000)+".npy", X)  
	    np.save("y"+str(num/10000)+".npy", y)  
	    print X.shape, y.shape  
	    first = 1  
	    X = np.zeros((1,N**4))  
	    y = np.zeros((1,N**4)) 
