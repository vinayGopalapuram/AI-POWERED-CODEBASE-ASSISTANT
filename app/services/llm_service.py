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
You are an AI codebase assistant.

Answer the user's question using only the provided code context.

If the answer cannot be determined from the provided context,
say that there is not enough information.

User Question:
{question}

Relevant Code Context:
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