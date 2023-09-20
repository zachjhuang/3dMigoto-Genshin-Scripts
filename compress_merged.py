import os
import hashlib

def main():
    # Get the absolute path to the directory containing the Python script
    script_dir = os.getcwd()

    # Construct the absolute path to merged.ini
    ini_file = os.path.join(script_dir, 'merged.ini')

    # Open the file for reading
    with open(ini_file, 'r') as infile, open('new_merged.ini', 'w') as outfile:
        # Stores hash: filename pairings
        hash_dict = {}
        duplicate_files = []
        # Iterate over each line in the file
        for line in infile:
            # Check if this is a position file declaration
            if 'filename = ' in line and '.buf' not in line:
                filename = line.split('=')[1].strip()
                hash_key = compute_file_hash(filename)
                # See if hash already exists
                hash_value = hash_dict.get(hash_key)
                if hash_value and hash_value != filename:
                    line = f"filename = {hash_value}\n"
                    # Delete file if it hasn't been deleted already
                    duplicate_files.append(filename)
                else:
                    # Add hash:filename to dictionary
                    hash_dict[hash_key] = filename
            outfile.write(line)
    for filename in duplicate_files:
        if os.path.exists(filename):
            os.remove(filename)
    os.remove('merged.ini')
    os.rename('new_merged.ini', 'merged.ini')

# Return hash for file
def compute_file_hash(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

if __name__ == "__main__":
    main()
