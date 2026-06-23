import base64
import io
from config import GROQ_API_KEY, LLM_PROVIDER
from groq import Groq
from PIL import Image

def get_llm_client():
    if LLM_PROVIDER == "groq":
        return Groq(api_key=GROQ_API_KEY)
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def image_to_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def extract_text_from_image(image, client):
    prompt = """You are an expert at extracting text from scanned engineering question papers.

STRICT RULES:
- Extract ONLY what is visible in the image. No explanations, no commentary, no conversational text.
- Do NOT include phrases like "Please let me know", "The confidence score is based on", or any meta-commentary.
- Do NOT wrap output in markdown code blocks.
- Preserve all mathematical equations, symbols, subscripts and superscripts EXACTLY.
- Format all math strictly as LaTeX (e.g. inline as $...$ and block as $$...$$).

Structure the output EXACTLY as follows:

## Exam Details
| Field | Value |
|-------|-------|
| Subject | ... |
| Degree | ... |
| Semester | ... |

## Questions
For each question:
**Q[number]. [marks]**
(a) [sub-question text] [[marks]]
(b) [sub-question text] [[marks]]

IMPORTANT: If marks are defined globally at the top of a section (e.g., "PART - B [5x4=20]" where 5 is the number of questions and 4 is the marks per question), you MUST infer the marks per question (4 in this case) and explicitly append it to every question in that section (e.g., **Q1. [4]**, **Q2. [4]**).

If a diagram exists at this position write exactly:
[DIAGRAM: x1, y1, x2, y2, Figure description]

## Confidence Score
[number]%"""

    image_data = image_to_base64(image)
    
    import time
    from groq import RateLimitError
    
    for attempt in range(6):
        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=8192
            )
            
            content = response.choices[0].message.content
            if response.choices[0].finish_reason == "length":
                content += "\n\n[WARNING: OCR text truncated due to length limits]"
                
            return content
        except RateLimitError:
            wait = (2 ** attempt) * 10
            print(f"  [Rate limit] Waiting {wait}s before retry {attempt+1}/6...")
            time.sleep(wait)
        except Exception as e:
            print(f"  [Error] {e}")
            if attempt == 5:
                return f"[OCR Failed: {e}]"
            time.sleep(5)
            
    return "[OCR Failed: Retries exhausted]"