import os
import json
from ArabicOcr import arabicocr


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
    rois_path = "E:\Cloudilic assessment\images_to_ocr"
    # rois_path = "E:\Cloudilic assessment\processed_images"
    to_extract = ["invoice number", "date", "total amount", "second product cost"]
    extracted_data = []

    image_to_ocr(rois_path, ocr_img_output=True) 