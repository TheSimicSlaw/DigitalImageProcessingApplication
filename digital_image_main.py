from dip_imports import *

def main():
  parser = ArgumentParser # input text file to read instructions from, output folder of images to create

  parser.add_argument("-f", "--input_file", dest="input_file", help="enter the name of the instructions file")
  parser.add_argument("-o", "--output_folder", dest="output_folder")

  args = parser.parse_args

  parent_dir = Path(__file__).resolve().parent
  arg_dir = parent_dir / args.output_folder

  try:
    os.makedirs(arg_dir, exist_ok=True)
    print("Successfully created directory {arg_dir}")
  except OSError as e:
    print("Error creating directory {arg_dir}: {e}")
  