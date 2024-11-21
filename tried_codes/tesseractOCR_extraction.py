import os
import pytesseract
import cv2
import json


# Set the path to Tesseract executable (for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

    # imgs_path = [os.path.join(rois_path, img) for img in os.listdir(rois_path)]
    imgs_path = [os.path.join(rois_path, img) for img in os.listdir(rois_path) if '2' in img or '3' in img]

    extracted_data = []

    for image_path in imgs_path:
        # Load the image using OpenCV
        img = cv2.imread(image_path)

        
        text = pytesseract.image_to_string(img, lang='ara')   # ara_digits
        print(text)
        
        # Assuming you're extracting text by some keyword matching:
        extracted_data.append(text.replace('\n', '').replace('\f', '')
)

    # Assuming `to_extract` contains keywords like 'invoice number', 'date', etc.
    data = dict(zip(to_extract, extracted_data))
    print(data)

    # Save to JSON file after closing the plot
    with open("extracted_data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)




if __name__ == "__main__":
    # rois_path = "E:/Cloudilic assessment/images_to_ocr"
    rois_path = "E:\Cloudilic assessment\processed_images"
    # to_extract = ["invoice number", "date", "total amount", "second product cost"]
    to_extract = ["date", "total amount"]
    extracted_data = []

    image_to_ocr(rois_path)
