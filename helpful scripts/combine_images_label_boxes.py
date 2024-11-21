import os
import shutil
import glob

def copy_images_and_labels(image_dir, label_dir, output_dir):
    """
    Copies concatenated images and their corresponding label files (.box) to a new output directory.
    
    Parameters:
    - image_dir (str): Path to the directory containing concatenated image files (.png).
    - label_dir (str): Path to the directory containing label files (.box).
    - output_dir (str): Path to the output directory where the images and labels will be copied.
    """
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all PNG image files in the image directory using glob
    image_files = glob.glob(os.path.join(image_dir, '*.png'))

    # Loop through each image file and match with its label
    for image_path in image_files:
        # Extract the base filename without extension
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Find the corresponding label file (.box extension)
        label_path = os.path.join(label_dir, base_name + '.box')
        
        if os.path.exists(label_path):
            # Copy both the image and label to the output directory
            shutil.copy(image_path, os.path.join(output_dir, os.path.basename(image_path)))
            shutil.copy(label_path, os.path.join(output_dir, base_name + '.box'))
            print(f"Copied {base_name}.png and {base_name}.box to {output_dir}")
        else:
            print(f"Label file for {base_name}.png not found, skipping...")


# Example usage:
if __name__ == "__main__":
    image_dir = "E:/Cloudilic assessment/helpful scripts/data/concatenated_images"
    label_dir = "E:/Cloudilic assessment/helpful scripts/data/labeled_boxes"
    output_dir = "E:/Cloudilic assessment/helpful scripts/data/images_and_boxes"

    copy_images_and_labels(image_dir, label_dir, output_dir)
