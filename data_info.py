# get basic info about the MRI and CT scans in the synthrad dataset
# scan shapes and pixel intensity ranges

import nibabel as nib
import glob
import time

# find the minimum and maximum pixel values in a single patient scan (MRI or CT)
def get_range_of_ndarr(data):
    min_num = 1e9
    max_num = -1e9

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                min_num = min(min_num, data[i][j][k])
                max_num = max(max_num, data[i][j][k])
    return min_num, max_num


# find the minimum and maximum pixel values in a dataset containing paired MRI
# and CT scans
def get_info(dataset):
    tot_min_mri = 1e9
    tot_max_mri = -1e9
    tot_min_ct = 1e9
    tot_max_ct = -1e9
    mins_mri = []
    maxs_mri = []
    mins_ct = []
    maxs_ct = []
    file = open('ranges.txt', 'w')

    for i in range(len(dataset)):
        t = time.time()
        folder, mri, ct = dataset[i]
        mri = mri.get_fdata()
        ct = ct.get_fdata()

        # get basic info about program progress and shape of each scan
        file.write(f"{i}/{len(dataset):} - {folder}: MRI shape: {mri.shape}, CT shape: {ct.shape} ")
        
        # get pixel range for the MRI and CT scan for a given patient
        local_min_mri, local_max_mri = get_range_of_ndarr(mri)
        local_min_ct, local_max_ct = get_range_of_ndarr(ct)

        # append the per-scan min/max and update the total min/max
        mins_mri.append(local_min_mri)
        maxs_mri.append(local_max_mri)
        mins_ct.append(local_min_ct)
        maxs_ct.append(local_max_ct)
        tot_min_mri = min(tot_min_mri, local_min_mri)
        tot_max_mri = max(tot_max_mri, local_max_mri)
        tot_min_ct = min(tot_min_ct, local_min_ct)
        tot_max_ct = max(tot_max_ct, local_max_ct)

        # write the per-scan min/max to the file and include timing info
        file.write(f'MRI range: [{local_min_mri}:{local_max_mri}], CT range: [{local_min_ct}:{local_max_ct}] ({time.time() - t}s)\n')
        print(f"Done with {i} out of {len(dataset)} ({time.time() - t}s elapsed)")

    # write the total min/max to the file
    file.write(f'Total ranges: MRI: [{tot_min_mri}:{tot_max_mri}], CT: [{tot_min_ct}:{tot_max_ct}]\n')
    file.close()


# initial testing
# mri = nib.load('/home/colter/hdd6_colter/synthrad/train/Task1/brain/1BA001/mr.nii.gz')
# ct = nib.load('/home/colter/hdd6_colter/synthrad/train/Task1/brain/1BA001/ct.nii.gz')
# get_info(mri.get_fdata())
# get_info(ct.get_fdata())

# load the MRI/CT scans from training data
# validation only has MR because CT is a hidden test case for the synthrad competition 
synthrad_train_folders = sorted(glob.glob('/home/colter/hdd6_colter/synthrad/train/Task1/brain/*'))
# synthrad_validation_folders = sorted(glob.glob('/home/colter/hdd6_colter/synthrad/validation/Task1/brain/*'))

print(synthrad_train_folders)
# print(synthrad_validation_folders)

# add the MRI/CT pairs to a list of (folder name, MRI, CT) tuples
paired_files = []
for folder in synthrad_train_folders: #+ synthrad_validation_folders:
    if folder.find('overview') == -1:
        folder_name = folder[folder.rfind('/')+1:]
        mri_nii_file = nib.load(folder + '/mr.nii.gz')
        ct_nii_file = nib.load(folder + '/ct.nii.gz')
        paired_files.append((folder_name, mri_nii_file, ct_nii_file))

# print(len(paired_files))

# get scan shapes and intensity ranges for each MRI/CT pair
# get_info(paired_files)
