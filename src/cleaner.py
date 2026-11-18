import re
import unicodedata

def clean_text(text) -> str:
    # Нормальзация Unicode и переноса строк
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Убираем управляющие символы
    text = ''.join(
        char for char in text
        if unicodedata.category(char) != "Cc" or char in "\t\n"
    )

    # Объединение слов, перенесённых через дефис
    text = re.sub(r'(?<=[а-яА-ЯёЁa-zA-Z])-\n(?=[а-яА-ЯёЁa-zA-Z])', '', text)

    # Удаление повторяющихся разделителей
    text = re.sub(r'(?m)^[ \t]*(-{3,}|\*{3,})[ \t]*\n?', '', text)

    # Удаление номеров страниц
    text = re.sub(r'(?im)^[ \t]*(страница\s*)?\d+[ \t]*\n?', '', text)
    text = re.sub(r'(?m)^[ \t]*-[ \t]*\d+[ \t]*-[ \t]*\n?', '', text)

    # Нормализация пробелов
    text = '\n'.join(
        re.sub(r'[ \t]+', ' ', line).strip()
        for line in text.split('\n')
    )

    # Удаление лишних пустых строк
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text
