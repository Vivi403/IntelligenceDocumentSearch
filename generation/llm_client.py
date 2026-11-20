import ollama


def generate_answer(prompt: str, max_tokens: int = 300) -> str:
    response = ollama.chat(
        model="qwen3:4b",
        messages=[{"role": "user", "content": prompt}],
        think=False,
        options={"num_predict": max_tokens, "temperature": 0.3},
    )

    return response["message"]["content"]
