from fastapi import APIRouter

from app.models.github_model import GitHubRequest
from app.services.github_service import clone_repository
from app.services.chunking_services import chunk_all_files
from app.services.file_service import extract_files
from app.services.embedding_service import embedding_service
from app.services.vector_db import store_chunks

router = APIRouter()


@router.post("/github")
def clone_github_repository(request: GitHubRequest):

    repo_path = clone_repository(request.repo_url)

    extracted_files=extract_files(repo_path)

    chunks=chunk_all_files(extracted_files)

    # TESTING THE FIRST CHUNK

    # first_chunk = chunks[0]
    # content = first_chunk["content"]
    # embedding = embedding_service.generate_embedding(content)
    # print("\nFIRST AST CHUNK:")
    # print(first_chunk)
    # print("\nEMBEDDING VECTOR:")
    # print(embedding)
    # print("\nVECTOR DIMENSION:")
    # print(len(embedding))

    # SENDING ALL THE CHUNKS TO THE EMBEDDING SERCIVES 
    embedded_chunks = embedding_service.generate_embeddings(chunks)

    print("TOTAL AST CHUNKS:", len(chunks))
    print("TOTAL EMBEDDED CHUNKS:", len(embedded_chunks))
    print("EMBEDDING DIMENSION:", len(embedded_chunks[0]["embedding"]))


    store_chunks(embedded_chunks)


    
    return {
        "message": "Repository cloned successfully",
        "repo_path": repo_path,
        "total_files": len(extracted_files),
        "total_chunks": len(chunks)
    }