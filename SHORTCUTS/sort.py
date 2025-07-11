import os
import shutil

def move_files_to_type_folders():
    current_directory = os.getcwd()
    
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        
        if os.path.isfile(item_path):
            file_extension = os.path.splitext(item)[1][1:]  # Get file extension without dot
            if not file_extension:
                file_extension = 'no_extension'
                
            destination_folder = os.path.join(current_directory, file_extension)
            
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
                
            shutil.move(item_path, os.path.join(destination_folder, item))

if __name__ == "__main__":
    move_files_to_type_folders()