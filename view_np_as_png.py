from matplotlib import pyplot as plt
import numpy as np

mri_orig = np.load('synthrad_train_np/1BA001/mri_orig.npy')
ct_orig = np.load('synthrad_train_np/1BA001/ct_orig.npy')
mri_norm = np.load('synthrad_train_np/1BA001/mri_normalized.npy')
ct_norm = np.load('synthrad_train_np/1BA001/ct_normalized.npy')
mri_nsized = np.load('synthrad_train_np/1BA001/mri_normsized.npy')
ct_nsized = np.load('synthrad_train_np/1BA001/ct_normsized.npy')

print(f'SHAPES - mri_orig: {mri_orig.shape}, ct_orig: {ct_orig.shape}, mri_norm: {mri_norm.shape}, ct_norm: {ct_norm.shape}, mri_nsized: {mri_nsized.shape}, ct_nsized: {ct_nsized.shape}')

for arr, name in [(mri_orig, 'mri_orig'), (ct_orig, 'ct_orig'), 
                  (mri_norm, 'mri_norm'), (ct_norm, 'ct_norm')]:
    print(f"Saving {name}:")
    for i in range(9, arr.shape[2], 10):
        plt.imshow(arr[:, :, i])
        plt.savefig(f'synthrad_train_np/1BA001/{name}_{i+1}.png')
        plt.clf()
        print(f"\tsaved {i+1}")

for arr, name in [(mri_nsized, 'mri_nsized'), (ct_nsized, 'ct_nsized')]:
    print(f"Saving {name}:")
    for i in range(9, arr.shape[0], 10):
        plt.imshow(arr[i][0])
        plt.savefig(f'synthrad_train_np/1BA001/{name}_{i+1}.png')
        plt.clf()
        print(f"\tsaved {i+1}")