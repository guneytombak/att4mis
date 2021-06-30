import numpy as np

data_identifier_source = 'nci'
data_identifier_target = 'nci'
experiment_name = 'id03_1'

save_images = False
save_path = './results/%s/test/%s' % (data_identifier_source, experiment_name)
model_path = './pre_trained/nci_model_segmentation_id03_1.pth'

use_attention = False
noBtNk = False

train_id = experiment_name
batch_size = 1

n0 = 64
image_size = (256, 256, 20)
no_slices = [20, 20, 20, 20, 19, 20, 20, 15, 20, 20]