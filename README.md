# Transpose_CSV

This is a simple python script to transpose a .csv file; that is, turn the rows into columns and the columns into rows. This can be useful for preparing data for programs such as MATLAB which expect .csv data to be in a specific orientation.

## Requirements

- **Python 3.6+**:  This is required as the script relies on f-strings, which were introduced in Python 3.6.
- **csv**, **argparse**, and **os** libraries:     These are used to import and export the .csv files, and are (as far as I'm aware) included as standard with most Python installations.

## How to Run

The preferred method to run the script is to use python to run `Transpose_CSV.py` from the command line. Alternatively, there is an .exe file included in the [latest release](https://github.com/NathanielJS1541/Transpose_CSV/releases/latest). This can be run from the command line without using python: `Transpose_CSV.exe`.

## Help Output

```helpfile
usage: Transpose_CSV.py [-h] -i INPUT_FILE [-o OUTPUT_FILE] [-f] [-c] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The input file name or path you wish to transpose.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file name or path, in 'new Style' Python String Formatting.
                        Possible flags are: {input_path}, {input_filename}, {input_ext}
                        Default: {input_path}\{input_filename}_Transposed.{input_ext}
  -f, --force-overwrite
                        If there already exists a file with the desired output path and
                        file name, overwrite it.WARNING: May cause data loss
  -c, --create-dir      If the complete path to the specified output file doesn't exist already,
                        create the folders specified recursively to create a valid path.
                        If the parent of the specified output folder does exist,
                        -c is not necessary and the final folder will be created anyway.
  -v, --verbose         Adds more verbosity to outputs for debugging.
```

## Example Usage

- The most basic usage would be to offer a single input using `python .\Transpose_CSV.py -i .\INPUT_FILE.csv`. This would save the output to `.\INPUT_FILE_transposed.csv`. If you are running the .exe file that would look like: `Transpose_CSV.exe -i .\INPUT_FILE.csv`
- You can also specify where the output should be sent to using `-o`: `python .\Transpose_CSV.py -i .\INPUT_FILE.csv -o C:\Users\John\MyNewFile.{input_ext}` would save the file to the specified path and name, but keep whatever extension it found on the input. The most useful flags are `{input_path} and {input_filename}`, since the script is designed for .csv files.
- You can place flags between specified parts of the filename like so: `python .\Transpose_CSV.py -i .\INPUT_FILE.csv -o {input_path}\My_New_{input_filename}.csv`
