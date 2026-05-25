import os
import cv2
import pytesseract
import numpy as np
# ================= CONFIG =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 🔥 FIXED PATH (matches your PDF → Image pipeline)
TEMP_IMG_DIR = os.path.join(BASE_DIR, "newspapers", "output")

OUTPUT_DIR = os.path.join(BASE_DIR, "detected_boxes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tesseract explicit path (safe)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

MIN_W, MIN_H = 300, 150

EDU_KEYWORDS = [ "notice", "notification", "advertisement",
    "admission", "exam", "university", "college",
    "recruitment", "vacancy", "apply",
    "result", "scholarship", "degree",
    "ugc", "cbse", "neet", "jee", "gate",
    "rs", "date", "no", "ref", "contact"
]
def safe_ocr(img):
    try:
        return pytesseract.image_to_string(img, config="--psm 6")
    except Exception:
        return ""


def detect_boxes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thr = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dil = cv2.dilate(thr, kernel, iterations=2)

    cnts, _ = cv2.findContours(
        dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    boxes = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        aspect = w / float(h)

        if w > MIN_W and h > MIN_H and 0.3 < aspect < 4.0:
            boxes.append((x, y, w, h))

    return boxes


def looks_like_photo(crop):
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    return np.std(hsv[:, :, 1]) > 40


def is_notice_text(text):
    lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 3]

    if len(lines) < 5:
        return False

    avg_len = np.mean([len(l) for l in lines])
    if avg_len > 90:
        return False

    digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)
    if digit_ratio < 0.025:
        return False

    period_lines = sum(1 for l in lines if l.endswith("."))
    if period_lines / len(lines) > 0.45:
        return False

    first_block = " ".join(lines[:5]).lower()
    if not any(k in first_block for k in EDU_KEYWORDS):
        return False

    return True


def process_page(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return

    parent = os.path.basename(os.path.dirname(img_path))
    base = f"{parent}_{os.path.splitext(os.path.basename(img_path))[0]}"

    boxes = detect_boxes(img)
    print(f"🔍 {base}: detected {len(boxes)} candidate boxes")

    saved = 0

    for x, y, w, h in boxes:
        crop = img[y:y+h, x:x+w]

        if looks_like_photo(crop):
            continue

        text = safe_ocr(crop)

        if not is_notice_text(text):
            continue

        out_path = os.path.join(
            OUTPUT_DIR, f"{base}_notice_{saved}.png"
        )
        cv2.imwrite(out_path, crop)
        saved += 1

    print(f"✅ Saved {saved} notices\n")


def main():
    print("\nStarting notification extraction...\n")
    print("📂 Image root:", TEMP_IMG_DIR) 

    total_images = 0

    for root, _, files in os.walk(TEMP_IMG_DIR):
        for file in files:
            if file.lower().endswith(".png"):
                img_path = os.path.join(root, file)
                print("Processing:", img_path)
                process_page(img_path)
                total_images += 1

    print(f"\n🚀 Done. Processed {total_images} images.")


if __name__ == "__main__":
    main()
