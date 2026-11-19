import math
import os
from enum import Enum
from cv2 import IMREAD_UNCHANGED, imread, imwrite
from numpy import uint8, zeros
from image_rotation import rotate, set_dtype

class State(Enum):
  BASE = 0
  READING_IMAGES = 1
  PROCESSING_IMAGES = 2
  RECEIVING_TRANSFORMATIONS = 3
  RECEIVING_TRANSFORM_DETAILS = 4
  COMPLETED_TRANSFORMATIONS = 5


def grayscale_circle(image, radius, center_x, center_y):  # the values being passed in for parameters are strings 
                                                          # and will be converted accordingly
  radius = int(radius)
  center_x = int(center_x)
  center_y = int(center_y)
  img_dtype = image.dtype

  print("grayscaling circle")
  out = zeros(image.shape, image.dtype)
  for x in range(image.shape[1]):
    for y in range(image.shape[0]):
      if (x - center_x) ** 2 + (y - center_y) ** 2 > radius ** 2:
        out[y][x] = image[y][x]
      else:
        out[y][x] = set_dtype((int(image[y][x][0]) + int(image[y][x][1]) + int(image[y][x][2])) // 3, img_dtype)
  return out

def crop(image, start_x, end_x, start_y, end_y):
  start_x = int(start_x)
  end_x = int(end_x)
  start_y = int(start_y)
  end_y = int(end_y)

  print("cropping")
  return image[start_y:end_y, start_x:end_x]

def save_image(image, image_name, output_directory):
  print(f"saving image {image_name} to {output_directory}")
  output_name = os.path.join(str(output_directory), image_name)
  imwrite(output_name, image)

SHAPE_FUNCTIONS = {
  "rotate": rotate,
  "grayscale_circle": grayscale_circle,
  "crop": crop,
  "save": save_image
}

SHAPE_FUNCTION_PARAMETERS = { # this is used to define which parameters are needed for each transformation 
                              # and what types the input should be coerced into
  "rotate": ["angle", "type"],
  "grayscale_circle": ["radius", "center_x", "center_y"],
  "crop": ["start_x", "end_x", "start_y", "end_y"],
  "save": ["image_name"]
}

def process_import_file(input_file_name, output_directory):
  input_file = open(input_file_name, "r")
  state = State.BASE

  line_num = 0
  image_index = -1
  starting_transformation = True
  parameter_index = -1
  for line in input_file:
    line = line.strip()
    line_num += 1
    print(f"line {line_num}: {line}, state: {state}")
    if line == "completed":
      state = State.COMPLETED_TRANSFORMATIONS
      return
    match state:
      case State.BASE:
        state = State.READING_IMAGES
        image_names = []
        images = []
      case State.READING_IMAGES:
        if check_reading_images_line_validity_and_return_continue(line, line_num):
          state = State.PROCESSING_IMAGES
        else:
          image_names.append(line[2:])
      case State.PROCESSING_IMAGES:
        image_index += 1
        check_processing_images_line_validity(line, line_num, image_index, image_names)
        images.append(imread(image_names[image_index], IMREAD_UNCHANGED))
        state = State.RECEIVING_TRANSFORMATIONS
      case State.RECEIVING_TRANSFORMATIONS:
        if line.startswith("- "):
          state = State.PROCESSING_IMAGES
        if not line.startswith("-- "):
          raise ValueError(f"Error on line {line_num}: line should be a transformation name that starts with \'-- \' but instead is \'{line}\'; state is RECEIVING_TRANSFORMATIONS")
        transformation = line[3:-1]
        if transformation not in SHAPE_FUNCTIONS:
          raise ValueError(f"Error on line {line_num}: transformation \'{transformation}\' is not a valid transformation; state is RECEIVING_TRANSFORMATIONS")
        parameters = SHAPE_FUNCTION_PARAMETERS[transformation]
        starting_transformation = True
        state = State.RECEIVING_TRANSFORM_DETAILS
      case State.RECEIVING_TRANSFORM_DETAILS:
        if starting_transformation:
          transformation_parameters = []
          parameter_index = 0
          starting_transformation = False
        if not line.startswith("--- "):
          raise ValueError(f"Error on line {line_num}: line should be a transformation parameter that starts with \'--- \' but instead is \'{line}\'; state is RECEIVING_TRANSFORM_DETAILS")
        parameter = line[4:].split()
        if parameter[0] != parameters[parameter_index]:
          raise ValueError(f"Error on line {line_num}: parameter name \'{parameter[0]}\' does not match expected parameter name \'{parameters[parameter_index]}\' for transformation \'{transformation}\'; state is RECEIVING_TRANSFORM_DETAILS")
        transformation_parameters.append(parameter[1])
        parameter_index += 1
        if parameter_index >= len(parameters):
          print(f"completing transformation {transformation} with parameters {transformation_parameters}")
          # call transformation function with parameters
          if transformation == "save":
            save_image(images[image_index], transformation_parameters[0], output_directory)
            state = State.PROCESSING_IMAGES
          else:
            function_to_call = SHAPE_FUNCTIONS[transformation]
            images[image_index] = function_to_call(images[image_index], *transformation_parameters)
            state = State.RECEIVING_TRANSFORMATIONS
      case State.COMPLETED_TRANSFORMATIONS:
        print("completed transformations")

def check_reading_images_line_validity_and_return_continue(line, line_num) -> bool:
  if line == "image transforms:":
    print("finished reading images")
    return True # If we have reached the end of the image list, it sends signal to change state
  if not line.startswith("- "):
    raise ValueError(f"Error on line {line_num}: line should be an image name that starts with '- ' but instead is \'{line}\'; state is READING_IMAGES")
  return False
  
def check_processing_images_line_validity(line, line_num, image_index, images):
  if not line.startswith("- "):
    raise ValueError(f"Error on line {line_num}: line should be an image name that starts with '- ' but instead is \'{line}\'; state is PROCESSING_IMAGES")
  if not line[2:-1] == images[image_index]:
    raise ValueError(f"Error on line {line_num}: line image name does not match image name from list. Line image name: {line[2:-1]}, list image name: {images[image_index]}")

