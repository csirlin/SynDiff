from utils_colter import *
# testing_resize()

# load the dataset and save the image components
dataset = get_dataset('/home/colter/hdd6_colter/synthrad/train/Task1/brain/*')
save_dataset(dataset, 'orig')

# normalize the data to be within the range [-1, 1]
ranges = get_folder_ranges('ranges_sorted.txt')
normalize_dataset(dataset, ranges)
save_dataset(dataset, 'normalized')

# resize to 256x256 and reorganized
resize_dataset(dataset)
save_dataset(dataset, 'normsized')
