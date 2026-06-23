import os
import json
import sqlite3
import logging
from datetime import datetime

# 1. SETUP LOGGING & DATABASE
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
DB_PATH = "mlops_telemetry.db"

def setup_database():
    """Initializes the SQLite database to store pipeline telemetry."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the telemetry table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watermark_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            document_id TEXT,
            page_id TEXT,
            watermark_text TEXT,
            source TEXT,
            bbox_x INTEGER,
            bbox_y INTEGER,
            bbox_w INTEGER,
            bbox_h INTEGER,
            qa_status TEXT,
            recovery_triggered BOOLEAN,
            final_retention_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_page_telemetry(doc_folder, base_name):
    """
    Reads the final states of a processed page and logs the metadata to SQL.
    """
    watermarks_file = os.path.join(doc_folder, f"{base_name}_final_watermarks.json")
    qa_report_file = os.path.join(doc_folder, "cleaned_images", f"{base_name}_qa_report.json")
    
    if not os.path.exists(watermarks_file) or not os.path.exists(qa_report_file):
        return 0

    with open(watermarks_file, 'r', encoding='utf-8') as f:
        watermarks = json.load(f)
        
    with open(qa_report_file, 'r', encoding='utf-8') as f:
        qa_report = json.load(f)

    # Extract QA Data
    status = qa_report.get("status", "UNKNOWN")
    recovery_triggered = qa_report.get("recovery_applied", False)
    
    # Handle retention score parsing safely
    retention_str = qa_report.get("final_retention", qa_report.get("metrics", {}).get("retention", {}).get("words", "0%"))
    retention_score = float(retention_str.replace('%', ''))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    records_inserted = 0

    doc_id = os.path.basename(doc_folder)

    for wm in watermarks:
        text = wm.get('text', 'N/A')
        source = wm.get('source', 'UNKNOWN')
        x, y, w, h = wm['bbox']
        
        cursor.execute('''
            INSERT INTO watermark_telemetry 
            (timestamp, document_id, page_id, watermark_text, source, bbox_x, bbox_y, bbox_w, bbox_h, qa_status, recovery_triggered, final_retention_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), doc_id, base_name, text, source, x, y, w, h, status, recovery_triggered, retention_score))
        
        records_inserted += 1

    conn.commit()
    conn.close()
    return records_inserted

def export_failed_data_for_retraining():
    """
    Queries the database for all pages that completely failed QA.
    This tells you exactly which images you need to upload to Roboflow 
    to train your next version of YOLO!
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT document_id, page_id, watermark_text, bbox_x, bbox_y, bbox_w, bbox_h 
        FROM watermark_telemetry 
        WHERE qa_status LIKE '%FAIL%' OR recovery_triggered = 1
    ''')
    
    failures = cursor.fetchall()
    conn.close()
    
    if failures:
        print("\n--- RETRAINING TARGETS IDENTIFIED ---")
        print(f"Found {len(failures)} problematic watermarks the current model struggled with.")
        print("Gather these original pages to train Version 2.0:")
        for f in failures[:5]: # Print first 5 as a preview
            print(f" -> {f[0]}/{f[1]}.png (Text: {f[2]} at [{f[3]},{f[4]},{f[5]},{f[6]}])")
        if len(failures) > 5:
            print(f" ... and {len(failures) - 5} more.")

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    
    print("Starting Stage 13: Self-Learning Telemetry Sync...\n")
    setup_database()
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        total_logs = 0
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            pages = [p for p in os.listdir(full_doc_path) if p.endswith(".png") and p.startswith("page_")]
            
            for page in pages:
                base_name = page.replace(".png", "")
                total_logs += log_page_telemetry(full_doc_path, base_name)
                
        print("="*40)
        print(" TELEMETRY SYNC COMPLETE ")
        print("="*40)
        print(f"New Data Points Added to Flywheel: {total_logs}")
        
        # Check if we have enough failures to warrant retraining
        export_failed_data_for_retraining()
        print("="*40)