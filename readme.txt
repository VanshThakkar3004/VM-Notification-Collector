Windows:

Download installer from:
https://github.com/UB-Mannheim/tesseract/wiki

During install:

Add to PATH ✔

Verify:

tesseract --version

🔹 Poppler (MANDATORY for pdf2image)

https://github.com/oschwartz10612/poppler-windows/releases

POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"

Verify:

pdftoppm -h
4️⃣ Recommended folder setup on new system

To avoid breaking paths, replicate this structure:

Notification_Collector/
│
├── convertpdf.py
├── detect_boxes.py
├── requirements.txt
│
└── newspapers/
    ├── input/          ← PDFs here
    ├── output/         ← auto-created (PDF → images)
    └── detected_boxes/ ← auto-created (final output)

5️⃣ One-command setup on new system
Step 1: Create venv (recommended)
python -m venv venv
venv\Scripts\activate

Step 2: Install everything
pip install -r requirements.txt

Step 3: Verify installs
python -c "import cv2, numpy, pytesseract, pdf2image, PIL; print('OK')"