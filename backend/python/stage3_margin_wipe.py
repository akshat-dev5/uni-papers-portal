import os
import json
import logging
import cv2

# 1. SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def wipe_margins(image_path):
    """
    Reads the config.json file and paints pure white over the defined margins.
    This sanitizes the image before the AI models ever see it.
    """
    img = cv2.imread(image_path)
    if img is None:
        logging.error(f"Could not read image: {image_path}")
        return False

    h_img, w_img = img.shape[:2]
    
    # 2. LOAD CONFIGURATION
    top_percent, bottom_percent, left_percent, right_percent = 0.04, 0.04, 0.00, 0.00
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                active = config.get("active_profile", "default")
                profile = config["university_profiles"].get(active, config["university_profiles"]["default"])
                top_percent = profile.get("top_margin_percent", 0.04)
                bottom_percent = profile.get("bottom_margin_percent", 0.04)
                left_percent = profile.get("left_margin_percent", 0.00)
                right_percent = profile.get("right_margin_percent", 0.00)
    except Exception as e:
        logging.warning(f"Could not load config.json, using defaults. Error: {e}")

    # 3. CALCULATE PIXEL CUTOFFS
    top_cut = int(h_img * top_percent)
    bottom_cut = int(h_img * (1.0 - bottom_percent))
    left_cut = int(w_img * left_percent)
    right_cut = int(w_img * (1.0 - right_percent))
    
    # 4. EXECUTE THE 4-SIDED WIPE
    cv2.rectangle(img, (0, 0), (w_img, top_cut), (255, 255, 255), -1)           # Top
    cv2.rectangle(img, (0, bottom_cut), (w_img, h_img), (255, 255, 255), -1)    # Bottom
    cv2.rectangle(img, (0, 0), (left_cut, h_img), (255, 255, 255), -1)          # Left
    cv2.rectangle(img, (right_cut, 0), (w_img, h_img), (255, 255, 255), -1)     # Right
    
    # Save it back over the original file so the AI reads the clean version
    cv2.imwrite(image_path, img)
    return True

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    print("Starting Stage 3: Data Sanitization (Margin Wipe)...\n")
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        pages_wiped = 0
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            pages = [p for p in os.listdir(full_doc_path) if p.endswith(".png") and p.startswith("page_")]
            
            for page in pages:
                image_path = os.path.join(full_doc_path, page)
                if wipe_margins(image_path):
                    pages_wiped += 1
                        
        print("="*40)
        print(" DATA SANITIZATION COMPLETE ")
        print("="*40)
        print(f"Total Pages Pre-Processed: {pages_wiped}")