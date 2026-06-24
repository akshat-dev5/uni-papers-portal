import re

def route_question(question_text: str) -> str:
    """
    Acts as the Orchestrator.
    Analyzes the question text and returns the optimal LLM model hosted on Groq.
    - 'llama-3.3-70b-versatile': for mathematical/analytical problems (high reasoning)
    - 'gemma2-9b-it': for programming/coding and logic questions (Google's architecture)
    - 'mixtral-8x7b-32768': for theoretical/essay questions (creative mixture of experts)
    """
    # Keywords that strongly indicate an analytical/mathematical problem
    analytical_keywords = [
        "calculate", "derive", "compute", "solve", "determine", "find the value",
        "equation", "formula", "circuit", "diagram", "matrix", "integral", "derivative"
    ]
    
    # Keywords that strongly indicate a programming/coding problem
    coding_keywords = [
        "write a program", "code", "function", "algorithm", "syntax", "array", 
        "pointer", "loop", "compile", "debug", "pseudo-code"
    ]
    
    question_lower = question_text.lower()
    
    # Mathematical symbols check
    if re.search(r'[\+\-\*\/\=\(\)\[\]\{\}\^\_\$]', question_text) or any(kw in question_lower for kw in analytical_keywords):
        return "llama-3.3-70b-versatile"
        
    # Coding/Programming check
    if any(kw in question_lower for kw in coding_keywords):
        return "gemma2-9b-it"
    
    # Theoretical essay questions go to Mixtral
    return "mixtral-8x7b-32768"
