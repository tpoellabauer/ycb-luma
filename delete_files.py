import os
import csv

base_path = "YCB/out"

# Import and process CSV Data
with open('csv/files_to_delete.csv', newline='') as csvfile:
    data_csv = csv.reader(csvfile, delimiter=';', quotechar='|')
    headers = next(data_csv)

    # Indices in data_csv=
    # 0: directory
    # 1: vid_id
    # 2: from
    # 3: to
    for row in data_csv:
        if row[0] == "":
            continue
        path = os.path.join(base_path, row[0])
        # If it removes multiple files
        if row[3] and int(row[3]) > 0:
            for i in range(int(row[2]), int(row[3])+1, 3):
                filename_mask = f"{row[1]}_frame_{i}.png"
                filename_rgb = f"{row[1]}_frame_{i}.jpg"
                mask_path = os.path.join(path, "masks", filename_mask)
                rgb_path = os.path.join(path, "rgb", filename_rgb)
                if os.path.exists(mask_path) and os.path.exists(rgb_path):
                    os.remove(mask_path)
                    os.remove(rgb_path)
                    print(f"{mask_path} and its rgb removed!")

        # For individual files
        else:
            filename_mask = f"{row[1]}_frame_{row[2]}.png"
            filename_rgb = f"{row[1]}_frame_{row[2]}.jpg"
            mask_path = os.path.join(path, "masks", filename_mask)
            rgb_path = os.path.join(path, "rgb", filename_rgb)
            if os.path.exists(mask_path) and os.path.exists(rgb_path):
                os.remove(mask_path)
                os.remove(rgb_path)
                print(f"{mask_path} and its rgb removed!")

