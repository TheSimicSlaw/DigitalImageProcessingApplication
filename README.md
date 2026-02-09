# DigitalImageProcessingApplication
This is an application that takes an instructions file and set of images and reads instructions from the file on how to alter the entered images. The file should be structured as such:

START_FILE
images:
- image1.jpg
- image2.jpg
- image3.jpg
image transforms:
- image1.jpg:
-- grayscale_circle:
--- radius 100
--- center 150, 120
-- return:
--- image1_gray_circled
- image2.jgp:
-- rotate:
--- angle 3
--- type nearest_neighbor_interpolation
--- rescaled original_dimensions
-- crop:
--- start_x 20
--- start_y 40
--- end_x 180
--- end_y 160
-- return:
--- image2_rotated_and_cropped
- image3.jpg:
-- return:
---image3_unchanged
completed
END_FILE
