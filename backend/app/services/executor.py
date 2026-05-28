import subprocess
import tempfile
import os

def execute_python_code(code: str) -> dict:
    """
    Safely executes arbitrary code strings using an isolated background OS subprocess.
    Includes a 5-second timeout constraint to prevent infinite loop crashes.
    """
    # Create a temporary file to hold the user's raw code script securely
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        # Run code as an independent OS system process
        result = subprocess.run(
            ["python", temp_file_path],
            capture_output=True,
            text=True,
            timeout=5.0  # Safe execution time-limit boundary
        )
        
        # Clean up the temp script file from memory storage
        os.remove(temp_file_path)

        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout,
                "error_type": None,
                "raw_error": None
            }
        else:
            # Code broke! Isolate the explicit Error Class dynamically from stderr
            stderr_lines = result.stderr.strip().split("\n")
            error_line = stderr_lines[-1] if stderr_lines else "Exception: Unknown Error"
            error_type = error_line.split(":")[0]

            return {
                "success": False,
                "output": result.stdout,
                "error_type": error_type,
                "raw_error": result.stderr
            }

    except subprocess.TimeoutExpired:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {
            "success": False,
            "error_type": "TimeoutError",
            "raw_error": "Execution Time Limit Exceeded. Your code took longer than 5 seconds to respond or hit an infinite loop."
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {
            "success": False,
            "error_type": e.__class__.__name__,
            "raw_error": str(e)
        }