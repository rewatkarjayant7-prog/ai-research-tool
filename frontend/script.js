document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-input");
    const fileDropArea = document.getElementById("file-drop-area");
    const fileMsg = document.getElementById("file-msg");
    const runBtn = document.getElementById("run-btn");
    const statusMsg = document.getElementById("status-msg");
    const uploadSection = document.getElementById("upload-section");
    const resultsSection = document.getElementById("results-section");
    const resetBtn = document.getElementById("reset-btn");

    let selectedFile = null;

    // Handle drag events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileDropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileDropArea.addEventListener(eventName, () => fileDropArea.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileDropArea.addEventListener(eventName, () => fileDropArea.classList.remove('dragover'), false);
    });

    // Handle drop
    fileDropArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        handleFiles(dt.files);
    });

    // Handle click upload
    fileInput.addEventListener("change", function () {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            const ext = file.name.split('.').pop().toLowerCase();

            if (ext !== 'pdf' && ext !== 'txt') {
                showStatus("Please upload a .pdf or .txt file.", "error");
                selectedFile = null;
                runBtn.disabled = true;
                fileMsg.textContent = "Drag & Drop a PDF/TXT or click to browse";
                return;
            }

            selectedFile = file;
            fileMsg.innerHTML = `<strong>Selected:</strong> ${file.name}`;
            runBtn.disabled = false;
            showStatus("", "");
        }
    }

    // Handle Run Tool
    runBtn.addEventListener("click", async () => {
        if (!selectedFile) return;

        runBtn.disabled = true;
        showStatus("Analyzing document. This may take 10-30 seconds...", "loading");

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const res = await fetch("/api/analyze", {
                method: "POST",
                body: formData
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Failed to analyze document");
            }

            const data = await res.json();

            showStatus("", "");
            populateResults(data);
            uploadSection.classList.add("hidden");
            resultsSection.classList.remove("hidden");

        } catch (error) {
            console.error("Analysis error:", error);
            showStatus(error.message, "error");
            runBtn.disabled = false;
        }
    });

    // Reset flow
    resetBtn.addEventListener("click", () => {
        selectedFile = null;
        fileInput.value = "";
        fileMsg.textContent = "Drag & Drop a PDF/TXT or click to browse";
        statusMsg.textContent = "";
        runBtn.disabled = true;

        resultsSection.classList.add("hidden");
        uploadSection.classList.remove("hidden");
    });

    function showStatus(msg, statusClass) {
        statusMsg.textContent = msg;
        statusMsg.className = "status-msg " + statusClass;
    }

    // Populate data into the DOM
    function populateResults(data) {
        // Simple cards
        document.getElementById("res-tone").textContent = data.management_tone;
        document.getElementById("res-confidence").textContent = data.confidence_level;
        document.getElementById("res-capacity").textContent = data.capacity_utilization;

        // Forward Guidance
        document.getElementById("res-rev").textContent = data.forward_guidance.revenue;
        document.getElementById("res-margin").textContent = data.forward_guidance.margin;
        document.getElementById("res-capex").textContent = data.forward_guidance.capex;

        // Lists
        populateList("res-positives", data.key_positives);
        populateList("res-concerns", data.key_concerns);
        populateList("res-growth", data.growth_initiatives);
        populateList("res-limitations", data.limitations);

        // Raw JSON
        document.getElementById("raw-json").textContent = JSON.stringify(data, null, 2);
    }

    function populateList(elementId, items) {
        const ul = document.getElementById(elementId);
        ul.innerHTML = "";
        if (!items || items.length === 0) {
            ul.innerHTML = "<li>Not mentioned in transcript</li>";
            return;
        }
        items.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            ul.appendChild(li);
        });
    }
});
