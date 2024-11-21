import os
import json
import torch
from PIL import Image
from torchvision import transforms
from number_to_digits_splitter import extract_digits


def predict_oc_image(label_map, loaded_model, image_path):
    # Define the transformations
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
    data_actual_names = ["invoice number", "date", "total amount", "second product cost"]
    data = {}
    # Label map (updated with your digit and special character labels)
    label_map = {
        '٠': 0, '١': 1, '٢': 2, '٣': 3, '٤': 4, '٥': 5, '٦': 6, '٧': 7, '٨': 8, '٩': 9,
        # '9': 10, '8': 11, '7': 12, '6': 13, '5': 14, '4': 15, '3': 16, '2': 17, '1': 18, '0': 19, '/': 20
    }

    # Load the JIT model
    loaded_model = torch.jit.load('E:\Cloudilic assessment\\torch models\\ocr_model_traced.pt')
    loaded_model.eval()  # Set to evaluation mode

    # split number to digits in order to pass its digit to the model for making prediciton
    number_image_dir = os.listdir("E:\Cloudilic assessment\images_to_ocr")

    for num in number_image_dir:
        dir_name = num.split('.')[0]
        data[dir_name] = ""
        number_image_path = os.path.join("E:\Cloudilic assessment\images_to_ocr", num)
        digits_images_path = f"E:\Cloudilic assessment\image_number_to_splitted_digits\{dir_name}"
        extract_digits(number_image_path, digits_images_path)

        for d in os.listdir(digits_images_path):
            digit_image_path = os.path.join(digits_images_path, d)
            data[dir_name] += predict_oc_image(label_map, loaded_model, digit_image_path)
    
    actual_data = {data_actual_names[i]: data[k] for i, k in enumerate(data)}
    
    print(actual_data)
    with open("invoice_ocr.json", 'w') as f:
        json.dump(actual_data, f, indent=4)
