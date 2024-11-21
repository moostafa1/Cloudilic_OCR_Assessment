import random
import pickle
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta


# Function to generate a random 14-digit number
def generate_random_number(digits, max_length=6000):
    return ''.join(random.choices(digits, k=max_length))

# Function to generate a random date in the range# Function to create a random date string in English or Arabic format
def generate_random_date(language='english'):
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2030, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    if language == 'arabic':
        date_str = random_date.strftime("%d/%m/%Y")
        arabic_date = ''.join('٠١٢٣٤٥٦٧٨٩'[int(digit)] if digit.isdigit() else digit for digit in date_str)
        return arabic_date
    else:
        return random_date.strftime("%d/%m/%Y")


# Function to create an image from text, adjusting size to fit the text and wrap long text
def create_image(text, max_chars_per_line=25):
    # Load the font
    font = ImageFont.truetype('arial.ttf', 10)
    
    # Split text into lines with a maximum number of characters per line
    lines = [text[i:i + max_chars_per_line] for i in range(0, len(text), max_chars_per_line)]
    
    # Create a temporary image to calculate text size
    temp_image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(temp_image)
    
    # Calculate the width and height for the longest line and total height for all lines
    max_line_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines) + len(lines) * 10  # Adding line spacing
    
    # Create the final image with appropriate size
    width, height = max_line_width + 20, total_height + 20  # Adding padding
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw each line of text
    y_offset = 10  # Start drawing from a slight top margin
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:4]
        draw.text(((width - text_width) // 2, y_offset), line, fill='black', font=font)
        y_offset += text_height + 10  # Move to the next line with spacing

    return image


def generate_n_dates(num_dates, language='english'):
    dates = ""
    for _ in range(num_dates):
        dates += generate_random_date(language) + " "
    return dates


if __name__ == '__main__':
    # List of Arabic digits
    arabic_digits = ['٠', '١', '٢', '٣', '٤', '٥ ', '٦', '٧', '٨', '٩']
    # english_digits = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
    english_digits = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ' / ']

    # Output directory for saving images
    output_dir = 'E:\\Cloudilic assessment\\helpful scripts\\data\\'

    # Number of images to generate
    num_images = 3

    # Generate and save random dates as images
    for i in range(num_images):
        # Create an Arabic and english digits image
        mixed_data = generate_random_number(arabic_digits + english_digits, max_length=2000)
        image = create_image(mixed_data)
        image.save(output_dir + f'digits_{i}.png', 'PNG')
        # Create an English date image
        # english_date = generate_random_date(language='english')
        # english_date += "   " + generate_random_number(english_digits)
        # image = create_image(english_date)
        # image.save(output_dir + f'english_date_{i}.png', 'PNG')

