import caffe
import numpy as np
import lmdb
filenames = [['train_input','train_output'],
             ['val_input','val_output'],
             ['test_input','test_output']]
end = [98,99,100]
start = [0,98,99]
name = ['X','y']
file_order = 0
for k, filename in enumerate(filenames):
    while file_order < end[k]:
        for j in range(2):
            x = np.load(name[j]+str(file_order)+".npy")
            x = x.astype(np.float32).reshape(10000,1,100,100)
            in_db = lmdb.open(filename[j], map_size=int(x.nbytes*1000))
            with in_db.begin(write=True) as in_txn:
                for i in range(x.shape[0]):
                    im = x[i]
                    im_dat = caffe.io.array_to_datum(im)
                    in_txn.put('{:0>10d}'.format(i+(file_order-start[k])*10000), im_dat.SerializeToString())
            in_db.close()
        file_order += 1
