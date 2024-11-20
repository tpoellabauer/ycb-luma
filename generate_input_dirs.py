import os
import csv

dataset_name = "YCB"

# Reads data.csv and parse them into a dictionary
data = {}
with open('csv/data.csv', newline='') as csvfile:
    data_csv = csv.reader(csvfile, delimiter=';', quotechar='|')
    headers = next(data_csv)
    for row in data_csv:
        data[row[0]] = {
            "name": row[1],
            "variations": int(row[2]),
            "different": True if row[3].lower() == "true" else False,
            "rigid": True if row[4].lower() == "true" else False,
            "brightness_threshold": int(row[5])
        }

# Define the path
output_folder = dataset_name+"/in/"
dir_list = []

# Generate the folders if doesn't exist
for data_id in data.keys():
    num_of_vars = data[data_id]["variations"]

    # Differentiate naming for object with multiple shape/colors (variability)
    if num_of_vars == 1:
        path_name = data_id + "_" + data[data_id]["name"].lower().replace(" ", "_")
        path = os.path.join(output_folder, path_name)
        dir_list.append(path)
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        for i in range(num_of_vars):
            path_name = data_id + "_" + str(i + 1) + "_" + data[data_id]["name"].lower().replace(" ", "_")
            path = os.path.join(output_folder, path_name)
            dir_list.append(path)
            if not os.path.exists(path):
                os.makedirs(path)

print("Input dirs from data.csv generated!")
