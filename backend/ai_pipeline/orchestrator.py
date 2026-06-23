import re

def route_question(question_text: str) -> str:
    """
    Acts as the Orchestrator.
    Analyzes the question text and returns the optimal LLM model hosted on Groq.
    - 'llama-3.3-70b-versatile': for mathematical/analytical problems (high reasoning)
    - 'mixtral-8x7b-32768': for theoretical/essay questions (creative mixture of experts)
    """
    # Keywords that strongly indicate an analytical/mathematical problem
    analytical_keywords = [
        "calculate", "derive", "compute", "solve", "determine", "find the value",
        "equation", "formula", "circuit", "diagram", "matrix", "integral", "derivative"
    ]
    
    # Mathematical symbols check
    if re.search(r'[\+\-\*\/\=\(\)\[\]\{\}\^\_\$]', question_text) or any(kw in question_text.lower() for kw in analytical_keywords):
        return "llama-3.3-70b-versatile"
    
    # Theoretical essay questions go to Mixtral
    return "mixtral-8x7b-32768"
