from cv2 import line
from dip_imports import *

class State(Enum):
  BASE = 0
  READING_IMAGES = 1
  PROCESSING_IMAGES = 2
  RECEIVING_TRANSFORMATIONS = 3
  RECEIVING_TRANSFORM_DETAILS = 4
  COMPLETED_TRANSFORMATIONS = 5

def rotate(angle, type, rescaled):
  print("rotating")

def grayscale_circle(image, radius, center_x, center_y):
  print("grayscaling circle")
  out = zeros(image.shape, dtype=numpy.uint8)
  for x in range(image.shape[1]):
    for y in range(image.shape[0]):
      if (x - center_x) ** 2 + (y - center_y) ** 2 > radius ** 2:
        out[y][x] = image[y][x]
      else:
        out[y][x] = (image[y][x][0] + image[y][x][1] + image[y][x][2]) // 3

def save_image(image_name, output_directory):
  print("saving image")

SHAPE_FUNCTIONS = {
  "rotate": rotate,
  "grayscale_circle": grayscale_circle,
  "save": save_image
}

SHAPE_FUNCTION_PARAMETERS_AND_TYPES = { # this is used to define which parameters are needed for each transformation 
                                        # and what types the input should be coerced into
  "rotate": [["angle", "type", "rescaled"],
             ["float", "str", "bool"]],
  "grayscale_circle": [["radius", "center_x", "center_y"],
                       ["int", "int", "int"]],
  "save": [["image_name", "output_directory"],
           ["str", "str"]]
}

def process_import_file(input_file_name, output_directory):
  input_file = open(input_file_name, "r")
  state = State.BASE

  line_num = 0
  image_index = -1
  for line in input_file:
    line = line.strip()
    line_num += 1
    print(f"line {line_num}: {line}")
    match state:
      case State.BASE:
        print(line)
        state = State.READING_IMAGES
        image_names = []
        in_images = []
        out_images = []
      case State.READING_IMAGES:
        if check_reading_images_line_validity_and_return_continue(line, line_num):
          state = State.PROCESSING_IMAGES
        else:
          image_names.append(line[2:])
      case State.PROCESSING_IMAGES:
        image_index += 1
        check_processing_images_line_validity(line, line_num, image_index, image_names)
        in_images.append(imread(image_names[image_index]))
        state = State.RECEIVING_TRANSFORMATIONS
      case State.RECEIVING_TRANSFORMATIONS:
        if not line.startswith("-- "):
          raise ValueError(f"Error on line {line_num}: line should be a transformation name that starts with \'-- \' but instead is \'{line}\'; state is RECIEVING_TRANSFORMATIONS")
        transformation = line[3:-1]
        if transformation not in SHAPE_FUNCTIONS:
          raise ValueError(f"Error on line {line_num}: transformation \'{transformation}\' is not a valid transformation; state is RECEIVING_TRANSFORMATIONS")
        state = State.RECEIVING_TRANSFORM_DETAILS
      case State.RECEIVING_TRANSFORM_DETAILS:
        print()
      case State.COMPLETED_TRANSFORMATIONS:
        print()
    print(f"current state: {state}")

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

