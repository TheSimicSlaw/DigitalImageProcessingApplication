from argparse import ArgumentParser
import os
from pathlib import Path
from digital_image_input_processor import process_import_file

def main():
  print("running main")
  parser = ArgumentParser() # args are an input text file to read instructions from & anoutput folder of images to create

  parser.add_argument("-f", "--input_file", dest="input_file", help="enter the name of the instructions file") 
  parser.add_argument("-o", "--output_folder", dest="output_folder")

  args = parser.parse_args()
  print("args parsed")
  args_valid_check(args)

  dir = set_directory(args.output_folder)

  process_import_file(args.input_file, dir)



def set_directory(output_folder_name):
  parent_dir = Path(__file__).resolve().parent
  arg_dir = parent_dir / output_folder_name

  try:
    os.makedirs(arg_dir, exist_ok=True)
    print("Successfully created directory {arg_dir}")
  except OSError as e:
    print("Error creating directory {arg_dir}: {e}")

  return arg_dir

def args_valid_check(args):
  if args.input_file == None:
    print("input_file is missing. Please enter one and start again")
    raise WindowsError("input_file is missing. Please enter one and start again")
  if args.output_folder == None:
    print("output_folder is missing")
    raise WindowsError("output_folder is missing")


if __name__ == "__main__":  
  main()
  