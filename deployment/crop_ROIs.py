from config import CONFIG
import cv2
import os
import json



def crop_roi():
    try:
        img = cv2.imread(CONFIG["invoice_image_path"])
        if img is None:
            raise FileNotFoundError(f"Image not found at {CONFIG['invoice_image_path']}")

        with open(CONFIG["rois_json"], "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        os.makedirs(CONFIG["cropped_rois_dir"], exist_ok=True)

        for key, coords in data.items():
            x1, y1 = coords[0]
            x2, y2 = coords[1]

            roi = img[y1:y2, x1:x2]
            if roi.size == 0:
                print(f"Invalid ROI for key: {key}")
                continue

            cv2.imwrite(os.path.join(CONFIG["cropped_rois_dir"], f"ROI_{key}.jpg"), roi)

        print(f"ROIs cropped and saved in {CONFIG['cropped_rois_dir']} successfully.")

    except FileNotFoundError as fnf_error:
        print(f"File error: {fnf_error}")
    except Exception as e:
        print(f"Error in cropping ROIs: {e}")


if __name__ == "__main__":
    crop_roi()
