import os
import re
import argparse

def find_and_replace_string(directory_path, string_to_find, string_to_replace):
    """
    Searches for a string in all files in a subdirectory and replaces it with another string.

    :param directory_path: The path to the subdirectory to search in.
    :param string_to_find: The string to search for.
    :param string_to_replace: The string to replace the searched string with.
    """

    # Loop over all files in the directory
    for filename in os.listdir(directory_path):
        # Construct the full path to the file
        file_path = os.path.join(directory_path, filename)

        # Check if the file is a directory
        if os.path.isdir(file_path):
            # Recursively call this function on the subdirectory
            find_and_replace_string(file_path, string_to_find, string_to_replace)
        elif filename.endswith(".ini"):
            # Read the contents of the file
            with open(file_path, 'r') as f:
                file_contents = f.read()

            # Replace all instances of the string in the file contents
            new_file_contents = re.sub(string_to_find, string_to_replace, file_contents)

            # Write the modified contents back to the file
            with open(file_path, 'w') as f:
                f.write(new_file_contents)

if __name__ == '__main__':
    # Define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('string_to_find', help='The string to search for.')
    parser.add_argument('string_to_replace', help='The string to replace the searched string with.')
    args = parser.parse_args()

    # Get the directory path
    directory_path = os.path.dirname(os.path.abspath(__file__))

    print(f"Replace '{args.string_to_find}' with '{args.string_to_replace}' in path '{directory_path}'? (Y/N)")
    user_input = input().lower()
    if user_input == 'y':
        find_and_replace_string(directory_path, args.string_to_find, args.string_to_replace)
