import os

main_folder = os.getcwd()

# Iterate over subfolders in the main folder
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    # Check if the subfolder is a directory
    if os.path.isdir(subfolder_path):
        if len(os.listdir(subfolder_path)) == 1:
            continue
        # Iterate over sub-subfolders in the subfolder
        for sub_subfolder in os.listdir(subfolder_path):
            sub_subfolder_path = os.path.join(subfolder_path, sub_subfolder)
            
            # Check if the sub-subfolder is a directory
            if os.path.isdir(sub_subfolder_path):
                
                # Iterate over files in the sub-subfolder
                for file in os.listdir(sub_subfolder_path):
                    file_path = os.path.join(sub_subfolder_path, file)
                    
                    # Check if the file has the .ini extension
                    if file.endswith(".ini") and "DISABLED" not in file:
                        
                        # Add "DISABLED" to the beginning of the filename
                        new_file = "DISABLED" + file
                        new_file_path = os.path.join(sub_subfolder_path, new_file)
                        # Rename the file
                        os.rename(file_path, new_file_path)
