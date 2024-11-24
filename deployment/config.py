import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

CONFIG = {
    "invoice_image_path": os.path.join(BASE_DIR, "data/Invoices", "Invoice arabic.jpeg"),
    "invoices_save_dir": os.path.join(BASE_DIR, "data/Invoices"),
    "cropped_rois_dir": os.path.join(BASE_DIR, "data", "cropped_rois"),
    "processed_images_dir": os.path.join(BASE_DIR, "data", "processed_images"),
    "rois_json": os.path.join(BASE_DIR, "data", "coordinates_data.json"),
    "tesseract_cmd": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    "torch_model_path": os.path.join(BASE_DIR, "models", "ocr_model_traced.pt"),
    "digits_dir": os.path.join(BASE_DIR, "data", "image_number_to_splitted_digits"),
    "output_json": os.path.join(BASE_DIR, "data/output", "invoice_ocr.json"),
    "credentials_path": os.path.join(BASE_DIR, "secrets", "credentials.json"),
    "service_account_path": os.path.join(BASE_DIR, "secrets", "service_account.json"),
    "token_path": os.path.join(BASE_DIR, "secrets", "token.json"),
}
