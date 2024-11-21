import cv2
import os
import numpy as np
from config import CONFIG

def process_and_save_image(image, save_path, target_size=(32, 32), padding=5):
    """
    Process the image to ensure it's binary (black and white),
    enhance clarity using sharpening, add white padding to the left and right sides,
    and resize to target size.
    """
    # Ensure the image is grayscale (if it's in BGR format, convert it)
    if len(image.shape) == 3:  # If the image is color (3 channels)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Sharpen the image
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening kernel
    sharpened_image = cv2.filter2D(image, -1, kernel)

    # Add white padding to both left and right sides
    padded_image = cv2.copyMakeBorder(
        sharpened_image,
        top=0,
        bottom=0,
        left=padding,
        right=padding,
        borderType=cv2.BORDER_CONSTANT,
        value=255  # White padding (255 for grayscale image)
    )

    # Resize the image to the target size
    resized_image = cv2.resize(padded_image, target_size, interpolation=cv2.INTER_LANCZOS4)
    # inverted_image = cv2.bitwise_not(resized_image)

    # Save the processed image
    cv2.imwrite(save_path, resized_image)


def extract_digits(image_path, output_folder):
    """
    Extract digits from an image, process them, and save each digit individually.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the input image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary threshold to create a binary image
    _, binary_image = cv2.threshold(gray_image, 70, 255, cv2.THRESH_BINARY)
    
    # Initialize the list to store x-coordinates for ROI (Regions of Interest)
    roi_lst = []
    
    # Loop through each pixel in the binary image to detect digits
    start_x = None
    for x in range(binary_image.shape[1]):  # Loop over columns (x-axis)
        # Check if we encounter a black pixel (0 in binary image, black pixel is 0, white is 255)
        if binary_image[:, x].min() == 0:  # If there is a black pixel in this column
            if start_x is None:  # This is the start of a new digit
                start_x = x  # Mark the starting x-coordinate of the digit
        else:
            if start_x is not None:  # If a digit just ended
                roi_lst.append((start_x - 1, x + 1))  # Add the start and end x-coordinates of the digit
                start_x = None  # Reset start_x for the next digit

    # If the last digit runs till the end of the image
    if start_x is not None:
        roi_lst.append((start_x, binary_image.shape[1]))
    
    # Loop over the ROIs and crop the image
    for idx, (start, end) in enumerate(roi_lst):
        # Crop the image from start to end x-coordinates (using the full y-range)
        cropped_digit = image[:, max(0, start):min(end, image.shape[1])]
        
        # Here, instead of applying a mask, we can directly modify the cropped image
        # For inpainting, we just focus on the regions defined by the start_x and end_x
        # For now, we are just passing the cropped_digit for further processing
        
        # Define the path for saving cropped images
        cropped_image_path = os.path.join(output_folder, f"digit_{idx + 1}.png")
        
        # Process and save the cropped image
        process_and_save_image(cropped_digit, cropped_image_path, target_size=(32, 32), padding=5)
    
    print(f"Finished extracting digits. Cropped images saved in {output_folder}")


# Example usage
if __name__ == "__main__":
    for dir in os.listdir(CONFIG["cropped_rois_dir"]):
        # if '1' in dir or '4' in dir:
        image_path = os.path.join(CONFIG["cropped_rois_dir"], dir)
        dir_name = os.path.basename(image_path).split('.')[0]
        output_folder = os.path.join(CONFIG["digits_dir"], dir_name)
        extract_digits(image_path, output_folder)
