from csv import reader, writer
import argparse
from pathlib import Path

# Constants
DEFAULT_TEMPLATE = "{input_path}\\{input_filename}_transposed.{input_ext}"


# Colours for output to terminal (Blender Style)
class OutputColours:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    VERBOSE = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Get Input Arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-i", "--input-file", help="The input file name or path you wish to transpose.",
                    type=str, required=True)
parser.add_argument("-o", "--output-file", help="Output file name or path, in 'new Style' Python String Formatting.\n"
                                                f"Possible flags are: {OutputColours.INFO}"
                                                "{input_path}, {input_filename}, {input_ext}\n"
                                                f"{OutputColours.BLUE}Default: {DEFAULT_TEMPLATE}{OutputColours.END}")
parser.add_argument("-f", "--force-overwrite", help="If there already exists a file with the desired output path and \n"
                                                    f"file name, overwrite it.{OutputColours.BOLD}"
                                                    f"{OutputColours.WARNING}WARNING: May cause data loss"
                                                    f"{OutputColours.END}", action="store_true")
parser.add_argument("-v", "--verbose", help="Adds more verbosity to outputs for debugging.", action="store_true")
args = parser.parse_args()

# Input validation
if args.input_file:
    if not Path(args.input_file).exists():
        raise FileNotFoundError(f"{OutputColours.ERROR}[ERR] The input file specified does not exist."
                                f"{OutputColours.END}")
if not args.output_file:
    # If no output template has been specified, use the default
    args.output_file = DEFAULT_TEMPLATE
    print(f"{OutputColours.INFO}[INFO] Outputting to input directory using default template: {DEFAULT_TEMPLATE}"
          f"{OutputColours.END}")


# Function to construct the output filename from the flags
def construct_output():
    # Separate relevant data from the input file
    input_path = args.input_file.split('\\')
    input_filename = input_path[-1]
    input_path = Path('\\'.join(input_path[0:len(input_path) - 1]))
    input_filename = input_filename.split('.')
    input_ext = input_filename[-1]
    input_filename = input_filename[0]

    # Add verbose output
    if args.verbose:
        print(f"{OutputColours.VERBOSE}"
              f"[VERBOSE] input_path = {input_path}\n"
              f"[VERBOSE] input_filename = {input_filename}\n"
              f"[VERBOSE] input_ext = {input_ext}\n"
              f"[VERBOSE] args.output_file = {args.output_file}"
              f"{OutputColours.END}")

    # Construct the output path and filename
    output = args.output_file.format(input_path=input_path, input_filename=input_filename, input_ext=input_ext)
    output_path = output.split('\\')
    output_path = Path('\\'.join(output_path[0:len(output_path) - 1]))

    # Add verbose output
    if args.verbose:
        print(f"{OutputColours.VERBOSE}"
              f"[VERBOSE] output = {output}\n"
              f"[VERBOSE] output_path = {output_path}"
              f"{OutputColours.END}")

    # Check if output path already exists, make it if not
    if not output_path.is_dir():
        if args.verbose:
            print(f"{OutputColours.VERBOSE}[VERBOSE] Creating Directory {output_path}{OutputColours.END}")
        output_path.mkdir(parents=True)

    return output


# Open the file
inputCSV = zip(*reader(open(args.input_file), delimiter=','))
# Construct the output file from arguments
output_file = construct_output()
# Check if the desired output file already exists and --force-overwrite has not been specified
if Path(output_file).is_file() and not args.force_overwrite:
    print(f"{OutputColours.ERROR}[ERR] The output file already exists and --force-overwrite has not been specified."
          f"{OutputColours.END}")
else:
    if Path(output_file).is_file() and args.force_overwrite:
        print(f"{OutputColours.WARNING}[WARN] The existing file {output_file} will be overwritten."
              f"{OutputColours.END}")
    # Transpose the file and save it
    writer(open(output_file, 'w', newline='')).writerows(inputCSV)
    # Display some output
    print(f"{OutputColours.INFO}[INFO] Output saved to: {output_file}{OutputColours.END}")
