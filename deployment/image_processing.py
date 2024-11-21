import cv2
import os
import numpy as np
from config import CONFIG


def convert_to_grayscale(image_path):
    gray = cv2.imread(image_path, 0)
    return gray

def binarize_image(gray_image):
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_image


def resize_image(image, width=800):
    height = int(image.shape[0] * (width / image.shape[1]))
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def detect_text_region(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 100 and h > 20:  # Filter out small contours
            roi = image[y:y+h, x:x+w]
            # Do OCR on the ROI or process further
    return image

def invert_image(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image

def edge_detection(image):
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    return edges

def save_image(image, output_path):
    cv2.imwrite(output_path, image)




def preprocess_image(image_path):
    """
    Preprocesses an image by converting it to grayscale, binarizing it,
    and resizing it for further processing.
    """
    try:
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise FileNotFoundError(f"Image not found at {image_path}")

        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        resized = cv2.resize(binary, (800, int(binary.shape[0] * 800 / binary.shape[1])))
        inverted = cv2.bitwise_not(resized)

        save_path = os.path.join(CONFIG["processed_images_dir"], os.path.basename(image_path))
        os.makedirs(CONFIG["processed_images_dir"], exist_ok=True)
        cv2.imwrite(save_path, inverted)
        # print("Image successfully processed and saved in [processed_images]")

        return save_path

    except Exception as e:
        print(f"Error preprocessing image {image_path}: {e}")
        return None


def preprocess_all_images():
    try:
        input_folder = CONFIG["cropped_rois_dir"]
        os.makedirs(CONFIG["processed_images_dir"], exist_ok=True)

        for filename in os.listdir(input_folder):
            if '2' in filename or '3' in filename:
                image_path = os.path.join(input_folder, filename)
                preprocess_image(image_path)

    except Exception as e:
        print(f"Error preprocessing all images: {e}")


if __name__ == "__main__":
    preprocess_all_images()