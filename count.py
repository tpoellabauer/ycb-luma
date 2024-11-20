import os
from PIL import Image

import csv

# Specify the input and output paths
dataset_name = "YCB"
output_folder = "csv"

# Counts how files are available on a folder
def count_list(base_path: str, output_type: str):
    dict_count = {}
    base_path = os.path.join(base_path, output_type)
    for directory in os.listdir(base_path):
        if output_type == "in":
            path = os.path.join(base_path, directory)
        else:
            path = os.path.join(base_path, directory, "masks") # Or RGB
        files_count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

        # Outputs the count based on its data_id
        data_id = directory.split("_")[0]
        if data_id in dict_count:
            dict_count[data_id] += files_count
        else:
            dict_count[data_id] = files_count

    # Sort the list
    return dict_count


# Write the list to .txt
def write_to_txt(fname, list_count):
    with open(os.path.join(output_folder, fname), 'w') as file:
        for item in list_count:
            file.write(str(item) + '\n')


# Write the list to .csv
def write_to_csv(fname, count):
    with open(os.path.join(output_folder, fname), 'w', newline='') as file:
        if type(count) is list:
            csv.writer(file, delimiter=";").writerows(count)
        elif type(count) is dict:
            for key, value in count.items():
                data = [int(key), int(value)]
                csv.writer(file, delimiter=";").writerow(data)


# Counts how many input videos are available each object
input_count = count_list(dataset_name, "in")

# Counts how many masks are generated each object
output_count = count_list(dataset_name, "out")

# Save list
#write_to_txt('count_inputs.txt', input_count)
write_to_csv('count_inputs.csv', input_count)
print(f"Input count from directory '{dataset_name}/in/' extracted to Documents/count_inputs.csv.")

#write_to_txt('count_masks.txt', output_count)
write_to_csv('count_outputs.csv', output_count)
print(f"Mask count from directory '{dataset_name}/out/' extracted to Documents/count_outputs.csv.")


# PAST CODES THAT ARE NOT USED ANYMORE / IRRELEVANT WITH NEWER CODES


# # Counts file in which has 512x512 resolution
# def count_masks_min_resolution(base_path):
#     list_count = []
#     base_path = os.path.join(base_path, "out")
#     for directory in os.listdir(base_path):
#         path = os.path.join(base_path, directory, "masks")  # Or RGB
#         images_name = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#         images_res_count = 0
#         # loop for each image
#         for img_name in images_name:
#             # Open the image file
#             img = Image.open(os.path.join(path, img_name))
#             # Get image resolution
#             width, height = img.size
#             if width >= 512 and height >= 512:
#                 images_res_count += 1
#         print((directory, images_res_count))
#         list_count.append((directory, images_res_count))
#
#     # Sort the list
#     return sorted(list_count, key=lambda t: t[0])
#
#
# # Counts how many count files differs
# def count_masks_differ(base_path, output_type="out"):
#     list_count = []
#     base_path = os.path.join(base_path, output_type)
#     for directory in os.listdir(base_path):
#         mask_path = os.path.join(base_path, directory, "masks")
#         rgb_path = os.path.join(base_path, directory, "rgb")
#         mask_files = [f for f in os.listdir(mask_path) if os.path.isfile(os.path.join(mask_path, f))]
#         rgb_files = [f for f in os.listdir(rgb_path) if os.path.isfile(os.path.join(rgb_path, f))]
#         if len(mask_files) != len(rgb_files):
#             # tell which files are missing
#             list_difference = set(rgb_files) - set(mask_files)
#             # Outputs the difference
#             list_count.append([directory, sorted(list_difference)])
#     # Sort the list
#     return sorted(list_count, key=lambda t: t[0])
#


#masks_min_res = count_masks_min_resolution(dataset_name)
#write_to_txt('masks_min_res.txt', masks_min_res)
#print(f"Input masks_min_res from directory '{dataset_name}/out/' extracted.")


# Counts how many objects differs in numbers between masks and rgb
# count_md = count_masks_differ(dataset_name)
# write_to_csv('count_temp.csv', count_md)
# print(f"Mask count from directory '{dataset_name}/out/' extracted to Documents/count_outputs.csv.")
