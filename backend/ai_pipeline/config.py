import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

LLM_PROVIDER = "groq"
GROQ_API_KEY = os.getenv("ocr_api_key") or os.getenv("GROQ_API_KEY")

GROQ_ANSWER_API_KEYS = []
for i in range(1, 10):
    key = os.getenv(f"answer_gen_key{i}")
    if key:
        GROQ_ANSWER_API_KEYS.append(key)

if not GROQ_ANSWER_API_KEYS and os.getenv("GROQ_ANSWER_API_KEY"):
    GROQ_ANSWER_API_KEYS.append(os.getenv("GROQ_ANSWER_API_KEY"))

DPI = 300
OUTPUT_FORMAT = "json"
WORD_OUTPUT_DIR = "output/word_files/"
JSON_OUTPUT_DIR = "output/json_files/"
INPUT_DIR = "input/"
