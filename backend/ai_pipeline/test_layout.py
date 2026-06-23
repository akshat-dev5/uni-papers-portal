from doclayout_yolo import YOLOv10
from huggingface_hub import hf_hub_download
import numpy as np
from pdf_processor import pdf_to_images

images = pdf_to_images("be_first-year-engineering_semester-2_2025_may_engineering-graphics-rev-2019c-scheme.pdf")
image = images[0]
image_np = np.array(image)

model_path = hf_hub_download(
    repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
    filename="doclayout_yolo_docstructbench_imgsz1024.pt"
)

model = YOLOv10(model_path)
results = model(image_np, imgsz=1024)

print("Detected regions:")
for box in results[0].boxes:
    cls_name = results[0].names[int(box.cls)]
    conf = float(box.conf)
    coords = box.xyxy.tolist()[0]
    print(f"Class: {cls_name}, Confidence: {conf:.2f}, Coordinates: {coords}")