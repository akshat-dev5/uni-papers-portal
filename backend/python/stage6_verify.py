import os
import json
import glob
import statistics

def verify_watermarks(doc_folder, threshold=70):
    """
    Evaluates watermark candidates by checking their physical positions, 
    size consistency, and distribution across the document.
    """
    candidates_file = os.path.join(doc_folder, "watermark_candidates.json")
    
    if not os.path.exists(candidates_file):
        print(f"Error: Could not find {candidates_file}. Run Stage 5 first.")
        return

    # Load the candidates flagged in Stage 5
    with open(candidates_file, 'r', encoding='utf-8') as f:
        candidates_data = json.load(f)
        
    # Extract just the text strings to verify
    target_texts = [item['candidate'] for item in candidates_data]
    
    # Load all page data
    json_files = glob.glob(os.path.join(doc_folder, "*_ocr.json"))
    total_pages = len(json_files)
    
    if total_pages == 0:
        return

    # Track metrics for each candidate
    # candidate_text -> { "pages_appeared_on": set(), "y_positions": [], "heights": [], "max_per_page": 0 }
    metrics = {text: {"pages": set(), "y_positions": [], "heights": [], "max_per_page": 0} for text in target_texts}

    # 1. GATHER ALL PHYSICAL METRICS
    for page_num, file_path in enumerate(json_files):
        with open(file_path, 'r', encoding='utf-8') as f:
            page_data = json.load(f)
            
            # Estimate the page height by finding the lowest piece of text on the page
            page_height = max([item['bbox'][1] + item['bbox'][3] for item in page_data]) if page_data else 1000
            
            # Count occurrences of candidates on THIS specific page
            page_counts = {text: 0 for text in target_texts}
            
            for item in page_data:
                text = item['text'].strip()
                if text in target_texts:
                    metrics[text]["pages"].add(page_num)
                    page_counts[text] += 1
                    
                    # Calculate relative Y position (0.0 is top, 1.0 is bottom)
                    y_center = item['bbox'][1] + (item['bbox'][3] / 2)
                    relative_y = y_center / page_height
                    metrics[text]["y_positions"].append(relative_y)
                    
                    # Track height (proxy for font size)
                    metrics[text]["heights"].append(item['bbox'][3])
            
            # Update max repetitions per page
            for text, count in page_counts.items():
                if count > metrics[text]["max_per_page"]:
                    metrics[text]["max_per_page"] = count

    # 2. CALCULATE FINAL SCORES
    verified_watermarks = []
    
    for text, data in metrics.items():
        score = 0
        
        # Check 1: Frequency across pages (Max 40 points)
        # E.g., if on 100% of pages -> 40 pts. If on 50% -> 20 pts.
        page_ratio = len(data["pages"]) / total_pages
        score += (page_ratio * 40)
        
        # Check 2: Margin Position (Max 30 points)
        # Watermarks live at the edges. Is the average position in the top 12% or bottom 12%?
        if data["y_positions"]:
            avg_y = statistics.mean(data["y_positions"])
            if avg_y < 0.12 or avg_y > 0.88:
                score += 30
            # Sometimes diagonal watermarks sit dead center
            elif 0.45 < avg_y < 0.55:
                score += 15 
                
        # Check 3: Font/Size Consistency (Max 20 points)
        # If the standard deviation of the height is very low, it's the exact same stamp.
        if len(data["heights"]) > 1:
            size_variance = statistics.stdev(data["heights"])
            if size_variance < 3.0: # Height varies by less than 3 pixels
                score += 20
        elif len(data["heights"]) == 1:
             score += 10 # Default points if it only appeared once
             
        # Check 4: Repetition (Max 10 points)
        if data["max_per_page"] > 1:
            score += 10
            
        # --- NEW: AUTO-KILL OVERRIDE ---
        url_keywords = ['www', '.com', '.in', '.org']
        if any(keyword in text.lower() for keyword in url_keywords):
            score += 100 # Instantly max out the score to force removal
             
        final_score = int(min(score, 100)) # Cap at 100
        
        # 3. APPLY THRESHOLD
        decision = "REMOVE" if final_score >= threshold else "KEEP (Legitimate Text)"
        
        verified_watermarks.append({
            "text": text,
            "score": final_score,
            "decision": decision,
            "metrics": {
                "page_coverage": f"{int(page_ratio * 100)}%",
                "avg_margin_position": round(avg_y, 2) if data["y_positions"] else 0
            }
        })

    # Sort so the most definite watermarks are at the top
    verified_watermarks = sorted(verified_watermarks, key=lambda x: x['score'], reverse=True)
    return verified_watermarks

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        print(f"Found {len(doc_folders)} documents. Starting Verification...\n")
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            output_file = os.path.join(full_doc_path, "verified_watermarks.json")
            
            print(f"Verifying watermarks in: {doc_folder}")
            results = verify_watermarks(full_doc_path, threshold=70)
            
            if results:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                    
        print("\n Batch Verification complete!")