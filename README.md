# pyType-cover How To

A demo of how to use the pyType-cover script across your code bases.

## Step 1
In the config.ini file decide whether you are going to run coverage across a directory including sub-directories or whether on a single file. If running across a directory set the parameter `cover_file_or_directory = dir`. To run on a single file set the parameter to `cover_file_or_directory = file`.

## Step 2
If running on a file set the parameter 'file_to_cover' to the **file path** and the **file name**. For example `file_to_cover = c:\directory_to_cover\file_name.py`

## Step 3
If running on a dir set the parameter `directory_to_cover` to the **file path**. For example `file_to_cover = c:\directory_to_cover\`

## Step 4
run `python pyType-cover.py /path/to/config.ini`

# Config example
```
[python_type_coverage]

#file or dir as strings
cover_file_or_directory = file

#filepath & file name of file to run coverage on
file_to_cover = pyType-cover.py

#root / parent directory of files to run coverage on
directory_to_cover = 
```

# Output example
```
No return type defined on file python_type_coverage.py line 90
No python typing found on file fdi_accessible_format.py line 72
```
