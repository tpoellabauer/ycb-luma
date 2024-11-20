import os
import numpy as np
import cv2

import csv

every_nth_frame = 3


def make_square(image):
    # Determine the size of the original image

    height, width = image.shape[:2]

    # Calculate the size of the square canvas

    size = max(width, height)

    # Create an empty square image with white background

    square_image = np.zeros((size, size, 3), dtype=np.uint8) * 255

    # Calculate the position to place the original image in the square canvas

    x = (size - width) // 2

    y = (size - height) // 2

    # Paste the original image onto the square canvas

    square_image[y:y + height, x:x + width] = image

    return square_image


def generate_masks(input_path, output_path, brightness_threshold, min_area_threshold=1000):
    # Get a list of all video files in the input folder
    video_files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

    # Creates file that maps index to its corresponding input video
    with open(os.path.join(output_path, "input_videos.csv"), 'w', newline='') as newfile:
        vid_files_enum = [[i, f] for i, f in enumerate(video_files)]
        csv.writer(newfile, delimiter=";").writerows(vid_files_enum)

    # Save video names with its index
    # with open("video_files.txt", 'w') as f:
    #     for vid_idx, video_file in video_files:
    #         file.write(str((vid_idx, video_file)) + '\n')

    # Process each video file
    for v_idx, video_file in enumerate(video_files):
        print("Currently processing " + video_file + " in " + input_path)

        # Open the video file
        video_path = os.path.join(input_path, video_file)
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create the output folders for the current video file
        video_mask_folder = os.path.join(output_path, "masks")
        if not os.path.exists(video_mask_folder):
            os.makedirs(video_mask_folder)

        video_rgb_folder = os.path.join(output_path, "rgb")
        if not os.path.exists(video_rgb_folder):
            os.makedirs(video_rgb_folder)

        # Process each frame of the video
        for frame_index in range(frame_count):
            # Read the current frame
            ret, frame = cap.read()

            # Process every nth frame
            if frame_index % every_nth_frame == 0:
                # make image square
                frame = make_square(frame)

                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Threshold the grayscale frame to create a binary mask
                ret, mask = cv2.threshold(gray, brightness_threshold, 255, cv2.THRESH_BINARY)

                # Filter out small areas in the mask
                filtered_mask = np.copy(mask)
                contours, _ = cv2.findContours(filtered_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Sort contours by area in descending order
                contours = sorted(contours, key=cv2.contourArea, reverse=True)

                # Get the largest contour
                largest_contour = contours[0]

                # for contour in contours:
                #     area = cv2.contourArea(contour)
                #     if area < min_area_threshold:
                #         cv2.drawContours(filtered_mask, [contour], 0, (0, 0, 0), -1)
                area = cv2.contourArea(largest_contour)
                if area > min_area_threshold:
                    cv2.drawContours(filtered_mask, [largest_contour], 0, (255, 255, 255), -1)

                    # Compute the bounding rectangle
                    x, y, w, h = cv2.boundingRect(largest_contour)

                    # Determine the square crop region
                    crop_size = max(w, h)
                    x_crop = x + (w - crop_size) // 2
                    y_crop = y + (h - crop_size) // 2
                    if x_crop <= 0 or y_crop <= 0:  # empty image
                        continue 

                    # Perform the crop
                    frame_crop = frame[y_crop:y_crop+crop_size, x_crop:x_crop+crop_size]
                    mask_crop = filtered_mask[y_crop:y_crop+crop_size, x_crop:x_crop+crop_size]

                    # Filters image if dimension lower than 512x512
                    mask_h, mask_w = mask_crop.shape
                    if mask_h < 512 or mask_w < 512:
                        continue

                    # Save the binary mask to the output folder
                    mask_filename = f"{v_idx}_frame_{frame_index}.png"
                    mask_path = os.path.join(video_mask_folder, mask_filename)
                    cv2.imwrite(mask_path, mask_crop)

                    # Save the original frame to the output folder
                    rgb_filename = f"{v_idx}_frame_{frame_index}.jpg"
                    rgb_path = os.path.join(video_rgb_folder, rgb_filename)
                    cv2.imwrite(rgb_path, frame_crop)

                    print(f"Generated binary mask and saved rgb frame for frame {frame_index} of {input_path}/{video_file}")

        # Release the video capture
        cap.release()


# Specify the input and output paths
dataset_name = "YCB"

input_path = dataset_name+"/in/"
output_path = dataset_name+"/out/"

# Import csv Data
data_csv = {}
with open('csv/data.csv', newline='') as csvfile:
    data_csv_raw = csv.reader(csvfile, delimiter=';', quotechar='|')
    headers = next(data_csv_raw)
    for row in data_csv_raw:
        data_csv[row[0]] = {
            "name": row[1],
            "variations": int(row[2]),
            "different": True if row[3].lower() == "true" else False,
            "rigid": True if row[4].lower() == "true" else False,
            "brightness_threshold": int(row[5])
        }


# Find folders with content within input directories
for directory in os.listdir(input_path):
    data_id = directory.split("_")[0]
    try:
        if os.listdir(os.path.join(input_path, directory)):

            # Create the output folder if it does not exist
            if not os.path.exists(os.path.join(output_path, directory)):
                os.makedirs(os.path.join(output_path, directory))

            # Skip folder if it already contains masks
            if not os.path.exists(os.path.join(output_path, directory, "rgb")):  # or "masks"
                generate_masks(
                    os.path.join(input_path, directory),
                    os.path.join(output_path, directory),
                    data_csv[data_id]["brightness_threshold"]
                )
    except NotADirectoryError:
        continue
