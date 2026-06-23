import os
import json
import logging
import re

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


def boxes_overlap(box1, box2):
    """
    Check whether two bounding boxes overlap.
    Format: [x, y, w, h]
    """

    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    x1_max = x1 + w1
    y1_max = y1 + h1

    x2_max = x2 + w2
    y2_max = y2 + h2

    if x1_max < x2:
        return False

    if x2_max < x1:
        return False

    if y1_max < y2:
        return False

    if y2_max < y1:
        return False

    return True


if __name__ == "__main__":

    base_folder = "decomposed_docs"

    print("Starting Stage 8: Hybrid Detection Fusion...")
    print()

    if not os.path.exists(base_folder):
        print(f"Folder '{base_folder}' not found.")
        exit()

    doc_folders = [
        f for f in os.listdir(base_folder)
        if f.startswith("doc_")
    ]

    total_ocr_found = 0
    total_yolo_fallback = 0

    for doc_folder in doc_folders:

        full_doc_path = os.path.join(
            base_folder,
            doc_folder
        )

        verified_file = os.path.join(
            full_doc_path,
            "verified_watermarks.json"
        )

        verified_bad_texts = []

        if os.path.exists(verified_file):

            try:
                with open(
                    verified_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    verified_data = json.load(f)

                for item in verified_data:

                    if item.get("decision") == "REMOVE":

                        verified_bad_texts.append(
                            item.get("text", "")
                        )

            except Exception as e:

                logging.error(
                    f"Failed reading {verified_file}: {e}"
                )

        pages = [
            p for p in os.listdir(full_doc_path)
            if p.startswith("page_")
            and p.endswith(".png")
        ]

        for page in pages:

            base_name = page.replace(".png", "")

            ocr_file = os.path.join(
                full_doc_path,
                f"{base_name}_ocr.json"
            )

            yolo_file = os.path.join(
                full_doc_path,
                f"{base_name}_ml_fallback.json"
            )

            output_file = os.path.join(
                full_doc_path,
                f"{base_name}_final_watermarks.json"
            )

            ocr_data = []
            yolo_data = []

            if os.path.exists(ocr_file):

                try:
                    with open(
                        ocr_file,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        ocr_data = json.load(f)

                except Exception as e:

                    logging.error(
                        f"Failed reading OCR file {ocr_file}: {e}"
                    )

            if os.path.exists(yolo_file):

                try:
                    with open(
                        yolo_file,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        yolo_data = json.load(f)

                except Exception as e:

                    logging.error(
                        f"Failed reading YOLO file {yolo_file}: {e}"
                    )

            final_boxes = []

            url_pattern = re.compile(
                r"(www\.|http|\.com|\.in|\.org|\.net|\.edu)",
                re.IGNORECASE
            )

            # OCR Detection
            for item in ocr_data:

                text = str(
                    item.get("text", "")
                )

                bbox = item.get("bbox")

                if not bbox:
                    continue

                normalized_text = (
                    text.lower()
                    .replace(" ", "")
                )

                is_watermark = False

                if url_pattern.search(normalized_text):
                    is_watermark = True

                if not is_watermark:

                    for bad_text in verified_bad_texts:

                        clean_bad = (
                            str(bad_text)
                            .lower()
                            .replace(" ", "")
                        )

                        if (
                            normalized_text in clean_bad
                            or clean_bad in normalized_text
                        ):
                            is_watermark = True
                            break

                if is_watermark:

                    final_boxes.append({
                        "source": "OCR",
                        "bbox": bbox,
                        "text": text
                    })

                    total_ocr_found += 1

            # YOLO Fallback
            for yolo_item in yolo_data:

                try:

                    y_box = [
                        yolo_item["x"],
                        yolo_item["y"],
                        yolo_item["w"],
                        yolo_item["h"]
                    ]

                except Exception:
                    continue

                duplicate = False

                for existing in final_boxes:

                    if boxes_overlap(
                        y_box,
                        existing["bbox"]
                    ):
                        duplicate = True
                        break

                if not duplicate:

                    final_boxes.append({
                        "source": "YOLO_FALLBACK",
                        "bbox": y_box
                    })

                    total_yolo_fallback += 1

            try:

                with open(
                    output_file,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        final_boxes,
                        f,
                        indent=2,
                        ensure_ascii=False
                    )

            except Exception as e:

                logging.error(
                    f"Failed saving {output_file}: {e}"
                )

    print("=" * 50)
    print("HYBRID FUSION COMPLETE")
    print("=" * 50)
    print(
        f"Total Watermarks Mapped: "
        f"{total_ocr_found + total_yolo_fallback}"
    )
    print(
        f"OCR Detections: "
        f"{total_ocr_found}"
    )
    print(
        f"YOLO Fallback Detections: "
        f"{total_yolo_fallback}"
    )
    print("=" * 50)