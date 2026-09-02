from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini client securely
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def analyze_error_with_ai(code: str, error_msg: str, error_type: str) -> dict:
    """
    Leverages Gemini's high-speed model to analyze and fix sandboxed execution errors.
    """
    if not GEMINI_API_KEY or not client:
        return {
            "explanation": "AI Debugging helper is offline because the GEMINI_API_KEY is unconfigured.",
            "suggestion": "Review your code syntax structural loops locally."
        }

    try:
        prompt = f"""
You are an advanced software engineer and computer science tutor. Your task is to diagnose code execution errors and return response packages strictly in structured JSON format.

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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        return {
            "explanation": f"Your code encountered a runtime {error_type} execution barrier.",
            "suggestion": "Trace your assignments, loop bounds, or variable data types to solve the issue."
        }
