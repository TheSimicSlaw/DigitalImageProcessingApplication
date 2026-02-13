# DigitalImageProcessingApplication
This is an application that takes an instructions file and set of images and reads instructions from the file (done in sequence per image) on how to alter the entered images. The file should be structured as such:

START_FILE
images:
- image1.jpg
- image2.jpg
- image3.jpg
image transforms:
- image1.jpg:
-- grayscale_circle:
--- radius 100
--- center_x 150
--- center_y 120
-- save:
--- image_name image1_gray_circled
- image2.jgp:
-- rotate:
--- angle 3
--- type nearest_neighbor_interpolation
--- rescaled True
-- crop:
--- start_x 20
--- end_x 180
--- start_y 40
--- end_y 160
-- save:
--- image_name image2_rotated_and_cropped
- image3.jpg:
-- save:
---image_name image3_unchanged
completed
END_FILE

Available Transformation:
- grayscale_circle returns the image passed in except that all pixels within a circle of a given radius centered on the point defined by center_x and center_y have been converted to their grayscale equivalent
- rotate returns the image rotated at a certain angle (defined in radians), with the types "no_interpolation", "nearest_neighbor_interpolation," and "bilinear_interpolation" and with the options to rescale it to the original dimensions (true) or leave it at the rotated dimensions (false)
- crop returns the image cropped to rectangular dimensions specified by starting and ending x and y values
- save saves the image that has been put through the transformations to the directory specified with the name given
