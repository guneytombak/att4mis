import torch
from torchvision import transforms
from data import HDF5Dataset

def load_datasets(dataset_name, batch_size, tf = transforms.ToTensor()):
    train_loader, test_loader, val_loader = None, None, None
        
    if dataset_name == 'abide_caltech':
        train_loader, test_loader, val_loader = getAbideCaltech(batch_size = batch_size, TF = tf)
        
    if dataset_name == 'abide_stanford':
        train_loader, test_loader, val_loader = getAbideStanford(batch_size = batch_size, TF = tf)
        
    if dataset_name == 'hcp_t1':
        train_loader, test_loader, val_loader = getHCPT1w(batch_size = batch_size, TF = tf)
        
    if dataset_name == 'hcp_t2':
        train_loader, test_loader, val_loader = getHCPT2w(batch_size = batch_size, TF = tf)
                
    return train_loader, test_loader, val_loader

def getAbideCaltech(batch_size, TF):
    path_train = 'data/abide/caltech/data_T1_2d_size_256_256_depth_256_res_0.7_0.7_from_0_to_10.hdf5'
    path_validation = 'data/abide/caltech/data_T1_2d_size_256_256_depth_256_res_0.7_0.7_from_10_to_15.hdf5'
    path_test = 'data/abide/caltech/data_T1_2d_size_256_256_depth_256_res_0.7_0.7_from_16_to_36.hdf5'
    
    
    ds_train = HDF5Dataset.HDF5Dataset(path_train, TF)
    train_loader = torch.utils.data.DataLoader(ds_train, batch_size = batch_size, shuffle = True)
    
    ds_test = HDF5Dataset.HDF5Dataset(path_test, TF)
    test_loader = torch.utils.data.DataLoader(ds_test, batch_size = batch_size, shuffle = False)
    
    ds_validation = HDF5Dataset.HDF5Dataset(path_validation, TF)
    val_loader = torch.utils.data.DataLoader(ds_validation, batch_size = batch_size, shuffle = False)
    
    return train_loader, test_loader, val_loader

def getAbideStanford(batch_size, TF):
    path_train = 'data/abide/stanford/data_T1_2d_size_256_256_depth_132_res_0.7_0.7_from_0_to_10.hdf5'
    path_validation = 'data/abide/stanford/data_T1_2d_size_256_256_depth_132_res_0.7_0.7_from_10_to_15.hdf5'
    path_test = 'data/abide/stanford/data_T1_2d_size_256_256_depth_132_res_0.7_0.7_from_16_to_36.hdf5'
    
    ds_train = HDF5Dataset.HDF5Dataset(path_train, TF)
    train_loader = torch.utils.data.DataLoader(ds_train, batch_size = batch_size, shuffle = True)
    
    ds_test = HDF5Dataset.HDF5Dataset(path_test, TF)
    test_loader = torch.utils.data.DataLoader(ds_test, batch_size = batch_size, shuffle = False)
    
    ds_validation = HDF5Dataset.HDF5Dataset(path_validation, TF)
    val_loader = torch.utils.data.DataLoader(ds_validation, batch_size = batch_size, shuffle = False)
    
    return train_loader, test_loader, val_loader

def getHCPT1w(batch_size, TF):
    path_train = 'data/hcp/data_T1_2d_size_256_256_depth_256_res_0.7_0.7_from_0_to_20.hdf5'
    path_validation = 'data/hcp/data_T1_2d_size_256_256_depth_256_res_0.7_0.7_from_20_to_25.hdf5'
    path_test = 'data/hcp/data_T1_2d_size_256_256_depth_256_res_0.7_0.7_from_50_to_70.hdf5'
    
    ds_train = HDF5Dataset.HDF5Dataset(path_train, TF)
    train_loader = torch.utils.data.DataLoader(ds_train, batch_size = batch_size, shuffle = True)
    
    ds_test = HDF5Dataset.HDF5Dataset(path_test, TF)
    test_loader = torch.utils.data.DataLoader(ds_test, batch_size = batch_size, shuffle = False)
    
    ds_validation = HDF5Dataset.HDF5Dataset(path_validation, TF)
    val_loader = torch.utils.data.DataLoader(ds_validation, batch_size = batch_size, shuffle = False)
    
    return train_loader, test_loader, val_loader

def getHCPT2w(batch_size, TF):
    path_train = 'data/hcp/data_T2_2d_size_256_256_depth_256_res_0.7_0.7_from_0_to_20.hdf5'
    path_validation = 'data/hcp/data_T2_2d_size_256_256_depth_256_res_0.7_0.7_from_20_to_25.hdf5'
    path_test = 'data/hcp/data_T2_2d_size_256_256_depth_256_res_0.7_0.7_from_50_to_70.hdf5'
    
    ds_train = HDF5Dataset.HDF5Dataset(path_train, TF)
    train_loader = torch.utils.data.DataLoader(ds_train, batch_size = batch_size, shuffle = True)
    
    ds_test = HDF5Dataset.HDF5Dataset(path_test, TF)
    test_loader = torch.utils.data.DataLoader(ds_test, batch_size = batch_size, shuffle = False)
    
    ds_validation = HDF5Dataset.HDF5Dataset(path_validation, TF)
    val_loader = torch.utils.data.DataLoader(ds_validation, batch_size = batch_size, shuffle = False)
    
    return train_loader, test_loader, val_loader


















