from pathlib import Path
from src.settings import RAW_DIR
from dataclasses import dataclass
from pypdf import PdfReader
from docx import Document


@dataclass
class ExtractedDocument:
    text: str
    source: str
    file_type: str


def extract_file(file_path) -> ExtractedDocument:

    if Path(file_path).is_absolute():
        file = Path(file_path)
    else:
        file = Path(RAW_DIR / file_path)

    if not file.exists():
        raise FileNotFoundError(f"Файл по пути {Path(RAW_DIR / file_path)} не найден")

    if not file.is_file():
        raise ValueError(f"Документ не является файлом в директории")

    ext = file.suffix.lower()

    if ext == ".txt":
        content = extract_txt(file)

    elif ext == ".pdf":
        content = extract_pdf(file)

    elif ext == ".docx":
        content = extract_docx(file)

    else:
        raise ValueError("Данное расширение файла пока не поддерживается")

    return ExtractedDocument(content, str(file.resolve()), ext.lstrip("."))


def extract_txt(file_path) -> str:

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def extract_pdf(file_path) -> str:

    content = []
    reader = PdfReader(file_path)

    for page in reader.pages:

        extract_page = page.extract_text()

        if extract_page:
            content.append(extract_page)

    return "\n".join(content)


def extract_docx(file_path) -> str:

    content = []
    reader = Document(file_path)

    for parag in reader.paragraphs:

        extract_parag = parag.text
        content.append(extract_parag)

    return "\n".join(content)
