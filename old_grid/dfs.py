import numpy as np
import random
n=20
low = 0
high = 30
density = 0.15
_ = 9999
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
        mp[i,i] = 0
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
graph = mat_init(low,high,n,density)
# print graph
a = is_connect_graph(graph)
if a == 1:
    dis, pre = dijkstra(graph, n)
    graph[graph == 9999] = 0
    print graph.reshape(-1,n*n)
    print dis[n-1]
    # print pre
    # print a
else:
    print a 