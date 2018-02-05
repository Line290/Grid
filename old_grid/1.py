import random
import numpy as np



low = 0
high = 10
size = 6
_ = 9999999
density = 0.9

start = 0
end = size-1
flag=[False]*size
#generate a size*size map matrix randomly, which values range from low to high
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
    flag=[False]*size
    count = 0
    for i in range(size):
        if flag[i] == False:
            dfs(graph, i)
            count += 1
    if count == 1:
        return 1
    else:
        return 0
def dfs(graph,v):
    flag[v] = True
    for i in range(size):
        if graph[v][i] != 0 and graph[v][i] != _ and flag[i] == False:
            dfs(graph, i)     
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

graph= mat_init(low, high, size, density)
# flag = is_connect_graph(graph,size)
if flag == 1:
    dis, pre = dijkstra(graph, size)
    graph[graph == 9999] = 0
    print graph
    print dis
    print pre
if __name__=='__main__':  
    n=6  
    graph=[  
            [0,6,3,_,_,_],  
            [6,0,2,5,_,_],  
            [3,2,0,3,4,_],  
            [_,5,3,0,2,3],  
            [_,_,4,2,0,5],  
            [_,_,_,3,5,0],  
            ]  
    dis,pre=dijkstra(graph,n)  
    a = is_connect_graph(graph)
    print a
    print(dis)  
    print(pre)  