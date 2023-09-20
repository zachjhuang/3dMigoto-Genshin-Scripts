import os
import re
import shutil

def main():
    # Get the absolute path to the directory containing the Python script
    script_dir = os.getcwd()

    # Construct the absolute path to merged.ini
    ini_file = os.path.join(script_dir, 'merged.ini')

    # Open the file for reading
    with open(ini_file, 'r') as infile, open('new_merged.ini', 'w') as outfile:
        curr = 0
        resource = None
        subfolders = []
        resource_pattern = r"\[Resource.+?\.\d+\]"
        # Iterate over each line in the file
        for line in infile:
            if 'Merged Mod:' in line:
                subfolders = line.split("; Merged Mod: ")[1].split(", ")
                subfolders = [os.path.dirname(i.split(",")[0]) for i in subfolders if '\\' in i]
            # Reset working directory when new number in [Resource...]
            elif re.match(line, resource_pattern):
                curr = int(line.split('.')[1].split(']')[0])
                resource = line.split('.')[0].split('[Resource')[1].split('IB')[0]
            # Check if this is a position file declaration
            elif 'filename = ' in line:
                # Extract the directory from the filename
                dir_name = os.path.dirname(line.split('=')[1].strip())
                working_dir = subfolders[curr]
                # Extract the filename from the path
                file_name = os.path.basename(line.split('=')[1].strip())
                file_extension = file_name.split('.')[1]
                new_file_name = resource + '.' + file_extension
                # Construct the source and destination paths
                src_path = os.path.join(dir_name, file_name)
                dst_path = os.path.join(working_dir, new_file_name)
                # Copy the file from the source to the destination
                if src_path != dst_path:
                    shutil.copy(src_path, dst_path)
                    line = f"filename = {dst_path}\n"
            outfile.write(line)
    
    os.remove('merged.ini')
    os.rename('new_merged.ini', 'merged.ini')

if __name__ == "__main__":
    main()

