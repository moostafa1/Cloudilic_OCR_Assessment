import os
import cv2
import json
import torch
import pytesseract
from PIL import Image
from config import CONFIG
from torchvision import transforms
from number_to_digits_splitter import extract_digits


def ocr_dates_eng_digits(rois_path):
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
    english_data_actual_names = ["date", "total amount"]
    extracted_data = []

    for image_path in imgs_path:
        # Load the image using OpenCV
        img = cv2.imread(image_path)

        
        text = pytesseract.image_to_string(img, lang='ara')   # ara_digits  ara
        # print(text)
        
        # Assuming you're extracting text by some keyword matching:
        extracted_data.append(text.replace('\n', '').replace('\f', '')
)

    # Assuming `english_data_actual_names` contains keywords like 'invoice number', 'date', etc.
    return dict(zip(english_data_actual_names, extracted_data))



def ocr_arabic_digits(label_map, loaded_model, image_path):
    # Define the transformations
    """
    Predicts the class of an image using a custom trained pytorch model.

    Parameters
    ----------
    label_map : dict
        A dictionary mapping class labels to their corresponding indices.
    loaded_model : torch.nn.Module
        The pre-tracustom trained pytorch model I trained  used for prediction.
    image_path : str
        The file path to the image to be classified.

    Returns
    -------
    str
        The predicted class label of the image.
    """
    transform = transforms.Compose([
        transforms.CenterCrop((32, 32)),  # Resize image to 32x32
        transforms.ToTensor(),        # Convert image to Tensor
        transforms.Normalize((0.5,), (0.5,))  # Normalize the image to [-1, 1]
    ])

    # Load the image
    image = Image.open(image_path).convert('RGB')  # Ensure it's in RGB format

    # Apply the transformation
    input_tensor = transform(image).unsqueeze(0)  # Add batch dimension (unsqueeze(0))

    # Make prediction
    with torch.no_grad():  # No need for gradients during inference
        output = loaded_model(input_tensor)

    # Get predicted class
    _, predicted_class = torch.max(output, 1)

    inverted_dict = {v: k for k, v in label_map.items()}

    # print(f"Predicted class: {inverted_dict[predicted_class.item()]}")
    return inverted_dict[predicted_class.item()]



    




if __name__ == "__main__":
    # for english digit extraction using tesseract model
    pytesseract.pytesseract.tesseract_cmd = CONFIG["tesseract_cmd"]
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
        number_image_path = os.path.join(CONFIG["pro"], num)
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
    with open(CONFIG["output_json"], 'w', encoding="utf-8") as f:
        f.write(json_string)
        # json.dump(actual_data, f, indent=4)
