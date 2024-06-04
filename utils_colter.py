import os
from sys import stdout
import numpy as np
import glob
import nibabel as nib


# resize an n1 x m1 image to an n2 x m2 image
# resize from source each time if possible
def resize(data, n2, m2):
    data = data.transpose()
    new_data = -1 * np.ones((n2, m2))
    n1 = data.shape[0]
    m1 = data.shape[1]

    for y in range(n1):
        for x in range(m1):
            if 0 <= y + (n2 - n1) // 2 < n2 and 0 <= x + (m2 - m1) // 2 < m2:
                new_data[y + (n2 - n1) // 2][x + (m2 - m1) // 2] = data[y][x]

    return new_data

def testing_resize():
    # testing with small examples
    mat5x5 = np.arange(5 * 5).reshape(5, 5)
    print("Original 5x5 matrix:")
    print(mat5x5)
    print("Resized to 7x7:")
    print(resize(mat5x5, 7, 7))
    print("Resized to 3x3:")
    print(resize(mat5x5, 3, 3))
    print("Resized to 8x8:")
    print(resize(mat5x5, 8, 8))
    print("Resized to 6x6:")
    print(resize(mat5x5, 6, 6))
    print("Resized to 4x4:")
    print(resize(mat5x5, 4, 4))
    print("Resized to 2x2:")
    print(resize(mat5x5, 2, 2))

    mat6x6 = np.arange(6 * 6).reshape(6, 6)
    print("Original 6x6 matrix:")
    print(mat6x6)
    print("Resized to 8x8:")
    print(resize(mat6x6, 8, 8))
    print("Resized to 4x4:")
    print(resize(mat6x6, 4, 4))
    print("Resized to 9x9:")
    print(resize(mat6x6, 9, 9))
    print("Resized to 7x7:")
    print(resize(mat6x6, 7, 7))
    print("Resized to 5x5:")
    print(resize(mat6x6, 5, 5))
    print("Resized to 3x3:")
    print(resize(mat6x6, 3, 3))

# resize scan[x][y] to out[0][x256][y256]
def resize_scan(scan):
    out = np.zeros((scan.shape[2], 1, 256, 256))
    for i in range(scan.shape[2]):
        out[i][0] = resize(scan[:, :, i], 256, 256)
    return out

def resize_dataset(dataset):
    # mris = [] # np.array((len(dataset), 1, 256, 256))
    # cts = [] # np.array((len(dataset), 1, 256, 256))
    print("Resizing dataset:", end = ' ')
    for i in range(len(dataset)):
        print(i, end = ', ')
        dataset[i][1] = resize_scan(dataset[i][1])
        dataset[i][2] = resize_scan(dataset[i][2])
        # folder, mri, ct = dataset[i]
        # mris.append(resize_scan(mri))
        # cts.append(resize_scan(ct))
    print()
    # return mris, cts

def get_dataset(folder_name, file_type = 'nii', mri_fn = 'mr.nii.gz', ct_fn = 'ct.nii.gz'):
    synthrad_train_folders = sorted(glob.glob(folder_name))
    paired_files = []
    print("Loading dataset:", end = ' ')
    for (i, folder) in enumerate(synthrad_train_folders): #+ synthrad_validation_folders:
        if i % 10 == 0:
            print(i, end = ', ')
            stdout.flush()
        if folder.find('overview') == -1:
            folder_name = folder[folder.rfind('/')+1:]
            if file_type == 'nii':
                mri_nii_file = nib.load(folder + '/' + mri_fn)
                ct_nii_file = nib.load(folder + '/' + ct_fn)
                paired_files.append([folder_name, mri_nii_file.get_fdata(), ct_nii_file.get_fdata()])
            if file_type == 'npy':
                mri_nii_file = np.load(folder + '/' + mri_fn)
                ct_nii_file = np.load(folder + '/' + ct_fn)
                paired_files.append([folder_name, mri_nii_file, ct_nii_file])
    print()
    return paired_files


# get range for each image
def get_folder_ranges(filename):
    file = open(filename, 'r')
    ranges_str = file.read()
    ranges_str_list = ranges_str.split('\n')
    ranges_list = []
    print("Getting pixel ranges:", end = ' ')
    for (i, line) in enumerate(ranges_str_list[:-2]):
        if i % 10 == 0:
            print(i, end = ', ')
        open_bracket_1 = line.find('[')
        colon_1 = line.find(':', open_bracket_1)
        close_bracket_1 = line.find(']', colon_1)
        open_bracket_2 = line.find('[', close_bracket_1)
        colon_2 = line.find(':', open_bracket_2)
        close_bracket_2 = line.find(']', colon_2)

        min_num_mri = float(line[open_bracket_1+1:colon_1])
        max_num_mri = float(line[colon_1+1:close_bracket_1])
        min_num_ct = float(line[open_bracket_2+1:colon_2])
        max_num_ct = float(line[colon_2+1:close_bracket_2])
        ranges_list.append([min_num_mri, max_num_mri, min_num_ct, max_num_ct])
    print()
    return ranges_list

# normalize data to be between -1 and 1
def normalize(data, min_num, max_num):
    return (data - min_num) / (max_num - min_num) * 2 - 1

def normalize_dataset(dataset, ranges):
    print("Normalizing dataset:", end = ' ')
    for i in range(len(dataset)):
        if i % 10 == 0:
            print(i, end = ', ')
        # print(f"normalizing {dataset[i][0]}")
        # print(f"mri min: {ranges[i][0]}, mri max: {ranges[i][1]}, ct min: {ranges[i][2]}, ct max: {ranges[i][3]}")
        dataset[i][1] = normalize(dataset[i][1], ranges[i][0], ranges[i][1])
        dataset[i][2] = normalize(dataset[i][2], ranges[i][2], ranges[i][3])
    print()

def save_dataset(dataset, desc):
    print(f"Saving dataset {desc}:", end = ' ')
    for i in range(len(dataset)):
        if i % 10 == 0:
            print(i, end = ', ')
        os.makedirs(os.path.join('/home/colter/hdd6_colter/synthrad_train_np', dataset[i][0]), exist_ok=True)
        np.save(f'/home/colter/hdd6_colter/synthrad_train_np/{dataset[i][0]}/mri_{desc}.npy', dataset[i][1])
        np.save(f'/home/colter/hdd6_colter/synthrad_train_np/{dataset[i][0]}/ct_{desc}.npy', dataset[i][2])
    print()

def get_middle_n(data, num, gap):
    length = (num - 1) * gap + 1
    bottom = data.shape[0] // 2 - length // 2
    top = bottom + length
    print(f"\t\tnum = {num}, gap = {gap}, {data.shape[0]} slices: selecting {range(bottom, top, gap) } ")
    return data[bottom:top:gap, :, :, :]

def concat_middle_ns(paired_files, num = 35, gap = 1):
    mri_concat = np.zeros((0, 1, 256, 256))
    ct_concat = np.zeros((0, 1, 256, 256))
    # print(mri_concat.shape)
    # print(ct_concat.shape)
    for i in range(len(paired_files)):
        if i % 5 == 0:
            print(i, end = ', ')
        stdout.flush()
        # print(paired_files[i][1].shape)
        # print(paired_files[i][2].shape)
        # print(get_middle_n(paired_files[i][1], n).shape)
        # print(get_middle_n(paired_files[i][2], n).shape)
        mri_concat = np.concatenate((mri_concat, get_middle_n(paired_files[i][1], num = num, gap = gap)), axis = 0)
        ct_concat = np.concatenate((ct_concat, get_middle_n(paired_files[i][2], num = num, gap = gap)), axis = 0)
    return mri_concat, ct_concat
