# grab the central 35 slices from each image and split into train
import glob
import random
import h5py
from utils_colter import *

folder_name = '/media/hdd6/colter/synthrad_train_np/*'
paired_files = get_dataset(folder_name, file_type='npy', mri_fn = 'mri_normsized.npy', ct_fn = 'ct_normsized.npy')
random.shuffle(paired_files)

# 60-20-20 train/validation/test split
paired_train = paired_files[:108]
paired_val = paired_files[108:144]
paired_test = paired_files[144:]

print(f"Concatenating {len(paired_train)} training images")
mri_train_concat, ct_train_concat = concat_middle_ns(paired_train, 35)
print(f"Concatenating {len(paired_val)} training images")
mri_val_concat, ct_val_concat = concat_middle_ns(paired_val, 35)
print(f"Concatenating {len(paired_test)} training images")
mri_test_concat, ct_test_concat = concat_middle_ns(paired_test, 35)

def save_data(folder_name, file_name, data):
    os.makedirs(folder_name, exist_ok=True)
    with h5py.File(os.path.join(folder_name, file_name), 'w') as f:
        f.create_dataset('data_fs', data=data)
    
print(f"Saving mri_train")
save_data('/home/colter/hdd6_colter/synthrad_h5/', 'data_train_mri.mat', mri_train_concat)
print(f"Saving ct_train")
save_data('/home/colter/hdd6_colter/synthrad_h5/', 'data_train_ct.mat', ct_train_concat)
print(f"Saving mri_val")
save_data('/home/colter/hdd6_colter/synthrad_h5/', 'data_val_mri.mat', mri_val_concat)
print(f"Saving ct_val")
save_data('/home/colter/hdd6_colter/synthrad_h5/', 'data_val_ct.mat', ct_val_concat)
print(f"Saving mri_test")
save_data('/home/colter/hdd6_colter/synthrad_h5/', 'data_test_mri.mat', mri_test_concat)
print(f"Saving ct_test")
save_data('/home/colter/hdd6_colter/synthrad_h5/', 'data_test_ct.mat', ct_test_concat)
