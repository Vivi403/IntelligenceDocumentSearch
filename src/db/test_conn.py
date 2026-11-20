from generation.llm_client import generate_answer
from generation.prompt import build_prompt
from src.search.hybrid_search import hybrid_search
from src.embedder import load_model
from src.db.qdrant_store import get_qdrant_client

model = load_model()
cl = get_qdrant_client()

inp = "Что такое Python?"

context = [i["content"] for i in hybrid_search(inp, model, cl)]
prompt = build_prompt(context, inp)
answer = generate_answer(prompt)

print(answer)
