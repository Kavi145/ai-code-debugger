from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.code import CodeExecutionRequest, CodeExecutionResponse
from app.services.executor import execute_python_code
from app.services.ai_analyzer import analyze_error_with_ai

app = FastAPI(title="AI Python Debugger Engine API")

# Essential Middleware allowing browser clients to query public API routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/execute", response_model=CodeExecutionResponse)
def run_and_debug_code(request: CodeExecutionRequest):
    # Step 1: Process the script inside the sandbox environment
    result = execute_python_code(request.code)
    
    # Step 2: Immediate return mapping for successful executions
    if result["success"]:
        return CodeExecutionResponse(
            success=True,
            output=result["output"]
        )
        
    # Step 3: Call the AI Engine if an error is caught
    ai_insights = analyze_error_with_ai(
        code=request.code, 
        error_msg=result["raw_error"], 
        error_type=result["error_type"]
    )
    
    return CodeExecutionResponse(
        success=False,
        output=result["output"],
        error_type=result["error_type"],
        raw_error=result["raw_error"],
        ai_explanation=ai_insights.get("explanation"),
        ai_suggestion=ai_insights.get("suggestion")
    )