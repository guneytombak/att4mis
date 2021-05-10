import numpy as np

train_id = 'trans02'
data_identifier_source = 'nci'

number_of_epoch = 2000

deterministic = True
seed = 42

loss_mult = [0.5, 0.5]

n0 = 16
pbm = 0.0
batch_size = 8
num_classes = 3
path_to_save_trained_model = './pre_trained'

image_size = (194, 256, 256)
patch_size = (32, 8 ,8)

embedder = {
   'shape'     : tuple([batch_size, n0*8, image_size[1]//8, image_size[2]//8]),
   'size'      : patch_size,
}

transformer = {
    'num_layers'        : 12,
    'd_model'           : np.prod(patch_size),
    'nhead'             : 8,
    'dim_feedforward'   : 1024,
}