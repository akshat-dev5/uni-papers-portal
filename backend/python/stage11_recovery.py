import os
import json
import logging
import cv2
import numpy as np

# Import your QA engine from Stage 10 to grade the recovery attempts
from stage10_qa import validate_damage

# 1. SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def apply_recovery_method(method_name, img, watermarks):
    """
    Applies one of three specific fallback strategies to remove watermarks 
    with minimal collateral damage to the surrounding text.
    """
    h_img, w_img = img.shape[:2]
    result_img = img.copy()
    inpaint_mask = np.zeros((h_img, w_img), dtype=np.uint8)
    needs_inpainting = False

    for wm in watermarks:
        # METHOD B: Ignore YOLO, only use OCR
        if method_name == "Method_B_OCR_Only" and wm.get('source') == "YOLO_FALLBACK":
            continue

        x, y, w, h = wm['bbox']
        
        # METHOD A: Zero Padding (Surgical precision)
        pad = 0 if method_name == "Method_A_Precision" else 2
        x1, y1 = max(0, x - pad), max(0, y - pad)
        x2, y2 = min(w_img, x + w + pad), min(h_img, y + h + pad)

        # METHOD C: White Fill Only (No inpainting)
        if method_name == "Method_C_WhiteFill":
            cv2.rectangle(result_img, (x1, y1), (x2, y2), (255, 255, 255), -1)
        else:
            cv2.rectangle(inpaint_mask, (x1, y1), (x2, y2), 255, -1)
            needs_inpainting = True

    if needs_inpainting:
        if method_name == "Method_A_Precision":
            # TELEA is mathematically tighter than Navier-Stokes (NS)
            result_img = cv2.inpaint(result_img, inpaint_mask, inpaintRadius=2, flags=cv2.INPAINT_TELEA)
        else:
            result_img = cv2.inpaint(result_img, inpaint_mask, inpaintRadius=4, flags=cv2.INPAINT_NS)

    return result_img

def auto_recover_page(doc_folder_path, base_name, original_ocr_file, clean_img_path):
    """
    Triggers the recovery loop. Tries A, then B, then C. 
    Stops early if a method achieves a 'PASS' score.
    """
    orig_img_path = os.path.join(doc_folder_path, f"{base_name}.png")
    watermarks_file = os.path.join(doc_folder_path, f"{base_name}_final_watermarks.json")
    
    if not os.path.exists(orig_img_path) or not os.path.exists(watermarks_file):
        return False

    orig_img = cv2.imread(orig_img_path)
    with open(watermarks_file, 'r', encoding='utf-8') as f:
        watermarks = json.load(f)

    methods = ["Method_A_Precision", "Method_B_OCR_Only", "Method_C_WhiteFill"]
    best_retention = 0.0
    best_img = None
    best_report = None

    for method in methods:
        logging.info(f"    -> Attempting {method}...")
        
        # 1. Generate the temporary recovery image
        temp_img = apply_recovery_method(method, orig_img, watermarks)
        temp_path = clean_img_path.replace(".png", "_temp.png")
        cv2.imwrite(temp_path, temp_img)
        
        # 2. Grade it using Stage 10 QA
        report = validate_damage(original_ocr_file, temp_path)
        
        # Clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # 3. Analyze the results
        if report:
            # Extract word retention percentage (e.g., "98.5%" -> 98.5)
            retention_str = report['metrics']['retention']['words'].replace('%', '')
            retention_score = float(retention_str)

            # If it's the best we've seen so far, save it
            if retention_score > best_retention:
                best_retention = retention_score
                best_img = temp_img
                best_report = report

            # If we achieved a PASS, stop fighting! The page is saved.
            if "PASS" in report["status"]:
                logging.info(f"  Recovery successful using {method}! (Retention: {retention_score}%)")
                break

    # 4. Save the absolute best result (even if it's still slightly failing)
    if best_img is not None:
        cv2.imwrite(clean_img_path, best_img)
        report_path = clean_img_path.replace(".png", "_qa_report.json")
        
        # Tag the report so we know it was recovered
        best_report["recovery_applied"] = True
        best_report["final_retention"] = f"{best_retention}%"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(best_report, f, indent=4)
            
        return True
        
    return False

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    print("Starting Stage 11: Auto-Recovery System...\n")
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        
        total_recovered = 0
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            clean_dir = os.path.join(full_doc_path, "cleaned_images")
            
            if not os.path.exists(clean_dir):
                continue
                
            # Find all QA reports to see which pages failed
            qa_reports = [r for r in os.listdir(clean_dir) if r.endswith("_qa_report.json")]
            
            for report_file in qa_reports:
                report_path = os.path.join(clean_dir, report_file)
                
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                    
                # If the page failed, trigger the Self-Healing sequence
                if "FAIL" in report_data.get("status", "") and not report_data.get("recovery_applied", False):
                    base_name = report_file.replace("_qa_report.json", "")
                    orig_ocr_file = os.path.join(full_doc_path, f"{base_name}_ocr.json")
                    clean_img_path = os.path.join(clean_dir, f"{base_name}_clean.png")
                    
                    logging.info(f"  Failure detected in {doc_folder}/{base_name}. Initiating Self-Healing Protocol...")
                    
                    if auto_recover_page(full_doc_path, base_name, orig_ocr_file, clean_img_path):
                        total_recovered += 1

        print("="*40)
        print(" AUTO-RECOVERY COMPLETE ")
        print("="*40)
        print(f"Pages Successfully Recovered: {total_recovered}")
        print("="*40)