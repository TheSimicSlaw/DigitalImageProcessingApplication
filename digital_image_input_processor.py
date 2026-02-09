from dip_imports import *

class State(Enum):
  BASE = 0
  READING_IMAGES = 1
  PROCESSING_IMAGES = 2
  RECEIVING_TRANSFORMATIONS = 3
  RECEIVING_TRANSFORM_DETAILS = 4
  COMPLETED_TRANSFORMATIONS = 5


def process_import_file(input_file_name):
  input_file = open(input_file_name, "r")
  state = State.BASE

  line_num = 0
  image_index = -1
  for line in input_file:
    line_num += 1
    match state:
      case State.BASE:
        print(line)
        state = State.READING_IMAGES
        images = []
      case State.READING_IMAGES:
        if line == "image transforms:":
          state = State.PROCESSING_IMAGES
          continue
        if not line.startswith("- "):
          raise ValueError(f"Error on line {line_num}: line should be an image name that starts with \'- \' but instead is \'{line}\'; state is READING_IMAGES")
        images.append(line[2:])
      case State.PROCESSING_IMAGES:
        if not line.startswith("- "):
          raise ValueError(f"Error on line {line_num}: line should be an image name that starts with \'- \' but instead is \'{line}\'; state is PROCESSING_IMAGES")
        image_index += 1
        if not line[3:-1] == images[image_index]:
          raise ValueError(f"Error on line {line_num}: line image name does not match image name from list. Line image name: {line[3:-1]}, list image name: {images[image_index]}")
        # assign image
        state = State.PROCESSING_IMAGES
      case State.RECEIVING_TRANSFORMATIONS:
        if not line.startswith("-- "):
          raise ValueError(f"Error on line {line_num}: line should be a transformation name that starts with \'-- \' but instead is \'{line}\'; state is RECIEVING_TRANSFORMATIONS")
        transformation = line[4:-1]


