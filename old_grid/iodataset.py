import random
import numpy as np
np.set_printoptions(threshold=np.inf)  

# a = np.loadtxt('data.txt')
# print a[:,:]
# b=2.5
# with open("data.txt", 'r') as f:
# 	data = f.readlines()
# 	for line in data:
# 		odom = line.split()
# 		numbers_float = map(float, odom)
# 		print numbers_float


# with open("data.txt", 'a') as f:
# 	f.write(str(b))

a = np.load("X.npy")
b = np.load("y.npy").reshape(1,-1).astype(np.int32)
print a.shape,b.shape
print b.dtype,b[0,0]
N = a.shape[0]
y_all = np.zeros((N,270))
y_all[range(N),b] = 1
print y_all[0,45]