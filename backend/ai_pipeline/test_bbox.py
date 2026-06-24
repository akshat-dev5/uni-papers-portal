from llm_client import get_llm_client, image_to_base64
from pdf_processor import pdf_to_images

client = get_llm_client()
images = pdf_to_images("be_first-year-engineering_semester-2_2025_may_engineering-graphics-rev-2019c-scheme.pdf")

# Test on page 1 only
image = images[0]

prompt = """Look at this engineering question paper image carefully.
Identify all diagrams, figures or technical drawings present.
For each diagram found, return its bounding box coordinates in this exact format:
[DIAGRAM: x1, y1, x2, y2, description]

Where x1,y1 is top-left corner and x2,y2 is bottom-right corner as pixel coordinates.
If no diagram exists on this page, say NONE."""

from groq import Groq

response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_to_base64(image)}"}}
        ]
    }],
    max_tokens=1024
)

print(response.choices[0].message.content)