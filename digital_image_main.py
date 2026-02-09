from dip_imports import *

def main():
  parser = ArgumentParser # input text file to read instructions from, output folder of images to create

  parser.add_argument("-f", "--file", dest="input_file", help="enter the name of the instructions file")
  parser.add_argument("-o", "--output_folder", dest="output_folder_name")

  args = parser.parse_args

  
  