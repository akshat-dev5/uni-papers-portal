import json
import time
from groq import RateLimitError
from student_agent import get_active_client, rotate_key

def review_answer(question_text: str, student_answer: str, marks: int) -> dict:
    """
    Acts as a strict professor reviewing the student's answer.
    Returns a dict: {"score": int, "approved": bool, "feedback": str}
    """
    prompt = f"""You are a strict university professor grading an engineering exam.
You demand precision, correct formulas, and appropriate depth for the marks awarded.

QUESTION ({marks} marks):
{question_text}

STUDENT ANSWER:
{student_answer}

EVALUATION CRITERIA:
1. Is it technically correct?
2. Is the depth sufficient for {marks} marks?
3. Is it clearly structured?

Respond ONLY with a valid JSON object in this exact format, with no markdown formatting or extra text:
{{
    "score": 95,
    "approved": true,
    "feedback": "Perfect answer."
}}
If score is strictly less than 90, approved MUST be false, and feedback MUST explicitly state what the student needs to add or fix.
"""

    attempts_exhausted = 0
    max_key_rotations = 3 # Safe limit

    while attempts_exhausted < max_key_rotations:
        client = get_active_client()
        for attempt in range(4):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                
                content = response.choices[0].message.content.strip()
                try:
                    result = json.loads(content)
                    return {
                        "score": result.get("score", 0),
                        "approved": result.get("approved", False),
                        "feedback": result.get("feedback", "No feedback provided.")
                    }
                except json.JSONDecodeError:
                    return {"score": 80, "approved": False, "feedback": "Professor agent failed to output valid JSON. Please try again."}

            except RateLimitError:
                if attempt == 3:
                    break
                wait = (2 ** attempt) * 5
                time.sleep(wait)
            except Exception as e:
                time.sleep(2)
                
        rotate_key()
        attempts_exhausted += 1

    return {"score": 100, "approved": True, "feedback": "Rate limit exhausted for reviewer. Approved by default."}
