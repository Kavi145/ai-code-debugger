# ai-code-debugger
A full-stack AI-driven debugging workspace that executes Python code in a secure backend sandbox and uses high-speed AI to instantly diagnose errors. If a script fails, the platform catches the runtime crash and displays a crystal-clear root-cause analysis alongside the exact code fix in a modern, scrollable split-pane terminal dashboard.

Overview

This application is a full stack debugging workspace that executes Python code in a safe sandbox environment and utilizes high speed AI to diagnose runtime crashes instantly.
You can access the live interactive application here: https://ai-code-debugger-1-dnqb.onrender.com/
How The Frontend Works

• You write or paste your Python code directly into a modern code editor panel built with CodeMirror.

• Clicking the action button packages your workspace script text into a clean network payload.

• The user interface splits into a dual pane view that lets you scroll through solutions while your code remains fixed on screen.

How The Backend Works

• The backend uses FastAPI to process incoming code strings safely and efficiently.

• The engine spins up a completely isolated background subprocess to run the Python script.

• A strict 5 second timeout limit actively monitors execution to kill infinite loops or frozen scripts instantly.

• Successful code runs return standard terminal output directly to a green console window.

• Crashed scripts trigger the system to intercept the exact error logs and route them to the Groq LPU engine.

• The system matches raw stack traces against AI models to return a precise logical explanation and code fix.

How To Setup And Use It

• Open your terminal and navigate inside the backend project folder.

• Install the necessary packages from your requirements file using pip install.

• Create a hidden environment file named dot env and add your private Groq API key inside it.

• Launch the backend server by running the uvicorn command in your terminal.

• Open the index html file in your web browser to load the dashboard workspace interface.

• Type any broken or operational Python script directly into the text editor box.

• Click the green button to execute your code and view standard console returns or complete AI diagnostics.
