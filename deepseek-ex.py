import cv2
import easyocr
import re
from sys import argv


def preprocess_receipt(img_path):
    # Load image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("Image not loaded")

    # Preprocessing pipeline
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 15, 2)
    img = cv2.medianBlur(img, 3)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


# Preprocess
if len(argv) != 2:
    print(f"Usage: python3 {argv[0]} receipt_image_file_name")
    exit()

image = preprocess_receipt(argv[1])

# OCR with receipt-optimized settings
reader = easyocr.Reader(['en'])
results = reader.readtext(
    image,
    allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/$%.,:- ',  # Key symbols
    decoder='beamsearch',
    beamWidth=7,
    contrast_ths=0.2,
    adjust_contrast=0.8,
    width_ths=0.5,
    slope_ths=0.1,  # Force horizontal alignment
    paragraph=True,
)

# Post-processing
receipt_data = []
for (bbox, text) in results:
    # Fix common OCR errors
    # Separate letter-number combos
    text = re.sub(r'([A-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'[|]', '1', text)  # Fix pipe->1 confusion
    text = re.sub(r'O(\d)', r'0\1', text)  # O->0 replacement
    receipt_data.append(text)

# Extract key fields
prices = re.findall(r'\$\d+\.\d{2}', ' '.join(receipt_data))
subtotal = next((p for p in prices if float(
    p[1:]) > 200), None)  # $227.36 in example
items = [item for item in receipt_data if re.match(
    r'^\d+\.\d{2}[A-Z]?$', item)]

print(receipt_data)
print(items)
print(prices)
