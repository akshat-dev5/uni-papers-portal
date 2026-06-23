import argparse
import json
import os
import subprocess
import tempfile
import urllib.request
from config import INPUT_DIR
from pdf_processor import pdf_to_images
from llm_client import get_llm_client, extract_text_from_image
from extractor import structure_output, combine_pages
from student_agent import generate_answers_for_paper

def generate_markdown(final_output, output_md_path):
    md_content = f"# Extracted Question Paper and Solutions\n\n"
    md_content += f"**Source:** {final_output.get('source_file', 'URL')}\n"
    md_content += f"**Total Pages:** {final_output.get('total_pages', 0)}\n"
    md_content += f"**Overall Confidence:** {final_output.get('overall_confidence', 0)}%\n\n"
    
    for page in final_output.get("pages", []):
        md_content += f"## Page {page.get('page_number', '1')}\n\n"
        md_content += page.get("extracted_content", "") + "\n\n"
        
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown file saved to: {output_md_path}")

def process_pdf_url(pdf_url, solution_id, temp_dir):
    print(f"Downloading PDF from: {pdf_url}")
    
    output_dir = os.path.join(temp_dir, "generated-solutions")
    os.makedirs(output_dir, exist_ok=True)
    
    # Download the PDF
    pdf_path = os.path.join(temp_dir, f"{solution_id}.pdf")
    try:
        urllib.request.urlretrieve(pdf_url, pdf_path)
    except Exception as e:
        print(f"ERROR: Failed to download PDF: {e}")
        return
        
    print("Converting PDF to images...")
    images = pdf_to_images(pdf_path)
    print(f"Total pages: {len(images)}")
    
    client = get_llm_client()
    pages_output = []
    
    for i, image in enumerate(images):
        print(f"Extracting page {i+1}/{len(images)}...")
        raw_text = extract_text_from_image(image, client)
        images_dir = os.path.join(temp_dir, "images")
        page_data = structure_output(raw_text, f"{solution_id}.pdf", i+1, image, images_dir)
        pages_output.append(page_data)
    
    final_output = combine_pages(pages_output)
    
    # 3-Agent Pipeline starts here
    final_output = generate_answers_for_paper(final_output)
    
    temp_json_path = os.path.join(temp_dir, f"{solution_id}.json")
    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    temp_md_path = os.path.join(temp_dir, f"{solution_id}.md")
    generate_markdown(final_output, temp_md_path)
    
    output_docx_path = os.path.join(output_dir, f"{solution_id}.docx")
    print(f"Converting Markdown to Word via Pandoc...")
    try:
        subprocess.run(["pandoc", temp_md_path, "-o", output_docx_path, "--mathjax"], check=True)
        print(f"Word document saved to: {output_docx_path}")
    except FileNotFoundError:
        print("ERROR: Pandoc is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Pandoc conversion failed: {e}")
        
    print(f"Done processing: {solution_id}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Headless 3-Agent OCR Pipeline")
    parser.add_argument("--url", required=True, help="URL of the PDF to process")
    parser.add_argument("--id", required=True, help="Unique solution ID")
    parser.add_argument("--temp_dir", required=True, help="Directory to store intermediate and final files")
    
    args = parser.parse_args()
    
    process_pdf_url(args.url, args.id, args.temp_dir)