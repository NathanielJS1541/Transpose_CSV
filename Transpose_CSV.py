from csv import reader, writer
import argparse
from os import path, mkdir, makedirs

# Constants
DEFAULT_TEMPLATE = "{input_path}\\{input_filename}_Transposed.{input_ext}"


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


# Function to construct the output filename and path from the flags specified by the user
def construct_output():
    # Separate relevant data from the input file
    input_path, input_filename = path.split(args.input_file)
    input_filename, input_ext = path.splitext(input_filename)
    input_ext = input_ext.strip('.')

    # Add verbose output if -v flag is specified
    if args.verbose:
        print(f"{OutputColours.VERBOSE}"
              f"[VERBOSE] input_path = {input_path}\n"
              f"[VERBOSE] input_filename = {input_filename}\n"
              f"[VERBOSE] input_ext = {input_ext}\n"
              f"[VERBOSE] args.output_file = {args.output_file}"
              f"{OutputColours.END}")

    # Construct the output path and filename from the output file flags provided by the user
    constructed_output = args.output_file.format(input_path=input_path,
                                                 input_filename=input_filename,
                                                 input_ext=input_ext)
    output_path, output_filename = path.split(constructed_output)
    output = path.join(output_path, output_filename)

    # Add verbose output to show the constructed output file and path
    if args.verbose:
        print(f"{OutputColours.VERBOSE}"
              f"[VERBOSE] output = {output}\n"
              f"[VERBOSE] output_path = {output_path}"
              f"{OutputColours.END}")

    # Check if output path already exists
    if not path.isdir(output_path):
        # Check if the parent directory exists
        if path.isdir(path.dirname(output_path)):
            # If the parent directory exists, we can simply create the final directory regardless of other flags
            if args.verbose:
                print(f"{OutputColours.VERBOSE}[VERBOSE] Creating Final Directory {output_path}{OutputColours.END}")
            mkdir(output_path)
        elif args.create_dir:
            # If the -c flag has been specified, we can create all parent folders in the path
            if args.verbose:
                print(f"{OutputColours.VERBOSE}[VERBOSE] Recursively Creating Path {output_path}{OutputColours.END}")
            makedirs(output_path)
        else:
            # Finally, if none of that could be done we must thrown an error as the output path will not exist.
            raise SystemExit(f"{OutputColours.ERROR}[ERR] The specified output path was not found and couldn't "
                             f"be created. Either create it manually or try specifying the {OutputColours.BOLD}"
                             f"-c flag.{OutputColours.END}")

    return output


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
parser.add_argument("-c", "--create-dir", help="If the complete path to the specified output file doesn't exist already"
                                               f",\ncreate the folders specified recursively to create a valid path.\n"
                                               f"If the parent of the specified output folder does exist,\n"
                                               f"-c is not necessary and the final folder will be created anyway.",
                    action="store_true")
parser.add_argument("-v", "--verbose", help="Adds more verbosity to outputs for debugging.", action="store_true")
args = parser.parse_args()

# Input validation
if args.input_file:
    # Check that the input file specified actually exists, if it doesn't raise an error.
    if not path.isfile(args.input_file):
        raise SystemExit(f"{OutputColours.ERROR}[ERR] The input file specified does not exist or is not a file."
                         f"{OutputColours.END}")
if not args.output_file:
    # If no output template has been specified, use the default (stored in DEFAULT_TEMPLATE)
    args.output_file = DEFAULT_TEMPLATE
    print(f"{OutputColours.INFO}[INFO] Outputting to input directory using default template: {DEFAULT_TEMPLATE}"
          f"{OutputColours.END}")

# Open the file and transpose it using zip()
inputCSV = zip(*reader(open(args.input_file), delimiter=','))
# Construct the output file name and path from the input arguments
output_file = construct_output()
# Check if the desired output file already exists
if path.isfile(output_file) and not args.force_overwrite:
    # If it does exist and --force-overwrite has not been specified, print an error message and exit the program without
    # writing anything. User must explicitly state they wish the file to be overwritten.
    raise SystemExit(f"{OutputColours.ERROR}[ERR] The output file already exists and --force-overwrite has not been "
                     f"specified.{OutputColours.END}")
else:
    # If --force-overwrite was specified and the file exists, just warn that the file will be overwritten. Too late
    # now...
    if path.isfile(output_file) and args.force_overwrite:
        print(f"{OutputColours.WARNING}[WARN] The existing file {output_file} will be overwritten."
              f"{OutputColours.END}")
    # Save the file to the output
    writer(open(output_file, 'w', newline='')).writerows(inputCSV)
    # Display some output to indicate success
    print(f"{OutputColours.INFO}[INFO] Output saved to: {output_file}{OutputColours.END}")
