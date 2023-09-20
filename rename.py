import os
import argparse

def replace_string_in_names():
    # Iterate through all files and subfolders in the specified folder
    
    old_strings = input("Enter the string(s) to be replaced: ")
    new_string = input("Enter the replacement string: ")
    for old_string in old_strings.split(','):
        for root, dirs, files in os.walk(os.getcwd(), topdown = False):
            for file in files:
                if ".ini" in file:
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, 'new_file.ini')
                    print(file)
                    with open(old_path, 'r') as infile, open(new_path, 'w') as outfile:
                        for line in infile:
                            if old_string in line:
                                line = line.replace(old_string, new_string)
                                print(line)
                            outfile.write(line.replace(old_string, new_string))
                    os.remove(old_path)
                    os.rename(new_path, old_path)
                    
            for file in files + dirs:
                if old_string in file:
                    old_name = os.path.join(root, file)
                    new_name = os.path.join(root, file.replace(old_string, new_string))

                    # Rename the file or subfolder
                    os.rename(old_name, new_name)
                    print(f"Renamed '{old_name}' to '{new_name}'")

# Call the function to replace the string in names
replace_string_in_names()