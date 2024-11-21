import os
from PIL import Image
from ArabicOcr import arabicocr



# Function to extract digits using Tesseract OCR
def image_to_ocr(rois_path, ocr_img_output=False):
    imgs_path = [os.path.join(rois_path, img) for img in os.listdir(rois_path)]

    for image_path in imgs_path:
        if ocr_img_output:
            out_image= 'out_' + image_path.split('\\')[-1]
            results = arabicocr.arabic_ocr(image_path, out_image)
            print(results)
        else:
            results = arabicocr.arabic_ocr(image_path)
            print(results)
        
        item = [item[1] for item in results]
        extracted_data.append(item)


    data = dict(zip(to_extract, extracted_data))
    print(data)


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
