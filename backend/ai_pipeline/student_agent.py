"""
answer_generator.py — Rewritten for reliability and quality.

Changes from original:
- Rate limit retry with exponential backoff
- Expanded question pattern detection (a–z, i–iv, numbered)
- Sub-questions no longer terminate parent question collection
- Scaled max_tokens per mark level
- Improved prompt: no rigid bullet count, no "Sketch required"
- Robust subject extraction with multiple regex patterns
- System message for persistent professor persona
- Higher temperature for better prose
- import re moved to top of file
"""

import re
import os
import time
from groq import Groq, RateLimitError


# ─── Regex Patterns ────────────────────────────────────────────────────────────

# Matches the start of any question line (ignoring sub-questions to allow parent grouping)
QUESTION_START = re.compile(
    r'^(\*\*\s*Q\d+[\.\)]'                     # **Q1. or **Q1)
    r'|\*\*\s*\d+[\.\)]'                        # **1. or **1)
    r'|\b\d+[\.\)]\s+[A-Z]'                    # 1. Define... 2) What is...
    r'|\bOR\b|\bor\b)'                          # OR alternative dividers
)

# Matches the start of a sub-question like (a), (b), (i), (ii)
SUBQUESTION_START = re.compile(
    r'^(\([a-zA-Z]\)'                            # (a) (b) ... (z)
    r'|\([ivxlcIVXLC]+\))'                       # (i) (ii) (iii) (iv)
)

# Marks extraction: last [number] in a question line is usually the mark
MARKS_REGEX = re.compile(r'\[(\d+)\]')

# Subject extraction patterns (tried in order)
SUBJECT_PATTERNS = [
    re.compile(r'\|\s*(?:Subject|Course Title|Paper|Course)\s*\|\s*([^|\n]+)\|', re.IGNORECASE),
    re.compile(r'Subject\s*[:\-]\s*(.+)', re.IGNORECASE),
    re.compile(r'Course\s*[:\-]\s*(.+)', re.IGNORECASE),
    re.compile(r'Paper\s*[:\-]\s*(.+)', re.IGNORECASE),
]


# ─── Client Manager ──────────────────────────────────────────────────────────────

from config import GROQ_ANSWER_API_KEYS

_current_key_idx = 0
_active_client = None

def get_active_client() -> Groq:
    global _active_client, _current_key_idx
    if not GROQ_ANSWER_API_KEYS:
        raise ValueError("No GROQ_ANSWER_API_KEYS found in .env")
    if _active_client is None:
        _active_client = Groq(api_key=GROQ_ANSWER_API_KEYS[_current_key_idx], max_retries=0)
    return _active_client

def rotate_key():
    global _current_key_idx, _active_client
    _current_key_idx = (_current_key_idx + 1) % len(GROQ_ANSWER_API_KEYS)
    _active_client = Groq(api_key=GROQ_ANSWER_API_KEYS[_current_key_idx], max_retries=0)
    print(f"  [Key Rotation] Switched to API Key {_current_key_idx + 1}")


# ─── Subject Extraction ────────────────────────────────────────────────────────

def extract_subject(extracted_data: dict) -> str:
    """
    Try multiple regex patterns across all pages to find the exam subject.
    Returns a clean subject string, or empty string if not found.
    """
    for page in extracted_data.get("pages", []):
        content = page.get("extracted_content", "")
        for pattern in SUBJECT_PATTERNS:
            match = pattern.search(content)
            if match:
                subject = match.group(1).strip()
                if 3 < len(subject) < 120:
                    return subject
    return ""


# ─── Prompt Builder ────────────────────────────────────────────────────────────

def build_answer_prompt(question_text: str, marks: int, subject: str, sub_part_text: str = None, feedback: str = None) -> str:
    """
    Builds a context-aware prompt scaled to the marks and subject.
    Avoids the rigid '2x marks bullet points' rule that produces poor answers.
    """
    subject_label = subject if subject else "Engineering"

    if marks <= 2:
        depth = "very concise — 2 to 3 key sentences covering the core definition or fact"
        word_guide = f"{marks * 30}–{marks * 50} words"
    elif marks <= 5:
        depth = "moderate — clear explanation with a relevant example or formula"
        word_guide = f"{marks * 50}–{marks * 80} words"
    elif marks <= 10:
        depth = "detailed — theory, derivation or algorithm steps, example, and brief applications"
        word_guide = f"{marks * 60}–{marks * 90} words"
    else:
        depth = "comprehensive — full theory, step-by-step derivation, worked example, diagram description, and applications"
        word_guide = f"{marks * 70}–{marks * 100} words"

    prompt = f"""You are solving the following university exam question worth {marks} marks.
Subject: {subject_label}

FULL EXAM QUESTION CONTEXT:
{question_text}
"""

    if sub_part_text:
        prompt += f"\nYOUR TASK: Answer ONLY this specific sub-part:\n{sub_part_text}\n"

    prompt += f"""
ANSWER REQUIREMENTS:
- Depth: {depth}
- Approximate length: {word_guide}
- Format: Choose whichever best fits this question:
    • Numbered steps for algorithms, procedures, or derivations
    • Bullet points for lists of properties, features, or advantages
    • Prose paragraphs for definitions, explanations, or comparisons
    • LaTeX for equations: inline as $...$ and block as $$...$$
- For diagram-based questions: DO NOT say "Sketch required".
  Instead: write a clear textual description of the diagram (components, 
  connections, labels, flow direction) and/or draw a simple ASCII diagram.
- Start your answer immediately — do NOT add "Sure!", "Here is the answer", or any other preamble.
- Do NOT repeat the question text.
- End with a one-line summary only if marks >= 7.
"""
    if feedback:
        prompt += f"""
[CRITICAL FEEDBACK FROM PROFESSOR ON PREVIOUS ATTEMPT]:
The professor rejected your last answer with the following feedback: "{feedback}"
You MUST thoroughly address this feedback in your new answer or you will fail the evaluation.
"""
    return prompt


