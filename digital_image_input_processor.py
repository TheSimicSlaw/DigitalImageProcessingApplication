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

  for line in input_file:
    print(line)
