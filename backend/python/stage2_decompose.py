import os
import fitz  # PyMuPDF
import logging

# 1. SETUP LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_next_doc_id(output_root):
    """
    Looks at the output folder and calculates the next available ID.
    If doc_001 and doc_002 exist, it returns 'doc_003'.
    """
    os.makedirs(output_root, exist_ok=True)
    existing_folders = [f for f in os.listdir(output_root) if f.startswith("doc_")]
    
    if not existing_folders:
        return "doc_001"
        
    highest_num = 0
    for folder in existing_folders:
        try:
            # Splits "doc_005" into ["doc", "005"] and grabs the number
            num = int(folder.split('_')[1])
            highest_num = max(highest_num, num)
        except ValueError:
            continue
            
    # Format with leading zeros (e.g., 001, 002, 010)
    next_num = highest_num + 1
    return f"doc_{next_num:03d}"

def decompose_pdf(pdf_file_path, output_root="decomposed_docs", dpi=300):
    """
    Takes a PDF, extracts each page, standardizes to a specific DPI, 
    and saves them as PNGs in a standardized doc_XXX folder.
    """
    if not os.path.exists(pdf_file_path):
        logging.error(f"Cannot find PDF file: {pdf_file_path}")
        return

    # 2. CREATE THE STANDARDIZED FOLDER (doc_001, doc_002, etc.)
    doc_id = get_next_doc_id(output_root)
    doc_folder = os.path.join(output_root, doc_id)
    os.makedirs(doc_folder, exist_ok=True)
    
    logging.info(f"Target folder ready: {doc_folder}/")

    # 3. PROCESS THE PDF
    try:
        pdf_document = fitz.open(pdf_file_path)
        total_pages = len(pdf_document)
        logging.info(f"Processing '{os.path.basename(pdf_file_path)}' into '{doc_id}' - Found {total_pages} pages.")

        for page_number in range(total_pages):
            page = pdf_document.load_page(page_number)
            image = page.get_pixmap(dpi=dpi)
            
            image_filename = f"page_{page_number + 1}.png"
            image_path = os.path.join(doc_folder, image_filename)
            
            image.save(image_path)

        pdf_document.close()
        logging.info(f"Successfully decomposed into {doc_folder}\n")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file_path}. Error: {str(e)}")

# --- BATCH EXECUTION ---
if __name__ == "__main__":
    # We point the script to the folder where you keep all your PDFs
    input_folder = "input_pdfs" 
    
    if not os.path.exists(input_folder):
        print(f" Folder '{input_folder}' not found. Please create it and add PDFs.")
    else:
        # Get a list of every PDF inside the folder
        pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
        
        if not pdf_files:
            print(f"No PDFs found in '{input_folder}'. Drop some PDFs in there first!")
        else:
            print(f"Found {len(pdf_files)} PDFs. Starting batch decomposition...\n")
            
            # Loop through every single PDF and process it
            for pdf_file in pdf_files:
                full_path = os.path.join(input_folder, pdf_file)
                decompose_pdf(full_path, dpi=300)
                
            print("\n All PDFs have been successfully decomposed into standardized doc_XXX folders!")