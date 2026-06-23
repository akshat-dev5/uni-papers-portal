import os
from PIL import Image
from layout_detector import detect_figures

def detect_and_save_diagrams(image, pdf_filename, page_number, output_images_dir):
    os.makedirs(output_images_dir, exist_ok=True)
    
    figures = detect_figures(image)
    
    if not figures:
        return []
        
    # Sort figures top-to-bottom by y1 coordinate to guarantee logical sequential mapping
    figures.sort(key=lambda f: f["y1"])
    
    diagram_paths = []
    for i, fig in enumerate(figures):
        # Crop with small padding
        padding = 10
        x1 = max(0, fig["x1"] - padding)
        y1 = max(0, fig["y1"] - padding)
        x2 = min(image.width, fig["x2"] + padding)
        y2 = min(image.height, fig["y2"] + padding)
        
        cropped = image.crop((x1, y1, x2, y2))
        
        img_filename = f"{pdf_filename.replace('.pdf', '')}_page{page_number}_fig{i+1}.jpg"
        img_path = os.path.join(output_images_dir, img_filename)
        cropped.save(img_path)
        
        diagram_paths.append({
            "description": f"Figure detected on page {page_number}",
            "image_path": img_path,
            "confidence": fig["confidence"]
        })
    
    return diagram_paths