# ─── Single Question Answer Generation ────────────────────────────────────────

def generate_answer_for_question(
    question_text: str,
    subject: str = "",
    marks: int = 5,
    sub_part_text: str = None,
    feedback: str = None,
    model: str = "llama-3.3-70b-versatile"
) -> str:
    """
    Generates an answer for a single question with exponential backoff retry.
    """
    if not question_text.strip():
        return ""

    subject_label = subject if subject else "Engineering"
    max_output_tokens = min(8192, max(512, marks * 350))

    system_message = (
        f"You are an experienced university professor and exam solution writer "
        f"specialising in {subject_label}. "
        f"You write precise, well-structured answers that an examiner would award full marks. "
        f"You never pad answers with filler text and you never leave any part of a question unanswered."
    )

    prompt = build_answer_prompt(question_text, marks, subject, sub_part_text, feedback)

    attempts_exhausted = 0
    max_key_rotations = len(GROQ_ANSWER_API_KEYS)

    while attempts_exhausted < max_key_rotations:
        client = get_active_client()
        for attempt in range(6):  # up to 6 attempts per key
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.65,
                    max_tokens=max_output_tokens,
                )
                
                content = response.choices[0].message.content.strip()
                if response.choices[0].finish_reason == "length":
                    content += "\n\n*(Note: Answer was truncated due to length limits)*"
                    
                return content

            except RateLimitError:
                if attempt == 5:
                    print("  [Rate Limit] Exhausted 6 retries for current key. Rotating...")
                    break  # Break out of the for loop to trigger rotation
                wait = (2 ** attempt) * 10  # 10, 20, 40, 80, 160 seconds
                print(f"  [Rate Limit] Waiting {wait}s (attempt {attempt + 1}/6)...")
                time.sleep(wait)

            except Exception as e:
                print(f"  [Error] on attempt {attempt + 1}: {e}")
                if attempt == 5:
                    return f"[Answer generation failed after 6 attempts: {e}]"
                time.sleep(5)
                
        # If we broke out of the inner loop due to persistent RateLimitError:
        rotate_key()
        attempts_exhausted += 1

    return "[Answer generation failed: all API keys exhausted their rate limits]"


# ─── Question Block Collector ──────────────────────────────────────────────────

def extract_marks_from_text(text: str) -> int:
    """
    Extract the marks value from a question string.
    Takes the LAST [number] match, which is usually the marks.
    Returns 5 as a safe default.
    """
    matches = MARKS_REGEX.findall(text)
    if matches:
        # Use the last match — in patterns like **Q3. [4]** the last is the marks
        return int(matches[-1])
    return 5


def collect_question_block(lines: list, start_index: int) -> tuple[list, int]:
    """
    Starting from start_index, collect all lines that belong to this question block.
    A block ends when:
      - A new MAIN question starts (**Q2., **Q3., etc.)
      - A section header starts (## )
      - A DIAGRAM placeholder appears
      - End of lines

    Sub-question labels (a), (b), (c), (d), (e) are treated as CONTINUATIONS,
    not terminators. They are part of the same question block.

    Returns: (list of lines in block, index of first line NOT in block)
    """
    block = [lines[start_index]]
    j = start_index + 1

    while j < len(lines):
        line = lines[j]
        stripped = line.strip()

        # Terminate on a new main question, section header, or diagram placeholder
        if (QUESTION_START.match(stripped)
                or stripped.startswith("## ")
                or stripped.startswith("[DIAGRAM:")):
            break

        block.append(line)
        j += 1

    return block, j


def split_into_subparts(block_lines: list) -> tuple[str, list]:
    """
    Splits a full question block into the parent context and a list of sub-questions.
    Returns: (parent_context_string, list_of_sub_question_strings)
    """
    parent_lines = []
    sub_questions = []
    current_sub = []
    in_subquestions = False
    
    for line in block_lines:
        stripped = line.strip()
        if SUBQUESTION_START.match(stripped):
            in_subquestions = True
            if current_sub:
                sub_questions.append("\n".join(current_sub).strip())
            current_sub = [line]
        elif in_subquestions:
            current_sub.append(line)
        else:
            parent_lines.append(line)
            
    if current_sub:
        sub_questions.append("\n".join(current_sub).strip())
        
    return "\n".join(parent_lines).strip(), sub_questions


