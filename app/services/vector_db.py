from pinecone import Pinecone,ServerlessSpec
import os

from dotenv import load_dotenv

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc=Pinecone(api_key=PINECONE_API_KEY)


# index = pc.Index(PINECONE_INDEX_NAME)
# print(index.describe_index_stats())
# print(pc.list_indexes())

existing_indexes = pc.list_indexes().names()

if PINECONE_INDEX_NAME not in existing_indexes:

    pc.create_index(
        name=PINECONE_INDEX_NAME,

        # Qwen produces 1024-dimensional embeddings
        dimension=1024,

        # We'll use cosine similarity for semantic search
        metric="cosine",

        # Create a serverless index
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"Created index: {PINECONE_INDEX_NAME}")
else:
    print(f"Index already exists: {PINECONE_INDEX_NAME}")

# print(pc.list_indexes())
index = pc.Index(PINECONE_INDEX_NAME)

def store_chunks(embedded_chunks):
    vectors = []
    # Convert every embedded chunk into Pinecone format
    for chunk in embedded_chunks:

        # Create a unique ID for this code chunk
        vector_id = (
            f"{chunk['file_path']}-"
            f"{chunk['name']}-"
            f"{chunk['start_line']}"
        )
        # Metadata we want to retrieve later with the vector
        metadata = {
            "file_path": chunk["file_path"],
            "language": chunk["language"],
            "chunk_type": chunk["chunk_type"],
            "name": chunk["name"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "content": chunk["content"],
        }
        # Prepare this chunk in Pinecone's required format
        vectors.append(
            {
                "id": vector_id,"values": chunk["embedding"],"metadata": metadata,
            }
        )
    # Upload all prepared vectors to Pinecone
    index.upsert(vectors=vectors)
    print(f"Stored {len(vectors)} chunks in Pinecone")

# SEARCH PINECONE SUING THE USER QUERY THAT WAS VECTORIZED IN QUERY ROUTER

def search_code(query_vector,top_k=5):
    results=index.query(
        vector=query_vector,top_k=top_k,include_metadata=True
    )
    # AS THE PINECONE RETURN SDK RESPONSE OBJECT AND NOT A PY DICT SO WE CONVERT THAT INTO PY DICT 
    matches=[]
    for match in results.matches:
        matches.append({
            "id":match.id,"score":match.score,"metadata":match.metadata
        })
    return matches

def format_context(matches):
    context = ""
    for match in matches:
        metadata = match["metadata"]
        context += f"""
File: {metadata["file_path"]}
Type: {metadata["chunk_type"]}
Name: {metadata["name"]}
Lines: {metadata["start_line"]}-{metadata["end_line"]}

Code:
{metadata["content"]}

-------------------------
"""

    return context