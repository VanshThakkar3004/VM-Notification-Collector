import os
from pdf2image import convert_from_path
from PIL import Image

# ==================================================
# SAFETY OVERRIDE (WE TRUST OUR PDFs)
# ==================================================
Image.MAX_IMAGE_PIXELS = None

# ================= CONFIG =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NEWSPAPER_DIR = os.path.join(BASE_DIR, "newspapers")
INPUT_DIR = os.path.join(NEWSPAPER_DIR, "input")
OUTPUT_DIR = os.path.join(NEWSPAPER_DIR, "output")

# 🔥 Lower DPI – enough for OCR & box detection
DPI = 300

POPPLER_PATH = r"C:\Program Files\poppler-25.12.0\Library\bin"

# =========================================
# Ensure required directories exist
# =========================================

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_pdf(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_subdir = os.path.join(OUTPUT_DIR, pdf_name)
    os.makedirs(output_subdir, exist_ok=True)

    print(f"→ Converting: {pdf_name}.pdf")

    pages = convert_from_path(
        pdf_path=pdf_path,
        dpi=DPI,
        poppler_path=POPPLER_PATH
    )

    for i, page in enumerate(pages, start=1):
        out_path = os.path.join(output_subdir, f"page_{i}.png")
        page.save(out_path, "PNG")

    print(f"✔ Saved {len(pages)} pages to {output_subdir}\n")


def main():
    pdfs = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    if not pdfs:
        print(f"⚠ No PDFs found in: {INPUT_DIR}")
        return

    for pdf in pdfs:
        convert_pdf(os.path.join(INPUT_DIR, pdf))

    print("🚀 All PDFs converted successfully!")


if __name__ == "__main__":
    print("📂 Script location:", BASE_DIR)
    print("📂 Input directory:", INPUT_DIR)
    print("📂 Output directory:", OUTPUT_DIR)
    print("-" * 50)
    main()