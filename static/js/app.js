/**
 * Java 21 Syntax Checker — Interactive Web Frontend
 * Powered by GNU Flex Lexer & GNU Bison LALR(1) Parser
 */

document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------------------------------------------------
    // 1. Initialize CodeMirror 5 with Java Mode
    // -------------------------------------------------------------------------
    const textarea = document.getElementById("codeEditor");
    const editor = CodeMirror.fromTextArea(textarea, {
        mode: "text/x-java",
        theme: "dracula",
        lineNumbers: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        tabSize: 4,
        indentUnit: 4,
        indentWithTabs: false,
        lineWrapping: true,
        extraKeys: {
            "Ctrl-Enter": () => triggerCheckSyntax(),
            "F5": () => triggerCheckSyntax(),
            "Tab": (cm) => cm.replaceSelection("    ", "end")
        }
    });

    let currentErrorLineHandle = null;
    let sampleDataCache = {};

    // -------------------------------------------------------------------------
    // 2. DOM Elements
    // -------------------------------------------------------------------------
    const checkBtn = document.getElementById("checkBtn");
    const clearBtn = document.getElementById("clearBtn");
    const fileInput = document.getElementById("fileInput");
    const sampleSelect = document.getElementById("sampleSelect");
    const dropZone = document.getElementById("dropZone");
    const dropOverlay = document.getElementById("dropOverlay");

    const lineColCounter = document.getElementById("lineColCounter");
    const charCounter = document.getElementById("charCounter");

    const statusBadge = document.getElementById("statusBadge");
    const loadingIndicator = document.getElementById("loadingIndicator");
    const resultBanner = document.getElementById("resultBanner");
    const bannerIcon = document.getElementById("bannerIcon");
    const resultTitle = document.getElementById("resultTitle");
    const resultMessage = document.getElementById("resultMessage");

    const errorDetailsCard = document.getElementById("errorDetailsCard");
    const errorLineNum = document.getElementById("errorLineNum");
    const errorTokenVal = document.getElementById("errorTokenVal");
    const errorLatency = document.getElementById("errorLatency");
    const jumpToLineBtn = document.getElementById("jumpToLineBtn");
    const jumpLineText = document.getElementById("jumpLineText");

    const rawConsoleOutput = document.getElementById("rawConsoleOutput");
    const copyConsoleBtn = document.getElementById("copyConsoleBtn");

    // -------------------------------------------------------------------------
    // 3. Editor Event Listeners (Line/Col & Char Count)
    // -------------------------------------------------------------------------
    function updateCounters() {
        const doc = editor.getDoc();
        const cursor = doc.getCursor();
        const text = editor.getValue();
        const lines = doc.lineCount();
        const chars = text.length;

        lineColCounter.textContent = `Line ${cursor.line + 1}, Col ${cursor.ch + 1}`;
        charCounter.textContent = `${chars.toLocaleString()} chars · ${lines.toLocaleString()} lines`;
    }

    editor.on("cursorActivity", updateCounters);
    editor.on("change", () => {
        updateCounters();
        clearErrorLineHighlight();
    });

    // -------------------------------------------------------------------------
    // 4. Fetch Sample Programs from Backend
    // -------------------------------------------------------------------------
    async function loadSamples() {
        try {
            const resp = await fetch("/api/samples");
            if (resp.ok) {
                const data = await resp.json();
                if (data.samples) {
                    sampleDataCache = data.samples;
                }
            }
        } catch (err) {
            console.warn("Could not load remote samples, using fallback.", err);
        }
    }
    loadSamples();

    sampleSelect.addEventListener("change", (e) => {
        const key = e.target.value;
        if (sampleDataCache[key]) {
            editor.setValue(sampleDataCache[key].code);
            editor.clearHistory();
            resetDiagnosticsView();
            setStatus("ready", "Ready");
            logToConsole(`Loaded sample: ${sampleDataCache[key].title}`);
        }
    });

    // -------------------------------------------------------------------------
    // 5. File Upload & Drag-and-Drop
    // -------------------------------------------------------------------------
    fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            loadFileIntoEditor(file);
        }
    });

    function loadFileIntoEditor(file) {
        if (!file.name.toLowerCase().endsWith(".java") && !file.name.toLowerCase().endsWith(".txt")) {
            alert("Please select a .java or .txt file.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (event) => {
            editor.setValue(event.target.result);
            editor.clearHistory();
            resetDiagnosticsView();
            setStatus("ready", "Ready");
            logToConsole(`Loaded file: ${file.name} (${file.size} bytes)`);
        };
        reader.onerror = () => {
            alert("Error reading file.");
        };
        reader.readAsText(file);
    }

    // Drag-and-drop on CodeMirror
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropOverlay.classList.add("active");
    });

    dropZone.addEventListener("dragleave", (e) => {
        e.preventDefault();
        dropOverlay.classList.remove("active");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropOverlay.classList.remove("active");
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            loadFileIntoEditor(e.dataTransfer.files[0]);
        }
    });

    // -------------------------------------------------------------------------
    // 6. Clear Button
    // -------------------------------------------------------------------------
    clearBtn.addEventListener("click", () => {
        editor.setValue("");
        editor.clearHistory();
        resetDiagnosticsView();
        setStatus("ready", "Ready");
        logToConsole("Editor cleared.");
    });

    // -------------------------------------------------------------------------
    // 7. Check Syntax Workflow
    // -------------------------------------------------------------------------
    checkBtn.addEventListener("click", triggerCheckSyntax);

    // Global Key Listener for F5 and Ctrl+Enter
    window.addEventListener("keydown", (e) => {
        if (e.key === "F5" || (e.ctrlKey && e.key === "Enter")) {
            e.preventDefault();
            triggerCheckSyntax();
        }
    });

    async function triggerCheckSyntax() {
        const code = editor.getValue();
        if (!code || !code.trim()) {
            displayEmptySourceWarning();
            return;
        }

        clearErrorLineHighlight();
        setStatus("checking", "Checking...");
        loadingIndicator.classList.remove("hidden");
        checkBtn.disabled = true;

        const startTime = performance.now();

        try {
            const response = await fetch("/api/check", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ code: code })
            });

            const data = await response.json();
            const clientLatency = (performance.now() - startTime).toFixed(1);

            loadingIndicator.classList.add("hidden");
            checkBtn.disabled = false;

            if (response.ok) {
                if (data.valid) {
                    renderSuccessResult(data, clientLatency);
                } else {
                    renderErrorResult(data, clientLatency);
                }
            } else {
                renderServerError(data);
            }
        } catch (err) {
            loadingIndicator.classList.add("hidden");
            checkBtn.disabled = false;
            renderNetworkError(err);
        }
    }

    // -------------------------------------------------------------------------
    // 8. Result Renderers
    // -------------------------------------------------------------------------
    function renderSuccessResult(data, clientLatency) {
        setStatus("valid", "Valid Java");

        resultBanner.className = "result-banner banner-success";
        bannerIcon.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M20 6L9 17l-5-5" />
            </svg>`;
        resultTitle.textContent = "SUCCESS: Valid Java Syntax";
        resultMessage.textContent = `Analyzed in ${data.elapsed_ms || clientLatency} ms. All language tokens and grammar constructs conform to Java 21 syntax specifications.`;

        errorDetailsCard.classList.add("hidden");

        logToConsole(`[SUCCESS] Valid Java Syntax\nEngine: Flex Lexer + Bison LALR(1)\nParser Elapsed: ${data.elapsed_ms}ms (Roundtrip: ${clientLatency}ms)`);
    }

    function renderErrorResult(data, clientLatency) {
        setStatus("error", "Syntax Error");

        resultBanner.className = "result-banner banner-error";
        bannerIcon.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>`;

        resultTitle.textContent = `Syntax Error Detected`;
        resultMessage.textContent = data.message || "Invalid Java syntax encountered.";

        // Populate error details
        if (data.line) {
            errorLineNum.textContent = `Line ${data.line}`;
            jumpLineText.textContent = `${data.line}`;
            jumpToLineBtn.onclick = () => jumpToLine(data.line);
        } else {
            errorLineNum.textContent = "N/A";
            jumpLineText.textContent = "";
        }

        errorTokenVal.textContent = data.token ? `'${data.token}'` : "(EOF/Unknown)";
        errorLatency.textContent = `${data.elapsed_ms || clientLatency} ms`;

        errorDetailsCard.classList.remove("hidden");

        // Highlight line in CodeMirror
        if (data.line) {
            highlightErrorLine(data.line);
        }

        logToConsole(`[ERROR] ${data.message}\nExit Code: ${data.exit_code}\nParser Elapsed: ${data.elapsed_ms}ms`);
    }

    function displayEmptySourceWarning() {
        setStatus("error", "Empty Input");
        resultBanner.className = "result-banner banner-error";
        bannerIcon.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>`;
        resultTitle.textContent = "Source Code Empty";
        resultMessage.textContent = "Please enter Java source code or load a sample program before running syntax check.";
        errorDetailsCard.classList.add("hidden");
        editor.focus();
    }

    function renderServerError(data) {
        setStatus("error", "Server Error");
        resultBanner.className = "result-banner banner-error";
        resultTitle.textContent = data.error || "Server Error";
        resultMessage.textContent = data.message || "The syntax checking server returned an error.";
        errorDetailsCard.classList.add("hidden");
        logToConsole(`[SERVER ERROR] ${data.message || JSON.stringify(data)}`);
    }

    function renderNetworkError(err) {
        setStatus("error", "Network Error");
        resultBanner.className = "result-banner banner-error";
        resultTitle.textContent = "Connection Failure";
        resultMessage.textContent = "Could not reach the syntax checking backend service. Check network or server status.";
        errorDetailsCard.classList.add("hidden");
        logToConsole(`[NETWORK ERROR] ${err.message}`);
    }

    // -------------------------------------------------------------------------
    // 9. CodeMirror Error Line Helpers
    // -------------------------------------------------------------------------
    function highlightErrorLine(lineNum) {
        clearErrorLineHighlight();
        const zeroIndex = lineNum - 1;
        if (zeroIndex >= 0 && zeroIndex < editor.lineCount()) {
            currentErrorLineHandle = editor.addLineClass(zeroIndex, "background", "cm-error-line");
            editor.setGutterMarker(zeroIndex, "CodeMirror-linenumbers", makeGutterMarker());
        }
    }

    function clearErrorLineHighlight() {
        if (currentErrorLineHandle) {
            editor.removeLineClass(currentErrorLineHandle, "background", "cm-error-line");
            currentErrorLineHandle = null;
        }
        editor.clearGutter("CodeMirror-linenumbers");
    }

    function makeGutterMarker() {
        const marker = document.createElement("div");
        marker.style.color = "#f85149";
        marker.style.fontWeight = "bold";
        marker.style.paddingLeft = "2px";
        marker.innerHTML = "●";
        return marker;
    }

    function jumpToLine(lineNum) {
        const zeroIndex = lineNum - 1;
        editor.focus();
        editor.setCursor({ line: zeroIndex, ch: 0 });
        const coords = editor.charCoords({ line: zeroIndex, ch: 0 }, "local");
        editor.scrollTo(null, coords.top - 80);
    }

    // -------------------------------------------------------------------------
    // 10. Diagnostics Helpers
    // -------------------------------------------------------------------------
    function setStatus(type, label) {
        statusBadge.className = `status-pill status-${type}`;
        statusBadge.textContent = label;
    }

    function resetDiagnosticsView() {
        resultBanner.className = "result-banner banner-neutral";
        bannerIcon.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>`;
        resultTitle.textContent = "Awaiting Input";
        resultMessage.textContent = "Type Java code or select a sample, then click 'Check Syntax'.";
        errorDetailsCard.classList.add("hidden");
    }

    function logToConsole(msg) {
        const timestamp = new Date().toLocaleTimeString();
        rawConsoleOutput.textContent = `[${timestamp}] ${msg}`;
    }

    copyConsoleBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(rawConsoleOutput.textContent).then(() => {
            copyConsoleBtn.textContent = "Copied!";
            setTimeout(() => copyConsoleBtn.textContent = "Copy", 1500);
        });
    });

    // -------------------------------------------------------------------------
    // 11. Initial State: Load First Sample (Record Patterns)
    // -------------------------------------------------------------------------
    setTimeout(() => {
        if (sampleDataCache["records_patterns"]) {
            editor.setValue(sampleDataCache["records_patterns"].code);
            sampleSelect.value = "records_patterns";
            updateCounters();
        }
    }, 300);
});
