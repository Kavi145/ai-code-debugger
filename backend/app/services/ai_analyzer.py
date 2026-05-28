from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Groq client securely
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def analyze_error_with_ai(code: str, error_msg: str, error_type: str) -> dict:
    """
    Leverages Groq's high-speed Llama-3.1 model to analyze and fix sandboxed execution errors.
    """
    if not GROQ_API_KEY or not client:
        return {
            "explanation": "AI Debugging helper is offline because the GROQ_API_KEY is unconfigured.",
            "suggestion": "Review your code syntax structural loops locally."
        }

    try:
        # Utilizing llama-3.1-8b-instant (Optimized for lightning-fast structural text responses)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an advanced software engineer and computer science tutor. Your task is to diagnose code execution errors and return response packages strictly in structured JSON format."
                },
                {
                    "role": "user",
                    "content": f"""
The student's code failed with an explicit error type of: {error_type}.

--- RAW CODE WORKSPACE ---
{code}

--- TERMINAL STACK TRACE ---
{error_msg}

Provide your analysis response in exactly this strict JSON format structure:
{{
    "explanation": "A clear, concise 2-3 sentence breakdown explaining WHY this error happened inside their specific code framework logic.",
    "suggestion": "Show the corrected line or block of code with an explanation of what was changed."
}}
"""
                }
            ],
            response_format={"type": "json_object"} # Forces Groq to output clean, parseable JSON
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        return {
            "explanation": f"Your code encountered a runtime {error_type} execution barrier.",
            "suggestion": "Trace your assignments, loop bounds, or variable data types to solve the issue."
        }