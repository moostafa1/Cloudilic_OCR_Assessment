import os
from PIL import Image

def generate_box_file(img_path, label, output_dir, sub_width=32, sub_height=32, padding=3):
    """
    Generate a box file for an image with concatenated characters.
    Args:
        img_path: Path to the concatenated image.
        label: Character label for each sub-image in the concatenated image.
        output_dir: Directory where the box file will be saved.
        sub_width: Width of each sub-image in the concatenated image.
        sub_height: Height of each sub-image in the concatenated image.
        padding: Number of pixels to add as padding to separate sub-images.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load the concatenated image
    img = Image.open(img_path)
    if img is None:
        print(f"Error: Could not load image from {img_path}")
        return

    img_width, img_height = img.size
    num_images_in_row = img_width // sub_width  # Number of characters in one row
    num_images_in_column = img_height // sub_height  # Number of rows in the concatenated image

    # Prepare the box file content
    box_file_content = []
    for row in range(num_images_in_column):
        for col in range(num_images_in_row):
            # Calculate the coordinates for each sub-image with padding
            x_min = col * sub_width + padding
            y_min = row * sub_height + padding
            x_max = x_min + sub_width - 2 * padding  # Subtract padding from the right side as well
            y_max = y_min + sub_height - 2 * padding  # Subtract padding from the bottom side as well

            # Adjust the label if it's "__" (change it to "/")
            if label == "__":
                label = "/"

            # Append the box file line
            box_file_content.append(f"{label} {x_min} {img_height - y_max} {x_max} {img_height - y_min} 0")

    # Save the box file
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    box_file_path = os.path.join(output_dir, f"{img_name}.box")

    with open(box_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(box_file_content))

    print(f"Box file saved: {box_file_path}")




# Example usage
if __name__ == "__main__":
    # Directory containing concatenated images
    concatenated_images_dir = "E:/Cloudilic assessment/helpful scripts/data/concatenated_images"
    output_dir = "E:/Cloudilic assessment/helpful scripts/data/labeled_boxes"

    # Define the mapping of characters to images
    char_image_mapping = {
        '٠': "٠_concatenated.png",
        '١': "١_concatenated.png",
        '٢': "٢_concatenated.png",
        '٣': "٣_concatenated.png",
        '٤': "٤_concatenated.png",
        '٥': "٥_concatenated.png",
        '٦': "٦_concatenated.png",
        '٧': "٧_concatenated.png",
        '٨': "٨_concatenated.png",
        '٩': "٩_concatenated.png",
        '0': "0_concatenated.png",
        '1': "1_concatenated.png",
        '2': "2_concatenated.png",
        '3': "3_concatenated.png",
        '4': "4_concatenated.png",
        '5': "5_concatenated.png",
        '6': "6_concatenated.png",
        '7': "7_concatenated.png",
        '8': "8_concatenated.png",
        '9': "9_concatenated.png",
        '__': "___concatenated.png",  # For "/" character
    }

    # Generate box files for all characters
    for char, img_name in char_image_mapping.items():
        img_path = os.path.join(concatenated_images_dir, img_name)
        if os.path.exists(img_path):
            generate_box_file(img_path, char, output_dir)
        else:
            print(f"Image not found: {img_path}")
