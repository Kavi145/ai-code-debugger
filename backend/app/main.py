from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

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

# Resolve paths for frontend static files based on container layout
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

@app.get("/")
def serve_frontend():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "AI Python Debugger Engine API is running."}

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
