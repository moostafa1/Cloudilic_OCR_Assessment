import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
from tqdm import tqdm
import random
from PIL import ImageFilter

def add_gaussian_noise(image, mean=0, sigma=25):
    """Add Gaussian noise to the image."""
    np_image = np.array(image)
    noise = np.random.normal(mean, sigma, np_image.shape).astype(np.uint8)
    noisy_image = cv2.add(np_image, noise)
    return Image.fromarray(noisy_image)

def random_augmentation(image, target_size=(32, 32)):
    """
    Apply a series of meaningful augmentations for OCR training on digits,
    with reduced pepper & salt noise and proper background handling during rotation.
    """
    # Random Scaling (zoom in or zoom out) - Scaling factor between 0.8 and 1.2
    if random.random() > 0.5:
        scale_factor = random.uniform(0.8, 1.2)
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
    
    # Random Rotation (between -15 to 15 degrees) with proper background handling
    if random.random() > 0.5:
        angle = random.uniform(-15, 15)  # Limited rotation for OCR purposes
        background_color = (255, 255, 255)  # White background
        rotated_image = image.rotate(angle, resample=Image.BICUBIC, expand=True)
        
        # Create a white background
        background = Image.new("RGB", rotated_image.size, color=background_color)
        background.paste(rotated_image, mask=rotated_image.split()[3] if rotated_image.mode == 'RGBA' else None)
        image = background
    
    # Random Translation (shifting the image) - small translation for digit displacement
    if random.random() > 0.5:
        width, height = image.size
        max_translation = 0.2  # Allow for small horizontal and vertical shift
        translate_x = random.uniform(-max_translation * width, max_translation * width)
        translate_y = random.uniform(-max_translation * height, max_translation * height)
        image = image.transform(
            (width, height),
            Image.AFFINE,
            (1, 0, translate_x, 0, 1, translate_y),
            resample=Image.BICUBIC
        )
    
    # Gaussian Blur (radius between 0.2 and 2)
    if random.random() > 0.5:
        image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 2)))
    
    # Sharpening (enhance sharpness between 1.0 and 2.0)
    if random.random() > 0.5:
        enhancer = ImageEnhance.Sharpness(image)
        factor = random.uniform(1.0, 2.0)
        image = enhancer.enhance(factor)
    
    # Dilation (expanding the white areas) - using OpenCV
    if random.random() > 0.5:
        np_image = np.array(image.convert('L'))  # Convert to grayscale for dilation
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(np_image, kernel, iterations=1)
        image = Image.fromarray(dilated)
    
    # Erosion (shrinking the white areas) - using OpenCV
    if random.random() > 0.5:
        np_image = np.array(image.convert('L'))  # Convert to grayscale for erosion
        kernel = np.ones((3, 3), np.uint8)
        eroded = cv2.erode(np_image, kernel, iterations=1)
        image = Image.fromarray(eroded)
    
    # Reduced Pepper and Salt Noise (random noise)
    if random.random() > 0.5:
        np_image = np.array(image)
        height, width = np_image.shape[:2]
        salt_pepper_ratio = 0.00005  # Further reduced noise level
        num_salt = int(salt_pepper_ratio * width * height)
        num_pepper = int(salt_pepper_ratio * width * height)

        # Add Salt (white pixels)
        for _ in range(num_salt):
            y = random.randint(0, height - 1)
            x = random.randint(0, width - 1)
            np_image[y, x] = 255

        # Add Pepper (black pixels)
        for _ in range(num_pepper):
            y = random.randint(0, height - 1)
            x = random.randint(0, width - 1)
            np_image[y, x] = 0

        image = Image.fromarray(np_image)

    # Bitwise NOT (invert colors) - invert black/white for robustness
    if random.random() > 0.5:
        np_image = np.array(image.convert('L'))  # Convert to grayscale for inversion
        np_image = cv2.bitwise_not(np_image)  # Invert the image (bitwise NOT)
        image = Image.fromarray(np_image)

    # Add Gaussian noise to simulate real-life image noise
    if random.random() > 0.5:
        image = add_gaussian_noise(image)

    # Center crop the image to the target size after augmentation
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    return image


def create_image(text, font, target_size=(32, 32), padding=2):
    # Create a temporary image to calculate text size
    temp_image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(temp_image)
    
    # Calculate the width and height for the text
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
    
    # Add padding to the width and height
    width = text_width + 2 * padding
    height = text_height + 2 * padding
    
    # Create the final image with appropriate size and padding
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw the text centered with padding
    draw.text((padding, padding), text, fill='black', font=font)

    # Ensure image is the target size
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    return image


def save_images(digits, font, save_path="E:\\Cloudilic assessment\\helpful scripts\\data", num_examples=50, target_size=(32, 32)):
    # Loop over each character and generate the required number of images
    for digit in tqdm(digits, desc="Generating Images"):
        # Sanitize the character to ensure valid directory and file names
        sanitized_digit = digit.strip().replace(" ", "_").replace("/", "__")
        
        # Create directory for the digit if it doesn't exist
        digit_dir = os.path.join(save_path, sanitized_digit)
        os.makedirs(digit_dir, exist_ok=True)
        
        for i in range(num_examples):
            # Generate the image for the character
            image = create_image(digit, font, target_size)
            
            # Apply random augmentation to the image
            image = random_augmentation(image, target_size)
            
            # Save the generated image with sanitized file names
            image_path = os.path.join(digit_dir, f"{sanitized_digit}_{i}.png")
            image.save(image_path)
    
    print("Image generation complete.")


# Example Usage
if __name__ == "__main__":
    digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ' / ']
    
    # Specify the font path for 'Arial'
    font_path = r'C:\Windows\Fonts\arial.ttf'  # Adjust the path to where Arial font is located
    font = ImageFont.truetype(font_path, 30)

    save_path = r"E:\Cloudilic assessment\helpful scripts\data"
    
    # Generate and save images with augmentation
    save_images(digits, font, save_path, num_examples=2000, target_size=(32, 32))
