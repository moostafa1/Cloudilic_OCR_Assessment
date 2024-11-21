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

def augment_scanned_image(image, target_size=(32, 32), inv=False):
    
    # Random Scaling
    if random.random() > 0.5:
        scale_factor = random.uniform(0.9, 1.1)
        width, height = image.size
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
    
    # Random Rotation
    if inv and random.random() > 0.5:
        angle = random.uniform(-5, 5)
        image = image.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
    
    # Random Translation
    if random.random() > 0.5:
        width, height = image.size
        max_translation = 0.05
        translate_x = random.uniform(-max_translation * width, max_translation * width)
        translate_y = random.uniform(-max_translation * height, max_translation * height)
        image = image.transform(
            (width, height),
            Image.AFFINE,
            (1, 0, translate_x, 0, 1, translate_y),
            resample=Image.BICUBIC
        )
    
    # Gaussian Blur
    if random.random() > 0.5:
        image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 1)))
    
    # Brightness Adjustment
    if random.random() > 0.5:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(random.uniform(0.9, 1.1))
    
    # Contrast Adjustment
    if random.random() > 0.5:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(random.uniform(0.8, 1.2))
    
    # Add Gaussian Noise
    if random.random() > 0.5:
        image = add_gaussian_noise(image)
    
    # Optional: Color Inversion
    if random.random() > 0.9:
        np_image = np.array(image.convert('L'))
        np_image = cv2.bitwise_not(np_image)
        image = Image.fromarray(np_image)
    
    # Resize to Target Size
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    return image


def create_image(text, font, target_size=(32, 32), padding=2, grayscale=False):
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

    # Convert to grayscale if requested
    if grayscale:
        image = image.convert('L')  # Convert to grayscale
    
    # Ensure image is the target size
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    return image


def save_images(digits, font, save_path="E:\\Cloudilic assessment\\helpful scripts\\data", num_examples=50, target_size=(32, 32), grayscale=False):
    # Loop over each character and generate the required number of images
    for digit in tqdm(digits, desc="Generating Images"):
        # Sanitize the character to ensure valid directory and file names
        sanitized_digit = digit.strip().replace(" ", "_").replace("/", "__")
        
        # Create directory for the digit if it doesn't exist
        digit_dir = os.path.join(save_path, sanitized_digit)
        os.makedirs(digit_dir, exist_ok=True)
        
        for i in range(num_examples):
            # Generate the image for the character
            image = create_image(digit, font, target_size, grayscale=grayscale)
            
            # Apply random augmentation to the image
            image = augment_scanned_image(image, target_size)
            
            # Save the generated image with sanitized file names
            image_path = os.path.join(digit_dir, f"{sanitized_digit}_{i}.png")
            image.save(image_path)
    
    print("Image generation complete.")


# Example Usage
if __name__ == "__main__":
    arabic_digits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
    # digits = ['٠', '١', '٢', '٣', '٤', 'o', '٦', '٧', '٨', '9']
    #, 
    english_digits = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ' / ']
    
    # Specify the font path for 'Arial'
    font_path = r'C:\Windows\Fonts\arial.ttf'  # Adjust the path to where Arial font is located
    font = ImageFont.truetype(font_path, 20)

    save_path = r"E:\Cloudilic assessment\helpful scripts\data"
    
    # Generate and save images with augmentation, optionally in grayscale
    save_images(arabic_digits + english_digits,
                font, save_path,
                num_examples=25, # last time 10k
                target_size=(32, 32),
                grayscale=True)