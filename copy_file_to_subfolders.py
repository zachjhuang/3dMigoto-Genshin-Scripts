import os
import shutil

def copy_to_subfolders(source_file, target_dir):
    for subdir in os.listdir(target_dir):
        subdir_path = os.path.join(target_dir, subdir)
        if os.path.isdir(subdir_path):
            target_file = os.path.join(subdir_path, os.path.basename(source_file))
            print(source_file + target_file)
            shutil.copy2(source_file, target_file)

if __name__ == '__main__':
    source_file = 'genshin_merge_mods.py'
    target_dir = '.'
    copy_to_subfolders(source_file, target_dir)