# ─── Main Pipeline Function ────────────────────────────────────────────────────

def generate_answers_for_paper(extracted_data: dict) -> dict:
    """
    Takes the structured OCR data and injects answers for every detected question.
    Returns the same dict with answers inserted inline into extracted_content.
    """
    subject = extract_subject(extracted_data)

    if subject:
        print(f"[Subject detected]: {subject}")
    else:
        print("[Subject not detected] — using generic engineering context.")

    total_questions = 0
    answered_questions = 0

    print("Starting 3-Agent Answer Generation Pipeline...\n")
    from professor_agent import review_answer
    from orchestrator import route_question

    for page_idx, page in enumerate(extracted_data.get("pages", [])):
        content = page.get("extracted_content", "")
        if not content:
            continue

        lines = content.split("\n")
        new_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Check if this line starts a question or sub-question
            if QUESTION_START.match(stripped):
                total_questions += 1

                # Collect the full question block (including all sub-parts)
                block_lines, next_i = collect_question_block(lines, i)
                full_question_text = "\n".join(block_lines).strip()

                parent_context, sub_questions = split_into_subparts(block_lines)

                # Add the parent question lines to output
                new_lines.append(parent_context)

                if not sub_questions:
                    marks = extract_marks_from_text(full_question_text)
                    
                    # 1. ORCHESTRATOR PHASE
                    selected_model = route_question(full_question_text)
                    print(f"  [Page {page_idx+1}] Orchestrator selected model: {selected_model}")
                    
                    # Generate and insert answer for the single main question
                    print(f"  [Page {page_idx+1}] Answering ({marks}m): {full_question_text[:60].strip()}...")
                    
                    answer = ""
                    feedback = None
                    for attempt in range(3): # Max 3 attempts
                        # 2. STUDENT PHASE
                        answer = generate_answer_for_question(full_question_text, subject, marks, feedback=feedback, model=selected_model)
                        if answer.startswith("[Answer generation failed"):
                            break
                        
                        # 3. PROFESSOR PHASE
                        review = review_answer(full_question_text, answer, marks)
                        print(f"    -> [Professor Review] Score: {review['score']}/100. Approved: {review['approved']}")
                        if review['approved']:
                            break
                        
                        feedback = review['feedback']
                        print(f"    -> [Revision needed] Feedback: {feedback}")

                    if answer and not answer.startswith("[Answer generation failed"):
                        answered_questions += 1
                        new_lines.extend(["", "***", "**Answer:**", "", answer, "", "***", ""])
                    else:
                        new_lines.extend(["", f"> [Warning] {answer}", ""])
                else:
                    # Process each sub-question individually
                    answered_questions += 1  # Count the whole parent as 1 answered question
                    for sub_q in sub_questions:
                        sub_marks = extract_marks_from_text(sub_q)
                        
                        # 1. ORCHESTRATOR PHASE
                        selected_model = route_question(sub_q)
                        print(f"  [Page {page_idx+1}] Orchestrator selected model: {selected_model}")
                        
                        print(f"  [Page {page_idx+1}] Answering Sub-part ({sub_marks}m): {sub_q[:60].strip()}...")
                        new_lines.extend(["", sub_q])
                        
                        answer = ""
                        feedback = None
                        for attempt in range(3):
                            # 2. STUDENT PHASE
                            answer = generate_answer_for_question(full_question_text, subject, sub_marks, sub_part_text=sub_q, feedback=feedback, model=selected_model)
                            if answer.startswith("[Answer generation failed"):
                                break
                            
                            # 3. PROFESSOR PHASE
                            review = review_answer(sub_q, answer, sub_marks)
                            print(f"    -> [Professor Review] Score: {review['score']}/100. Approved: {review['approved']}")
                            if review['approved']:
                                break
                            
                            feedback = review['feedback']
                            print(f"    -> [Revision needed] Feedback: {feedback}")

                        if answer and not answer.startswith("[Answer generation failed"):
                            new_lines.extend(["", "***", "**Answer:**", "", answer, "", "***", ""])
                        else:
                            new_lines.extend(["", f"> [Warning] {answer}", ""])

                i = next_i  # jump past the collected block

            else:
                new_lines.append(line)
                i += 1

        page["extracted_content"] = "\n".join(new_lines)

    print(f"\nAnswer generation complete: {answered_questions}/{total_questions} questions answered.")
    extracted_data["answer_coverage"] = {
        "total_questions": total_questions,
        "answered": answered_questions,
        "coverage_pct": round((answered_questions / total_questions * 100) if total_questions else 0, 1)
    }

    return extracted_data