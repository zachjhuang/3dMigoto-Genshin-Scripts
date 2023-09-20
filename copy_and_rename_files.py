import os
import re
import shutil

def copy_and_rename_files():
    # Set the working directory to the folder the script is in
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)

    # Define a regular expression that matches the string "old_"
    regex = re.compile('old_')

    # Define the path to the directory containing the subfolders
    directory_path = '.'

    # Define the filenames of the files to be copied
    filenames_to_copy = [['SayuBodyMetalMap.dds', 'SayuHeadMetalMap.dds'],
                         ['SayuHoodHeadDiffuse.dds', 'SayuBodyDiffuse.dds'],
                         ['SayuHoodHeadLightMap.dds', 'SayuBodyLightMap.dds'],
                         ['SayuHoodHeadMetalMap.dds', 'SayuHeadMetalMap.dds'],
                         ['SayuHoodHeadShadowRamp.jpg', 'SayuBodyShadowRamp.jpg'],]

    # Loop over the subfolders in the directory
    for subfolder in os.listdir(directory_path):
        # Construct the full path to the subfolder
        subfolder_path = os.path.join(directory_path, subfolder)

        # Check if the subfolder is a directory
        if os.path.isdir(subfolder_path):
            # Remove the string "old_" from the subfolder name
            new_subfolder_name = regex.sub('', subfolder)

            # Construct the full path to the new subfolder
            new_subfolder_path = os.path.join(directory_path, new_subfolder_name)

            # Rename the subfolder
            os.rename(subfolder_path, new_subfolder_path)

            # Copy the files to the new subfolder and rename them
            for new_filename, old_filename in filenames_to_copy:
                # Construct the full path to the file to be copied
                source_file_path = os.path.join(new_subfolder_path, old_filename)

                # Construct the full path to the new file
                destination_file_path = os.path.join(new_subfolder_path, new_filename)

                # Copy the file to the new subfolder and rename it
                shutil.copyfile(source_file_path, destination_file_path)

if __name__ == '__main__':
    copy_and_rename_files()
