import os
import json
import logging
from ultralytics import YOLO

# 1. SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_watermark_yolo(image_path, model_path="best.pt", conf_thresh=0.4):
    """
    Runs your custom trained YOLOv8 object detection model as a fallback 
    when OCR fails. Returns bounding boxes in exact {x, y, w, h} format.
    """
    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        return None

    # 2. LOAD YOUR CUSTOM TRAINED MODEL
    if not os.path.exists(model_path):
        logging.error(f"Could not find model weights file: {model_path}. "
                      f"Please copy 'best.pt' into your project directory!")
        return None

    try:
        model = YOLO(model_path)
    except Exception as e:
        logging.error(f"Failed to load YOLO model: {e}")
        return None

    logging.info(f"Running ML Fallback on {image_path} using custom weights ({model_path})...")
    
    # 3. RUN INFERENCE
    # verbose=False stops it from printing cluttering debug lines to the terminal
    results = model.predict(source=image_path, conf=conf_thresh, verbose=False)

    extracted_elements = []

    # 4. PARSE YOLO OUTPUT TENSORS
    if results and len(results) > 0:
        boxes = results[0].boxes
        
        for box in boxes:
            # YOLO provides coordinates in xyxy format 
            # (top-left X, top-left Y, bottom-right X, bottom-right Y)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            # Convert to standard x, y, width, height requested by the task
            x = int(x1)
            y = int(y1)
            w = int(x2 - x1)
            h = int(y2 - y1)
            
            extracted_elements.append({
                "x": x,
                "y": y,
                "w": w,
                "h": h
            })

    return extracted_elements

def save_ml_results(data, output_path):
    """Saves the YOLO detections into a JSON file."""
    if data is not None:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Successfully saved {len(data)} ML detections to {output_path}")

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        print(f"Found {len(doc_folders)} documents. Starting ML Fallback...\n")
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            pages = [p for p in os.listdir(full_doc_path) if p.endswith(".png") and p.startswith("page_")]
            
            for page in pages:
                image_path = os.path.join(full_doc_path, page)
                json_name = page.replace(".png", "_ml_fallback.json")
                output_json = os.path.join(full_doc_path, json_name)
                
                print(f"Running YOLO on: {image_path}")
                detections = detect_watermark_yolo(image_path, model_path="best.pt")
                save_ml_results(detections, output_json)
                
        print("\n Batch ML Fallback complete!")