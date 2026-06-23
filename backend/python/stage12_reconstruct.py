import os
import logging
import fitz  # PyMuPDF

# 1. SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def reconstruct_pdf(doc_folder, output_pdf_path):
    """
    Scans the cleaned images folder, sorts the pages numerically, 
    and binds them back into a single, high-resolution PDF document.
    """
    clean_dir = os.path.join(doc_folder, "cleaned_images")
    
    if not os.path.exists(clean_dir):
        logging.error(f"Cleaned images folder not found: {clean_dir}")
        return False

    # Get all clean images
    images = [img for img in os.listdir(clean_dir) if img.endswith("_clean.png")]
    
    if not images:
        logging.warning(f"No clean images found in {clean_dir}")
        return False
        
    # CRITICAL: Sort numerically so page_10 comes after page_9, not page_1
    # This splits "page_1_clean.png" to extract the integer 1
    images.sort(key=lambda x: int(x.split('_')[1]))

    # Create a new, blank PDF
    pdf_document = fitz.open()

    for img_name in images:
        img_path = os.path.join(clean_dir, img_name)
        
        # Open the image as a standalone PyMuPDF document
        img_doc = fitz.open(img_path)
        
        # Convert the raw image bytes natively into a PDF page (preserves resolution/orientation)
        pdf_bytes = img_doc.convert_to_pdf()
        img_pdf = fitz.open("pdf", pdf_bytes)
        
        # Insert the newly created page into our master document
        pdf_document.insert_pdf(img_pdf)
        
        # Clean up memory
        img_doc.close()
        img_pdf.close()

    # Save the final, perfectly bound PDF
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    return True

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    base_folder = "decomposed_docs"
    output_folder = "final_outputs"
    
    print("Starting Stage 12: PDF Reconstruction Service...\n")
    
    # Create a pristine directory just for the final deliverables
    os.makedirs(output_folder, exist_ok=True)
    
    if not os.path.exists(base_folder):
        print(f" Folder '{base_folder}' not found.")
    else:
        doc_folders = [f for f in os.listdir(base_folder) if f.startswith("doc_")]
        total_pdfs = 0
        
        for doc_folder in doc_folders:
            full_doc_path = os.path.join(base_folder, doc_folder)
            
            # Name the final file based on its batch ID (e.g., doc_001_clean.pdf)
            final_pdf_name = f"{doc_folder}_clean.pdf"
            output_pdf_path = os.path.join(output_folder, final_pdf_name)
            
            logging.info(f"Reconstructing {final_pdf_name}...")
            
            if reconstruct_pdf(full_doc_path, output_pdf_path):
                total_pdfs += 1

        print("="*45)
        print("  PIPELINE FULLY COMPLETE  ")
        print("="*45)
        print(f"Final Clean PDFs Generated: {total_pdfs}")
        print(f"Saved to: /{output_folder}/")
        print("="*45)