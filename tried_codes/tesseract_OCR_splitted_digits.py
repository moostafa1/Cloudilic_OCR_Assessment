import os
import json
import pytesseract
from PIL import Image
from number_to_digits_splitter import extract_digits

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract digits using Tesseract OCR
def predict_oc_image(label_map, image_path):
    # Open the image
    image = Image.open(image_path).convert('RGB')

    # Use Tesseract to extract text from the image in Arabic language
    extracted_text = pytesseract.image_to_string(image, lang='ara_digits')

    # Translate extracted Arabic digits to English digits using the label map
    predicted_digits = ""
    for char in extracted_text:
        if char in label_map:  # Check if the character is a digit in Arabic
            predicted_digits += str(label_map[char])

    return predicted_digits

if __name__ == "__main__":
    data_actual_names = ["invoice number", "date", "total amount", "second product cost"]
    data = {}
    
    # Label map (Arabic to English digit)
    label_map = {
        '٠': 0, '١': 1, '٢': 2, '٣': 3, '٤': 4, '٥': 5, '٦': 6, '٧': 7, '٨': 8, '٩': 9
    }

    # Directory containing images to OCR
    number_image_dir = os.listdir("E:\\Cloudilic assessment\\images_to_ocr")

    for num in number_image_dir:
        dir_name = num.split('.')[0]
        data[dir_name] = ""
        number_image_path = os.path.join("E:\\Cloudilic assessment\\images_to_ocr", num)
        digits_images_path = f"E:\\Cloudilic assessment\\image_number_to_splitted_digits\\{dir_name}"
        extract_digits(number_image_path, digits_images_path)

        for d in os.listdir(digits_images_path):
            digit_image_path = os.path.join(digits_images_path, d)
            data[dir_name] += predict_oc_image(label_map, digit_image_path)

    actual_data = {data_actual_names[i]: data[k] for i, k in enumerate(data)}

    # Print and save the output
    print(actual_data)
    with open("invoice_ocr.json", 'w') as f:
        json.dump(actual_data, f, indent=4)
