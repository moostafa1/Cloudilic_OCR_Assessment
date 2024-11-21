import os
import easyocr
import cv2
import json

def image_to_ocr(rois_path):
    """
    Extract text from all images in `rois_path` and save the extracted text.

    Parameters
    ----------
    rois_path : str
        Path to the directory containing images to be processed.

    Returns
    -------
    data : dict
        A dictionary with the extracted text, where keys are the keywords in `to_extract`.
    """

    # Initialize EasyOCR Reader for Arabic and English
    reader = easyocr.Reader(['ar', 'en'])

    imgs_path = [os.path.join(rois_path, img) for img in os.listdir(rois_path)]

    extracted_data = []

    for image_path in imgs_path:
        # Load the image using OpenCV
        img = cv2.imread(image_path)

        # Perform OCR using EasyOCR
        result = reader.readtext(img)
        
        # Extract the text from the result
        text = " ".join([item[1] for item in result])
        print(text)
        
        # Append the extracted text to the data list
        extracted_data.append(text)

    # Assuming `to_extract` contains keywords like 'invoice number', 'date', etc.
    data = dict(zip(to_extract, extracted_data))
    print(data)

    # Save to JSON file
    with open("extracted_data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    rois_path = "E:/Cloudilic assessment/images_to_ocr"
    to_extract = ["invoice number", "date", "total amount", "second product cost"]
    extracted_data = []

    image_to_ocr(rois_path)
