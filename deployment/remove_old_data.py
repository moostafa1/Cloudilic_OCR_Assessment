import os
import shutil
from config import CONFIG


def clean_directory(dir_path):
    """
    Removes all files and nested directories inside a given directory.

    Parameters:
    dir_path (str): Path to the directory.

    Returns:
    str: Success or error message.
    """
    if not os.path.exists(dir_path):
        return f"Directory '{dir_path}' does not exist."

    if not os.path.isdir(dir_path):
        return f"'{dir_path}' is not a directory."

    try:
        # Loop over each item in the directory
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            # Check if it's a file or directory
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # Remove file or symlink
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directory
        return f"Directory '{dir_path}' has been cleaned."
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
if __name__ == "__main__":
    print(clean_directory(CONFIG["processed_images_dir"]))
    print(clean_directory(CONFIG["digits_dir"]))
    print(clean_directory(CONFIG["cropped_rois_dir"]))
