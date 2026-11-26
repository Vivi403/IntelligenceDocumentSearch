const API_BASE = "";

const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const selectedFile = document.getElementById("selected-file");
const uploadStatus = document.getElementById("upload-status");
const documentsList = document.getElementById("documents-list");
const refreshButton = document.getElementById("refresh-documents");
const questionForm = document.getElementById("question-form");
const questionInput = document.getElementById("question-input");
const chatMessages = document.getElementById("chat-messages");
const queryStatus = document.getElementById("query-status");

function setStatus(element, message, isError = false) {
  element.textContent = message;
  element.classList.toggle("error", isError);
}

function safeText(value) {
  return String(value ?? "");
}

function formatFileSize(bytes) {
  if (!Number.isFinite(Number(bytes))) return "";
  const size = Number(bytes);
  if (size < 1024) return `${size} Б`;
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} КБ`;
  return `${(size / (1024 * 1024)).toFixed(1)} МБ`;
}

function renderDocuments(documents) {
  documentsList.replaceChildren();

  if (!Array.isArray(documents) || documents.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "Документы пока не загружены";
    documentsList.append(empty);
    return;
  }

  for (const documentData of documents) {
    const item = document.createElement("div");
    item.className = "document-item";

    const icon = document.createElement("div");
    icon.className = "document-icon";
    icon.textContent = safeText(documentData.extension || "DOC").replace(".", "").toUpperCase();

    const info = document.createElement("div");
    info.className = "document-info";

    const name = document.createElement("strong");
    name.textContent = safeText(documentData.filename || documentData.name || "Документ");

    const meta = document.createElement("span");
    meta.textContent = documentData.size ? formatFileSize(documentData.size) : "Добавлен в базу знаний";

    const removeButton = document.createElement("button");
    removeButton.className = "delete-button";
    removeButton.type = "button";
    removeButton.textContent = "×";
    removeButton.setAttribute("aria-label", `Удалить документ ${name.textContent}`);
    removeButton.title = "Удалить документ";
    removeButton.addEventListener("click", () => removeDocument(documentData.id, removeButton));

    info.append(name, meta);
    item.append(icon, info, removeButton);
    documentsList.append(item);
  }
}

async function removeDocument(documentId, button) {
  if (!documentId) {
    setStatus(queryStatus, "Не удалось определить документ для удаления.", true);
    return;
  }

  button.disabled = true;
  try {
    const response = await fetch(`${API_BASE}/documents/${documentId}`, { method: "DELETE" });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Не удалось удалить документ");
    await loadDocuments();
  } catch (error) {
    button.disabled = false;
    setStatus(queryStatus, error.message || "Ошибка удаления документа.", true);
  }
}

async function loadDocuments() {
  documentsList.innerHTML = '<div class="empty-state">Загрузка списка документов…</div>';

  try {
    const response = await fetch(`${API_BASE}/documents`);
    if (!response.ok) throw new Error(`Ошибка загрузки списка (${response.status})`);

    const data = await response.json();
    renderDocuments(Array.isArray(data) ? data : data.documents || []);
  } catch (error) {
    documentsList.textContent = "";
    const message = document.createElement("div");
    message.className = "empty-state";
    message.textContent = error.message || "Не удалось загрузить документы";
    documentsList.append(message);
  }
}

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = fileInput.files[0];

  if (!file) {
    setStatus(uploadStatus, "Сначала выберите файл.", true);
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  setStatus(uploadStatus, "Загружаю документ…");

  try {
    const response = await fetch(`${API_BASE}/documents`, {
      method: "POST",
      body: formData,
    });
    const data = await response.json().catch(() => ({}));

    if (!response.ok) throw new Error(data.detail || "Не удалось загрузить файл");

    setStatus(uploadStatus, data.message || "Документ успешно загружен.");
    fileInput.value = "";
    selectedFile.textContent = "";
    await loadDocuments();
  } catch (error) {
    setStatus(uploadStatus, error.message || "Ошибка загрузки.", true);
  }
});

fileInput.addEventListener("change", () => {
  selectedFile.textContent = fileInput.files[0]
    ? `Выбран файл: ${fileInput.files[0].name}`
    : "";
  setStatus(uploadStatus, "");
});

refreshButton.addEventListener("click", loadDocuments);

function addMessage(text, role) {
  const message = document.createElement("div");
  message.className = `message ${role}`;
  message.textContent = text;
  chatMessages.append(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

document.querySelector(".suggestion")?.addEventListener("click", () => {
  questionInput.value = "Какие основные темы раскрыты в документах?";
  questionInput.focus();
});

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    questionForm.requestSubmit();
  }
});

questionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();

  if (!question) {
    setStatus(queryStatus, "Введите вопрос.", true);
    return;
  }

  addMessage(question, "user");
  questionInput.value = "";
  setStatus(queryStatus, "Ищу ответ в документах…");

  try {
    const response = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await response.json().catch(() => ({}));

    if (!response.ok) throw new Error(data.detail || "Не удалось получить ответ");

    const answer = data.answer || data.response || data.result || "Ответ получен, но его текст отсутствует.";
    addMessage(answer, "assistant");
    setStatus(queryStatus, "");
  } catch (error) {
    setStatus(queryStatus, error.message || "Ошибка поиска.", true);
  }
});

loadDocuments();
