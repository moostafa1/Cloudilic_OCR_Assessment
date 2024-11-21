import os
from PIL import Image
import numpy as np

def concatenate_images(digits, path, out_path, width):
    """
    Concatenates images from directories corresponding to each digit.
    
    Parameters:
        digits (list): List of digit directories to process.
        path (str): Path to the parent directory containing digit folders.
        out_path (str): Path where the concatenated image will be saved.
        width (int): Number of images in a row.
    """
    os.makedirs(out_path, exist_ok=True)
    for digit in digits:
        # Get the directory for the current digit
        digit_dir = os.path.join(path, digit.strip())
        
        # Verify if the directory exists
        if not os.path.isdir(digit_dir):
            print(f"Directory for digit '{digit}' not found, skipping.")
            continue
        
        # Load all image file paths from the digit's directory
        image_files = [os.path.join(digit_dir, f) for f in os.listdir(digit_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            print(f"No images found in directory for digit '{digit}', skipping.")
            continue
        
        # Open all images and resize them to the same size
        images = [Image.open(img_file) for img_file in image_files]
        image_width, image_height = images[0].size
        
        # Create a blank canvas for the concatenated image
        rows = (len(images) + width - 1) // width  # Calculate the number of rows
        canvas_width = width * image_width
        canvas_height = rows * image_height
        concatenated_image = Image.new('RGB', (canvas_width, canvas_height), color='white')
        
        # Paste each image onto the canvas
        for idx, img in enumerate(images):
            row, col = divmod(idx, width)
            x = col * image_width
            y = row * image_height
            concatenated_image.paste(img, (x, y))
        
        # Save the concatenated image
        output_file = os.path.join(out_path, f"{digit.strip()}_concatenated.png")
        concatenated_image.save(output_file)
        print(f"Saved concatenated image for digit '{digit}' at: {output_file}")

# Example Usage
if __name__ == "__main__":
    # Define the input list of digits
    digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0', '__']
    
    # Specify the input path containing digit directories
    path = r"E:\Cloudilic assessment\helpful scripts\data"
    
    # Specify the output path for saving concatenated images
    out_path = r"E:\Cloudilic assessment\helpful scripts\data\concatenated_images"
    
    # Define the number of images per row
    width = 25
    
    # Run the concatenation function
    concatenate_images(digits, path, out_path, width)
