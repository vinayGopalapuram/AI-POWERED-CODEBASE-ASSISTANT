import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

client=Groq(
    api_key=GROQ_API_KEY
)

def generate_answer(question: str, context: str):

    # Instructions + retrieved code + user's question
    prompt = f"""
You are an AI assistant that helps users understand a software codebase.

Answer the user's question using only the provided code context.

Guidelines:
- Give a clear and direct answer.
- Mention relevant file names, functions, or classes when useful.
- Clearly distinguish between where logic is implemented and where it is called.
- Explain the code in simple language.
- Do not mention embeddings, Pinecone, retrieval, context, or internal system details.
- Do not invent information that is not present in the provided code.
- If the answer cannot be determined from the code, clearly say so.

User Question:
{question}

Relevant Code:
{context}
"""
    # Send the question and retrieved code to the LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user","content": prompt
            }
        ]
    )
    return response.choices[0].message.content