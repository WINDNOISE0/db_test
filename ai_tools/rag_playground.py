import os

from anthropic import Anthropic
from db.connections import get_engine
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import text

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")

question = "Как обеспечивается изоляция между тестами в базе данных?"
question_embedding = model.encode(question).tolist()

engine = get_engine()
with engine.connect() as conn:
    result = conn.execute(
        text("""
            SELECT content FROM knowledge_base
            ORDER BY embedding <=> :query_embedding
            LIMIT 2
        """),
        {"query_embedding": str(question_embedding)}
    )
    context_chunks = [row.content for row in result]

context = "\n".join(context_chunks)

prompt = f"""Ответь на вопрос, опираясь ТОЛЬКО на приведённый контекст. Если в контексте нет ответа — скажи, что не знаешь.

Контекст:
{context}

Вопрос: {question}
"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)