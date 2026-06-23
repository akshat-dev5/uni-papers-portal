import os
import json
import logging
from paddleocr import PaddleOCR

# =====================================================
# LOGGING
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =====================================================
# INITIALIZE OCR ONCE
# =====================================================
logging.info("Initializing PaddleOCR engine once...")

try:
    ocr_engine = PaddleOCR(
        use_textline_orientation=True,
        lang='en',
        ocr_version='PP-OCRv3',
        enable_mkldnn=False
    )
    logging.info("PaddleOCR initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize PaddleOCR: {e}")
    raise

# =====================================================
# OCR EXTRACTION
# =====================================================
def extract_text_from_image(image_path):
    """
    Runs PaddleOCR on an image and converts results into:
    {
        "text": "...",
        "bbox": [x, y, w, h]
    }
    """

    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        return []

    try:
        logging.info(f"Scanning image: {image_path}")

        result = ocr_engine.ocr(image_path)

        extracted_elements = []

        if result and len(result) > 0:

            page_data = result[0]

            try:
                page_dict = dict(page_data)

                texts = page_dict.get("rec_texts", [])
                polys = page_dict.get("rec_polys", [])

                for text, poly in zip(texts, polys):

                    x_coords = [int(point[0]) for point in poly]
                    y_coords = [int(point[1]) for point in poly]

                    x = min(x_coords)
                    y = min(y_coords)
                    w = max(x_coords) - x
                    h = max(y_coords) - y

                    extracted_elements.append({
                        "text": str(text),
                        "bbox": [x, y, w, h]
                    })

            except Exception as parse_error:
                logging.error(
                    f"Failed to parse OCR structure for {image_path}: {parse_error}"
                )

        return extracted_elements

    except Exception as ocr_error:
        logging.error(
            f"OCR failed for {image_path}: {ocr_error}"
        )
        return []

# =====================================================
# SAVE OCR JSON
# =====================================================
def save_ocr_results(data, output_path):

    if data is None:
        data = []

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

        logging.info(
            f"Successfully saved {len(data)} text elements to {output_path}"
        )

    except Exception as e:
        logging.error(
            f"Failed to save OCR results to {output_path}: {e}"
        )

# =====================================================
# BATCH EXECUTION
# =====================================================
if __name__ == "__main__":

    base_folder = "decomposed_docs"

    if not os.path.exists(base_folder):
        print(f"Folder '{base_folder}' not found.")
        exit()

    doc_folders = [
        f for f in os.listdir(base_folder)
        if f.startswith("doc_")
    ]

    print(
        f"Found {len(doc_folders)} documents. Starting batch OCR...\n"
    )

    total_pages = 0

    for doc_folder in doc_folders:

        full_doc_path = os.path.join(
            base_folder,
            doc_folder
        )

        pages = sorted([
            p for p in os.listdir(full_doc_path)
            if p.endswith(".png")
            and p.startswith("page_")
        ])

        for page in pages:

            image_path = os.path.join(
                full_doc_path,
                page
            )

            json_name = page.replace(
                ".png",
                "_ocr.json"
            )

            output_json = os.path.join(
                full_doc_path,
                json_name
            )

            print(f"Scanning: {image_path}")

            ocr_data = extract_text_from_image(
                image_path
            )

            save_ocr_results(
                ocr_data,
                output_json
            )

            total_pages += 1

    print("\n========================================")
    print(" OCR COMPLETE ")
    print("========================================")
    print(f"Pages Processed: {total_pages}")
    print("========================================")