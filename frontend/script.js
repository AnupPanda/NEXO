const API_BASE = "http://127.0.0.1:8000";

window.addEventListener("DOMContentLoaded", () => {
  const getModeValue = () => document.querySelector('input[name="mode"]:checked').value;
  
  const modeContainer = document.getElementById("modeContainer");
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const filesInput = document.getElementById("filesInput");
  const filePreview = document.getElementById("filePreview");
  const resultBox = document.getElementById("resultBox");
  const loadingBox = document.getElementById("loadingBox");
  const msgBox = document.getElementById("msgBox");
  const downloadBtn = document.getElementById("downloadBtn");
  const dropHint = document.getElementById("dropHint");
  const convertBtn = document.getElementById("convertBtn");

  function isMultiMode() {
    const mode = getModeValue();
    return mode === "merge_images_to_pdf" || mode === "merge_pdfs";
  }

  function updateHint() {
    const mode = getModeValue();
    const hints = {
      docx_to_pdf: "Upload one .docx file",
      ppt_to_pdf: "Upload one .pptx file",
      excel_to_pdf: "Upload one .xlsx file",
      merge_pdfs: "Upload 2+ PDF files",
      split_pdf: "Upload one PDF to split into pages",
      compress_pdf: "Upload one PDF to reduce size",
      merge_images_to_pdf: "Upload multiple JPG/PNG images",
    };
    dropHint.textContent = hints[mode] || "Upload your file";
    clearStatus();
  }

  function clearStatus() {
    filePreview.innerHTML = "";
    fileInput.value = "";
    filesInput.value = "";
    resultBox.classList.add("hidden");
    msgBox.classList.add("hidden");
    downloadBtn.classList.add("hidden");
  }

  function renderFiles(files) {
    filePreview.innerHTML = "";
    [...files].forEach(file => {
      const card = document.createElement("div");
      card.className = "file-card";
      card.innerHTML = `<div class="file-name">${file.name}</div><div class="file-size">${(file.size / 1024).toFixed(1)} KB</div>`;
      filePreview.appendChild(card);
    });
  }

  modeContainer.addEventListener("change", updateHint);
  dropZone.addEventListener("click", () => isMultiMode() ? filesInput.click() : fileInput.click());

  fileInput.addEventListener("change", () => renderFiles(fileInput.files));
  filesInput.addEventListener("change", () => renderFiles(filesInput.files));

  convertBtn.addEventListener("click", async () => {
    const formData = new FormData();
    const mode = getModeValue();
    formData.append("mode", mode);

    if (isMultiMode()) {
      if (!filesInput.files.length) return alert("Please select files first");
      [...filesInput.files].forEach(f => formData.append("files", f));
    } else {
      if (!fileInput.files[0]) return alert("Please select a file first");
      formData.append("file", fileInput.files[0]);
    }

    resultBox.classList.remove("hidden");
    loadingBox.classList.remove("hidden");
    msgBox.classList.add("hidden");
    downloadBtn.classList.add("hidden");

    try {
      const res = await fetch(`${API_BASE}/convert`, { method: "POST", body: formData });
      const data = await res.json();
      loadingBox.classList.add("hidden");
      msgBox.classList.remove("hidden");

      if (data.ok) {
        msgBox.textContent = "Conversion Successful!";
        msgBox.className = "msg-box msg-success";
        downloadBtn.classList.remove("hidden");
        downloadBtn.onclick = () => {
          const a = document.createElement("a");
          a.href = `${API_BASE}${data.url}`;
          a.download = data.file;
          a.click();
        };
      } else {
        msgBox.textContent = data.msg;
        msgBox.className = "msg-box msg-error";
      }
    } catch (err) {
      loadingBox.classList.add("hidden");
      msgBox.classList.remove("hidden");
      msgBox.textContent = "Server connection failed.";
      msgBox.className = "msg-box msg-error";
    }
  });

  updateHint();
});