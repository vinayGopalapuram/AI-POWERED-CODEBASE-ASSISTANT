from fastapi import APIRouter
from app.models.query_model import queryrequest
from app.services.embedding_service import embedding_service as es
from app.services.vector_db import search_code,format_context
from app.services.llm_service import generate_answer

router=APIRouter()

@router.post("/query")
def query_posting(request:queryrequest):
    # USED TO CONVERT THE USER QUERY INTO VECTORS 
    question = es.generate_embedding(request.question)

    # USED TO SEARCH THE PINECONE DB FOR THE TOP  RELAVANT CODE CHUNKS
    results=search_code(question,
                        request.repo_name)

    # PREPARE FOR LLM
    # That takes raw Pinecone results and creates something readable
    context=format_context(results)

    # this us used to call llm service 
    answer=generate_answer(request.question,context)

    return{
        # "question": request.question,
        # "context": context   
        "answer":answer  
    }