import os
from PIL import Image

def add_padding(img, padding=2):
    """
    Adds padding around the image.

    Parameters:
        img (PIL.Image): The input image to which padding will be added.
        padding (int): The padding size in pixels.

    Returns:
        PIL.Image: The padded image.
    """
    # Get the size of the original image
    width, height = img.size
    
    # Calculate new size with padding
    new_width = width + 2 * padding
    new_height = height + 2 * padding
    
    # Create a new image with a white background
    padded_img = Image.new('RGB', (new_width, new_height), color='white')
    
    # Paste the original image into the center of the new image
    padded_img.paste(img, (padding, padding))
    
    return padded_img


def concatenate_all_images(digits, path, out_path, width):
    """
    Concatenates all images from all digit directories into a single image and saves labels to a .box file in jTessBoxEditor format.

    Parameters:
        digits (list): List of digit directories to process.
        path (str): Path to the parent directory containing digit folders.
        out_path (str): Path where the concatenated image and labels file will be saved.
        width (int): Number of images in a row.

    Returns:
        list: A list of labels in the order of concatenated images.
    """
    # Initialize a list to store all images and corresponding labels
    labels_in_order = []
    all_images = []

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
        
        # Open all images, apply padding, and append to the list
        for img_file in image_files:
            with Image.open(img_file) as img:
                # padded_img = add_padding(img)  # Add padding to the image
                # all_images.append(padded_img.copy())  # Ensure the padded image is copied
                all_images.append(img.copy())
                # Set the label to "/" if it's "__"
                label = "/" if digit == "__" else digit
                labels_in_order.append(label)

    # Check if any images were loaded
    if not all_images:
        print("No images found in the specified directories.")
        return []

    # Determine size of the canvas (after padding)
    image_width, image_height = all_images[0].size
    rows = (len(all_images) + width - 1) // width  # Calculate the number of rows
    canvas_width = width * image_width
    canvas_height = rows * image_height
    concatenated_image = Image.new('RGB', (canvas_width, canvas_height), color='white')

    # Save bounding box details
    bounding_boxes = []

    # Paste all images onto the canvas with adjusted bounding boxes
    for idx, img in enumerate(all_images):
        row, col = divmod(idx, width)
        x_min = col * image_width + 6
        y_min = row * image_height + 3
        x_max = x_min + image_width - 2
        y_max = y_min + image_height
        
        # Adjust bounding boxes for padding
        x_min += 2  # Add reverse padding
        y_min += 2  # Add reverse padding
        x_max -= 2  # Subtract reverse padding
        y_max -= 2  # Subtract reverse padding
        
        bounding_boxes.append((labels_in_order[idx], x_min, canvas_height - y_max, x_max, canvas_height - y_min, 0))
        concatenated_image.paste(img, (x_min, y_min))

    # Save the concatenated image
    output_file = os.path.join(out_path, "all_digits_concatenated.png")
    concatenated_image.save(output_file)
    print(f"Saved concatenated image for all digits at: {output_file}")

    # Save the labels to a .box file
    labels_file = os.path.splitext(output_file)[0] + ".box"
    with open(labels_file, 'w', encoding='utf-8') as f:
        for label, x_min, y_min, x_max, y_max, page_num in bounding_boxes:
            f.write(f"{label} {x_min} {y_min} {x_max} {y_max} {page_num}\n")
    print(f"Saved labels in jTessBoxEditor format to: {labels_file}")

    return labels_in_order


# Example Usage
if __name__ == "__main__":
    # Define the input list of digits
    digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0', '__']
    
    # Specify the input path containing digit directories
    path = r"E:\Cloudilic assessment\helpful scripts\data"
    
    # Specify the output path for saving concatenated image
    out_path = r"E:\Cloudilic assessment\helpful scripts\data\concatenated_images"
    os.makedirs(out_path, exist_ok=True)
    
    # Define the number of images per row
    width = 25
    
    # Run the concatenation function
    labels_in_order = concatenate_all_images(digits, path, out_path, width)
