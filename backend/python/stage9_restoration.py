import os
import json
import logging
import cv2
import numpy as np

# 1. SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def process_lama_inpaint(image, mask):
    """
    Placeholder for LaMa (Large Mask Inpainting) Deep Learning Model.
    LaMa requires PyTorch and pre-trained weights. Until configured, 
    this falls back to OpenCV's Navier-Stokes inpainting.
    """
    # TODO: Initialize LaMa model here in the future
    # return lama_model.predict(image, mask)
    
    logging.info("  -> [LaMa Stub] Falling back to OpenCV Inpaint for complex mark.")
    return cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_NS)

def restore_image(image_path, watermarks, output_path):
    """
    Applies the adaptive decision tree to remove visual watermarks from the PNG.
    """
    img = cv2.imread(image_path)
    if img is None:
        logging.error(f"Could not read image: {image_path}")
        return False

    h_img, w_img = img.shape[:2]
    
    inpaint_mask = np.zeros((h_img, w_img), dtype=np.uint8)
    needs_inpainting = False

    for wm in watermarks:
        x, y, w, h = wm['bbox']
        
        pad = 8
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(w_img, x + w + pad)
        y2 = min(h_img, y + h + pad)

        is_small_text = ((w * h) < (h_img * w_img * 0.02)) and (h < 60)

        if is_small_text:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), -1)
        else:
            cv2.rectangle(inpaint_mask, (x1, y1), (x2, y2), 255, -1)
            needs_inpainting = True

    if needs_inpainting:
        img = process_lama_inpaint(img, inpaint_mask)

    cv2.imwrite(output_path, img)
    return True

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    print("Starting Stage 9: Adaptive Visual Restoration Engine...\n")
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        pages_cleaned = 0
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            
            # Create a subfolder to hold the final cleaned images
            clean_output_dir = os.path.join(full_doc_path, "cleaned_images")
            os.makedirs(clean_output_dir, exist_ok=True)
            
            # Find all original pages
            pages = [p for p in os.listdir(full_doc_path) if p.endswith(".png") and p.startswith("page_")]
            
            for page in pages:
                base_name = page.replace(".png", "")
                image_path = os.path.join(full_doc_path, page)
                watermarks_file = os.path.join(full_doc_path, f"{base_name}_final_watermarks.json")
                output_path = os.path.join(clean_output_dir, f"{base_name}_clean.png")
                
                # Check if we have watermarks mapped for this page
                if os.path.exists(watermarks_file):
                    with open(watermarks_file, 'r', encoding='utf-8') as f:
                        watermarks = json.load(f)
                    
                    if watermarks:
                        print(f"Restoring: {doc_folder} -> {page}")
                        if restore_image(image_path, watermarks, output_path):
                            pages_cleaned += 1
                    else:
                        # No watermarks found, just copy the image over
                        img = cv2.imread(image_path)
                        cv2.imwrite(output_path, img)
                        
        print("="*40)
        print(" RESTORATION COMPLETE ")
        print("="*40)
        print(f"Total Pages Visually Cleaned: {pages_cleaned}")