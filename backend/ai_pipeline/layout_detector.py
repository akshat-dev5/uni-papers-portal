from doclayout_yolo import YOLOv10
from huggingface_hub import hf_hub_download
import numpy as np

_model = None

def get_layout_model():
    global _model
    if _model is None:
        model_path = hf_hub_download(
            repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
            filename="doclayout_yolo_docstructbench_imgsz1024.pt"
        )
        _model = YOLOv10(model_path)
    return _model

def detect_figures(image):
    model = get_layout_model()
    image_np = np.array(image)
    results = model(image_np, imgsz=1024)
    
    figures = []
    for box in results[0].boxes:
        cls_name = results[0].names[int(box.cls)]
        if cls_name == "figure":
            coords = box.xyxy.tolist()[0]
            figures.append({
                "x1": int(coords[0]),
                "y1": int(coords[1]),
                "x2": int(coords[2]),
                "y2": int(coords[3]),
                "confidence": float(box.conf)
            })
    return figures