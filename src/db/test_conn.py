from db.repositories import save_document

document_id = save_document("oop-ru.pdf", "pdf", "data/raw/oop-ru.pdf")

print("ID документа:", document_id)
