import os
from PIL import Image
import cv2
import numpy as np

def dilate_image(image, kernel_size=(5, 5), iterations=1):
    """
    Applies dilation to the given image.

    Parameters:
    - image (PIL.Image.Image): The image to dilate.
    - kernel_size (tuple): Size of the dilation kernel. Default is (5, 5).
    - iterations (int): Number of times dilation is applied. Default is 1.

    Returns:
    - PIL.Image.Image: The dilated image.
    """
    # Convert PIL image to NumPy array for OpenCV
    image_np = np.array(image)
    
    # Handle grayscale and RGB images separately
    if len(image_np.shape) == 2:  # Grayscale
        dilated_np = cv2.dilate(image_np, np.ones(kernel_size, np.uint8), iterations=iterations)
    else:  # RGB
        # Split channels, dilate each, then merge
        channels = cv2.split(image_np)
        dilated_channels = [cv2.dilate(ch, np.ones(kernel_size, np.uint8), iterations=iterations) for ch in channels]
        dilated_np = cv2.merge(dilated_channels)
    
    # Convert back to PIL image
    return Image.fromarray(dilated_np)

def resize_images_in_directory(directory_path, size=(32, 32), kernel_size=(5, 5), iterations=1):
    """
    Resizes all images in the specified directory to a fixed size, applies dilation,
    and replaces the original images.

    Parameters:
    - directory_path (str): Path to the directory containing images.
    - size (tuple): Target size for resizing (width, height). Default is (32, 32).
    - kernel_size (tuple): Size of the dilation kernel. Default is (5, 5).
    - iterations (int): Number of times dilation is applied. Default is 1.
    """
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        try:
            with Image.open(file_path) as img:
                # Resize the image
                resized_img = img.resize(size, Image.LANCZOS)
                
                # Save the dilated image, replacing the original
                resized_img.save(file_path)
                print(f"Processed and saved: {file_path}")
        except Exception as e:
            print(f"Skipping file '{filename}'. Error: {e}")


# Example usage:
# Provide the path to the directory containing images
if __name__ == "__main__":
    resize_images_in_directory('E:\Cloudilic assessment\helpful scripts\data\٥')
