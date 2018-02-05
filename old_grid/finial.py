import numpy as np
import random
np.set_printoptions(threshold=np.inf)  
n=50
low = 0
high = 30
density = 0.15
_ = 9999999999
start = 0
end = n - 1
# graph=[  
#         [0,6,3,_,_,_],  
#         [6,0,2,5,_,_],  
#         [3,2,0,3,4,_],  
#         [_,5,3,0,2,3],  
#         [_,_,4,2,0,5],  
#         [_,_,_,3,5,0],  
#         ]  
graph = []
flag = [False]*n
def mat_init(low=0, high = 10, size = 20, density=0.3):
    mp = np.random.random_integers(low, high, size*size).reshape(size,size)
    #symmetric matrix
    # mp2 = mp
    for i in range(size):
        for j in range(i):
            if mp[i,j] < high-(high-low)*density:
                mp[i,j] = _
                # mp2[i,j] = 0
            else:
                mp[i,j] = random.randint(low, high)
                # mp2[i,j] = mp[i,j]
            mp[j,i] = mp[i,j]
            # mp2[j,i] = mp2[i,j]
        mp[i,i] = _
        # mp2[i,i] = 0
    return mp
def is_connect_graph(graph):
    # flag=[False]*n
    count = 0
    for i in range(n):
        if flag[i] == False:
            dfs(i)
            count += 1
    if count == 1:
        return count
    else:
        return count
def dfs(v):
    flag[v] = True
    for i in range(n):
        if graph[v][i] != 0 and graph[v][i] != _ and flag[i] == False:
            dfs(i)
def dijkstra(graph,n):  
    dis=[0]*n  
    flag=[False]*n  
    pre=[0]*n  
    flag[0]=True  
    k=0  
    for i in range(n):  
        dis[i]=graph[k][i] 
    for j in range(n-1):  
        mini=_  
        for i in range(n):  
            if dis[i]<mini and not flag[i]:  
                mini=dis[i]  
                k=i  
        if k==0:
            return  
        flag[k]=True  
        for i in range(n):  
            if dis[i]>dis[k]+graph[k][i]:  
                dis[i]=dis[k]+graph[k][i]  
                pre[i]=k  
#       print(k)  
    return dis,pre
dist=0
X = np.zeros((1,n*n))
y = np.zeros(1)
first = 0
count = 0
for i in range(9999999):
	flag = [False]*n
	graph = mat_init(low,high,n,density)
	# print graph
	a = is_connect_graph(graph)
	if i%1000 == 0:
		print i,a
	# print a 
	if a == 1:
		dis, pre = dijkstra(graph, n)
		dist = dis[n-1]
		# graph[graph == 9999] = 0
		if first == 0:
			X += graph.reshape(-1,n*n)
			y += dist
			first = 1
			# print X,y
			count += 1
		else:
			X = np.vstack((X,graph.reshape(-1,n*n)))
			# print dis[n-1]
			y = np.vstack((y,dist))
			count += 1
			if count >1000:
				break
# print X ,y
print y
print X.shape, y.shape
# np.save("X2.npy", X)
# np.save("y2.npy", y)