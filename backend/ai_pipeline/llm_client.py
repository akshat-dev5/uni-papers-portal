import base64
import io
from config import GROQ_API_KEY, VISION_PROVIDER, GEMINI_API_KEY
from groq import Groq
from PIL import Image

def get_llm_client():
    if VISION_PROVIDER == "gemini":
        import google.generativeai as genai
        if not GEMINI_API_KEY:
            raise ValueError("No GEMINI_API_KEY found in config or .env")
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel("gemini-flash-lite-latest")
    elif VISION_PROVIDER == "groq":
        return Groq(api_key=GROQ_API_KEY)
    else:
        raise ValueError(f"Unsupported VISION_PROVIDER: {VISION_PROVIDER}")

def image_to_base64(image):
    max_dimension = 1024
    if max(image.size) > max_dimension:
        ratio = max_dimension / max(image.size)
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
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

    import time
    
    if VISION_PROVIDER == "gemini":
        from google.api_core.exceptions import InvalidArgument, PermissionDenied, NotFound
        for attempt in range(6):
            try:
                response = client.generate_content([prompt, image])
                return response.text
            except (InvalidArgument, PermissionDenied, NotFound) as e:
                return f"[OCR Failed: API Key Invalid, Permission Denied, or Model Not Found. {e}]"
            except Exception as e:
                wait = (2 ** attempt) * 10
                print(f"  [Gemini API Error] Waiting {wait}s before retry {attempt+1}/6... {e}")
                time.sleep(wait)
        return "[OCR Failed: Retries exhausted on Gemini]"

    # Groq Fallback
    image_data = image_to_base64(image)
    from groq import RateLimitError
    model_name = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    for attempt in range(6):
        try:
            response = client.chat.completions.create(
                model=model_name,
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
                max_tokens=2048
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