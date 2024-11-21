import os
import cv2
import json
import torch
import pytesseract
from PIL import Image
from config import CONFIG
from torchvision import transforms
from number_to_digits_splitter import extract_digits
from crop_ROIs import crop_roi
from image_processing import preprocess_image
from invoice_extraction_models import ocr_dates_eng_digits, ocr_arabic_digits



# def append_to_json(new_data, file_path="data/invoice_ocr.json"):
#     try:
#         # Open the file in read mode to get the current data
#         with open(file_path, 'r', encoding="utf-8") as f:
#             # Load the current data
#             existing_data = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         # If file does not exist or is empty, initialize with an empty list
#         existing_data = []

#     # Append the new data to the existing data
#     existing_data.append(new_data)

#     # Write the updated data back to the file
#     with open(file_path, 'w', encoding="utf-8") as f:
#         json.dump(existing_data, f, indent=4, ensure_ascii=False)

#     return json.dumps(new_data)  # Return the new data as a JSON string if needed



def image_text_extractor(invoice_image_path):
    # step 1: crop the region of interest of the data we're going to extract:
    # invoice number, date, total amount, second product cost
    crop_roi()
    
    # step 2: make required image processing in order to be able to extract the data
    input_folder = CONFIG["cropped_rois_dir"]
    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        preprocess_image(image_path)
    print("Images are completely preprocessed and saved in [processed_images]")

    # step 3: extract the data using OCR models
    # for english digit extraction using tesseract model
    pytesseract.pytesseract.tesseract_cmd = CONFIG["tesseract_cmd"]
    english_data_actual_names = ["date", "total amount"]
    rois_path = CONFIG["processed_images_dir"]
    english_data = ocr_dates_eng_digits(rois_path)


    # for arabic digit extraction using torch model
    arabic_data_actual_names = ["invoice number", "second product cost"]
    data = {}
    # Label map (updated with your digit and special character labels)
    label_map = {
        '٠': 0, '١': 1, '٢': 2, '٣': 3, '٤': 4, '٥': 5, '٦': 6, '٧': 7, '٨': 8, '٩': 9,
    }

    # Load the JIT model
    loaded_model = torch.jit.load(CONFIG["torch_model_path"])
    loaded_model.eval()  # Set to evaluation mode

    # split number to digits in order to pass its digit to the model for making prediciton
    number_image_dir = os.listdir(CONFIG["cropped_rois_dir"])
    arabic_images = [i for i in number_image_dir if '1' in i or '4' in i]

    for num in arabic_images:
        dir_name = num.split('.')[0]
        data[dir_name] = ""
        number_image_path = os.path.join(CONFIG["cropped_rois_dir"], num)
        digits_images_path = os.path.join(CONFIG["digits_dir"], dir_name)
        extract_digits(number_image_path, digits_images_path)

        for d in os.listdir(digits_images_path):
            digit_image_path = os.path.join(digits_images_path, d)
            data[dir_name] += ocr_arabic_digits(label_map, loaded_model, digit_image_path)
    
    arabic_data = {arabic_data_actual_names[i]: data[k] for i, k in enumerate(data)}
    

    # just to order the data in the intended order
    to_extract = ["invoice number", "date", "total amount", "second product cost"]
    actual_data = {}
    for key in to_extract:
        if key in english_data:
            actual_data[key] = english_data[key]
        elif key in arabic_data:
            actual_data[key] = arabic_data[key]
    
    # save extracted data to json file
    json_string = json.dumps(actual_data, ensure_ascii=False, indent=4)
    with open("data/invoice_ocr.json", 'w', encoding="utf-8") as f: # 'a'
        f.write(json_string)
        # json.dump(actual_data, f, indent=4)
    # json_string = append_to_json(actual_data, file_path="data/invoice_ocr.json")
    return json_string


if __name__ == "__main__":
    invoice_image_path = CONFIG["output_json"]
    image_text_extractor(invoice_image_path)