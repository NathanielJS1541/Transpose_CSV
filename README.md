# Transpose_CSV

This is a simple python script to transpose a .csv file; that is, turn the rows into columns and the columns into rows. This can be useful for preparing data for programs such as MATLAB which expect .csv data to be in a specific orientation.

## Requirements

- **Python 3.6+**:  This is required as the script relies on f-strings, which were introduced in Python 3.6.
- **csv**, **argparse**, and **pathlib** libraries:     These are used to import and export the .csv files, and are (as far as I'm aware) included as standard with most Python installations.

## Help Output

```helpfile
usage: Transpose_CSV.py [-h] -i INPUT_FILE [-o OUTPUT_FILE] [-f] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The input file name or path you wish to transpose.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file name or path, in 'new Style' Python String Formatting.
                        Possible flags are: {input_path}, {input_filename}, {input_ext}
                        Default: {input_path}\{input_filename}_transposed.{input_ext}
  -f, --force-overwrite
                        If there already exists a file with the desired output path and
                        file name, overwrite it. WARNING: May cause data loss
  -v, --verbose         Adds more verbosity to outputs for debugging.
```

## Example Usage

- The most basic usage would be to offer a single input using `python .\Transpose_CSV.py -i .\INPUT_FILE.csv`. This would save the output to `.\INPUT_FILE_transposed.csv`.
- You can also specify where the output should be sent to using `-o`: `python .\Transpose_CSV.py -i .\INPUT_FILE.csv -o C:\Users\John\MyNewFile.{input_ext}` would save the file to the specified path and name, but keep whatever extension it found on the input. The most useful flags are `{input_path} and {input_filename}`, since the script is designed for .csv files.
- You can place flags between specified parts of the filename like so: `python .\Transpose_CSV.py -i .\INPUT_FILE.csv -o {input_path}\My_New_{input_filename}.csv`
