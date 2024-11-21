import os
from shutil import copy2
from PIL import Image

def convert_png_to_tif(png_dir, box_dir, output_dir="png_to_tif"):
    """
    Converts .png images to .tif format for Tesseract training and copies .box files.
    Args:
        png_dir: Directory containing .png images.
        box_dir: Directory containing corresponding .box files.
        output_dir: Directory to save the .tif images and .box files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through all .png files in the directory
    for file_name in os.listdir(png_dir):
        if file_name.endswith('.png'):
            png_path = os.path.join(png_dir, file_name)

            # Corresponding .box file
            base_name = os.path.splitext(file_name)[0]
            box_file_path = os.path.join(box_dir, f"{base_name}.box")
            
            # Check if the .box file exists
            if not os.path.exists(box_file_path):
                print(f"Skipping {file_name}: .box file not found.")
                continue

            # Open the .png image
            img = Image.open(png_path)

            # Convert to grayscale
            img_gray = img.convert('L')

            # Save as uncompressed .tif
            tif_path = os.path.join(output_dir, f"{base_name}.tif")
            img_gray.save(tif_path, format='TIFF', compression='none')
            print(f"Converted {file_name} to {tif_path}")

            # Copy the .box file to the output directory
            copied_box_path = os.path.join(output_dir, f"{base_name}.box")
            copy2(box_file_path, copied_box_path)
            print(f"Copied {box_file_path} to {copied_box_path}")

if __name__ == "__main__":
    # Directories
    png_dir = "E:\\Cloudilic assessment\\helpful scripts\\data\\concatenated_images"
    box_dir = "E:\\Cloudilic assessment\\helpful scripts\\data\\labeled_boxes"
    output_dir = "E:\\Cloudilic assessment\\helpful scripts\\data\\png_to_tif"

    # Run the conversion
    convert_png_to_tif(png_dir, box_dir, output_dir)
