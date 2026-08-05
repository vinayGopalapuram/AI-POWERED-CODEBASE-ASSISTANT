from sentence_transformers import SentenceTransformer


MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

# This service is responsible for converting
# our code chunks into numerical vectors (embeddings).
class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            MODEL_NAME,
            trust_remote_code=True
        )


    # This function converts ONE piece of code into ONE vectirs.
    def generate_embedding(self, content: str):
        embedding = self.model.encode(
            content,
            normalize_embeddings=True
        )
        return embedding.tolist()


    def generate_embeddings(self, chunks: list):

        embedded_chunks = []
        for chunk in chunks:
            embedding = self.generate_embedding(
                chunk["content"]
            )

            embedded_chunk = {
                **chunk,
                "embedding": embedding
            }

            embedded_chunks.append(embedded_chunk)

        print(embedded_chunks)
        return embedded_chunks


embedding_service = EmbeddingService()