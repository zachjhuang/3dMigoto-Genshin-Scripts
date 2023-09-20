import os
import re

def clean_subfolder_names():
    # Set the working directory to the folder the script is in
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)

    # Define a regular expression that matches non-letter characters
    regex = re.compile('[^a-zA-Z]')

    # Define the path to the directory containing the subfolders
    directory_path = '.'

    # Loop over the subfolders in the directory
    for subfolder in os.listdir(directory_path):
        # Construct the full path to the subfolder
        subfolder_path = os.path.join(directory_path, subfolder)

        # Check if the subfolder is a directory
        if os.path.isdir(subfolder_path):
            # Remove non-letter characters from the subfolder name
            new_subfolder_name = regex.sub('', subfolder)

            # Construct the full path to the new subfolder
            new_subfolder_path = os.path.join(directory_path, new_subfolder_name)

            # Rename the subfolder
            os.rename(subfolder_path, new_subfolder_path)

if __name__ == '__main__':
    clean_subfolder_names()