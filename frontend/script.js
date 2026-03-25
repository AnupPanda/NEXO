const API_BASE = "https://nexo-api-v2.onrender.com";

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const filesInput = document.getElementById('filesInput');
const convertBtn = document.getElementById('convertBtn');
const resultBox = document.getElementById('resultBox');
const downloadBtn = document.getElementById('downloadBtn');
const loadingBox = document.getElementById('loadingBox');
const msgBox = document.getElementById('msgBox');
const dropHint = document.getElementById('dropHint');

// --- 1. CONFIGURATION & MAPPING ---
const MULTI_MODES = ["merge_pdfs", "merge_images_to_pdf"];

// --- 2. UI INTERACTION (DRAG & DROP) ---
['dragenter', 'dragover'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-active');
    });
});

['dragleave', 'drop'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-active');
    });
});

dropZone.addEventListener('drop', (e) => {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    const files = e.dataTransfer.files;
    handleFileSelection(files, mode);
});

dropZone.onclick = () => {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    MULTI_MODES.includes(mode) ? filesInput.click() : fileInput.click();
};

// --- 3. FILE VALIDATION LOGIC ---
function handleFileSelection(files, mode) {
    if (files.length === 0) return;
    
    // Update UI text
    dropHint.innerHTML = `<span style="color: #00e5ff;">${files.length} file(s) selected:</span><br>${files[0].name}`;
    
    // Logic for Single vs Multi
    if (!MULTI_MODES.includes(mode) && files.length > 1) {
        alert("This mode only supports one file. I will use the first one.");
    }
}

[fileInput, filesInput].forEach(input => {
    input.onchange = () => {
        const mode = document.querySelector('input[name="mode"]:checked').value;
        handleFileSelection(input.files, mode);
    };
});

// --- 4. THE CORE CONVERSION ENGINE ---
convertBtn.onclick = async () => {
    const uiMode = document.querySelector('input[name="mode"]:checked').value;
    const isMulti = MULTI_MODES.includes(uiMode);
    const files = isMulti ? filesInput.files : fileInput.files;

    if (files.length === 0) {
        alert("Please upload a file first!");
        return;
    }

    // Enter Loading State
    toggleLoading(true);

    // SMART TRANSLATION: Map UI buttons to Backend route strings
    let finalMode = uiMode;
    if (uiMode === "img_to_pdf") {
        finalMode = files[0].type === "image/png" ? "png_to_pdf" : "jpg_to_pdf";
    } else if (uiMode === "pdf_to_img") {
        finalMode = "pdf_to_png"; 
    }

    const formData = new FormData();
    formData.append("mode", finalMode);

    if (isMulti) {
        Array.from(files).forEach(f => formData.append("files", f));
    } else {
        formData.append("file", files[0]);
    }

    try {
        const response = await fetch(`${API_BASE}/convert`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.msg || "Server Error");
        }

        const data = await response.json();

        // Success State
        showResult(true, data.file, `${API_BASE}${data.url}`);

    } catch (err) {
        showResult(false, err.message);
    } finally {
        toggleLoading(false);
    }
};

// --- 5. UI HELPER FUNCTIONS ---
function toggleLoading(isLoading) {
    convertBtn.disabled = isLoading;
    resultBox.classList.toggle('hidden', !isLoading && !msgBox.textContent);
    loadingBox.classList.toggle('hidden', !isLoading);
    if (isLoading) {
        msgBox.classList.add('hidden');
        downloadBtn.classList.add('hidden');
    }
}

function showResult(success, message, url = null) {
    resultBox.classList.remove('hidden');
    msgBox.classList.remove('hidden');
    msgBox.style.color = success ? "#4ade80" : "#f87171";
    msgBox.textContent = success ? "Success! File is ready." : "Error: " + message;

    if (success && url) {
        downloadBtn.classList.remove('hidden');
        downloadBtn.onclick = () => {
            const a = document.createElement('a');
            a.href = url;
            a.download = message;
            document.body.appendChild(a);
            a.click();
            a.remove();
        };
    }
}