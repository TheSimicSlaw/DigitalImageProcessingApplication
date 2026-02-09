from dip_imports import *

def main():
  parser = ArgumentParser # input text file to read instructions from, output folder of images to create

  parser.add_argument("-f", "--input_file", dest="input_file", help="enter the name of the instructions file")
  parser.add_argument("-o", "--output_folder", dest="output_folder")

  args = parser.parse_args
  args_valid_check(args)

  set_directory(args.output_folder)

  

def set_directory(output_folder_name):
  parent_dir = Path(__file__).resolve().parent
  arg_dir = parent_dir / output_folder_name

  try:
    os.makedirs(arg_dir, exist_ok=True)
    print("Successfully created directory {arg_dir}")
  except OSError as e:
    print("Error creating directory {arg_dir}: {e}")

def args_valid_check(args):
  if args.input_file == None:
    raise WindowsError("input_file is missing. Please enter one and start again")
  if args.output_folder == None:
    raise WindowsError("output_folder is missing")

  