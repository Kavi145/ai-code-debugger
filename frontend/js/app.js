// Build out the interactive CodeMirror context environment mapping
const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    indentUnit: 4,
    matchBrackets: true
});

// Update this link with your live public Render/Railway URL once deployed
const BACKEND_API_ENDPOINT = "http://localhost:8000/execute";

document.getElementById("run-btn").addEventListener("click", async () => {
    const userCode = editor.getValue();
    const consoleOutput = document.getElementById("console-output");
    const aiCard = document.getElementById("ai-card");
    
    // Set UI to loading state
    consoleOutput.className = "console-box system-idle";
    consoleOutput.innerText = "Processing script safely inside sandboxed environment...";
    aiCard.classList.add("hidden");

    try {
        const response = await fetch(BACKEND_API_ENDPOINT, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: userCode })
        });

        if (!response.ok) {
            throw new Error("Target computing node responded with invalid error code statuses.");
        }

        const data = await response.json();

        if (data.success) {
            consoleOutput.className = "console-box success";
            consoleOutput.innerText = data.output || "Code executed successfully with no returned stdout outputs.";
        } else {
            consoleOutput.className = "console-box error";
            consoleOutput.innerText = data.raw_error;

            // Map and expose the dynamic AI diagnostic insights
            document.getElementById("ai-explanation").innerText = data.ai_explanation;
            document.getElementById("ai-suggestion").innerText = data.ai_suggestion;
            aiCard.classList.remove("hidden");
        }

    } catch (error) {
        consoleOutput.className = "console-box error";
        consoleOutput.innerText = `Network Connection Failure:\nUnable to establish communication loops with the API Engine. Details: ${error.message}`;
    }
});