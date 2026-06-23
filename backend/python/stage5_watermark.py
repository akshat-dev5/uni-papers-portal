import os
import json
import glob

def detect_watermarks(doc_folder):
    """
    Scans all OCR JSON files in a document folder, applies heuristic rules, 
    and generates a list of watermark candidates with confidence scores.
    """
    # 1. FIND ALL PAGES
    json_files = glob.glob(os.path.join(doc_folder, "*_ocr.json"))
    total_pages = len(json_files)
    
    if total_pages == 0:
        return {"error": "No OCR JSON files found in directory."}

    # 2. GATHER DATA & CALCULATE FREQUENCIES
    text_frequencies = {}
    text_dimensions = {} 

    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Keep track of words seen ON THIS PAGE so we don't double count 
            # if a watermark repeats twice on page 1.
            seen_on_page = set()
            
            for item in data:
                text = item['text'].strip() 
                bbox = item['bbox']
                
                # We use lowercase for the rules, but keep original for output
                lower_text = text.lower()
                
                if lower_text not in seen_on_page:
                    text_frequencies[text] = text_frequencies.get(text, 0) + 1
                    seen_on_page.add(lower_text)
                
                # Save the dimensions to check for rotation later
                text_dimensions[text] = bbox

    # 3. APPLY RULES & SCORE CANDIDATES
    candidates = []
    url_keywords = ['www', '.com', '.in', '.org',"www."]

    for text, count in text_frequencies.items():
        confidence = 0.0
        lower_text = text.lower()
        
        # Rule 1: Contains URL Indicators (Strongest flag)
        if any(keyword in lower_text for keyword in url_keywords):
            confidence += 0.50
            
        # Rule 2: Appears on Many Pages (e.g., > 50% of the document)
        if (count / total_pages) > 0.5:
            confidence += 0.35
            
        # Rule 3: Extreme Rotation (Height > Width)
        bbox = text_dimensions[text]
        w, h = bbox[2], bbox[3]
        if h > w: 
            confidence += 0.15
            
        # 4. FILTER AND FORMAT
        # If confidence hits a certain threshold, flag it as a candidate
        if confidence >= 0.35: 
            candidates.append({
                "candidate": text,
                "confidence": round(min(confidence, 0.99), 2) # Cap at 0.99
            })

    # Sort the final list so the highest confidence is at the top
    candidates = sorted(candidates, key=lambda x: x['confidence'], reverse=True)
    return candidates

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        print(f"Found {len(doc_folders)} documents. Generating candidates...\n")
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            output_file = os.path.join(full_doc_path, "watermark_candidates.json")
            
            print(f"Analyzing candidates in: {doc_folder}")
            results = detect_watermarks(full_doc_path)
            
            # Save if it successfully processed without errors
            if "error" not in results:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                    
        print("\n Batch Candidate Generation complete!")