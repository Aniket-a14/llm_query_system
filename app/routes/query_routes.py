from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.schemas import QueryRequest, QueryResponse
from app.services.document_parser import parse_documents
from app.services.embedding_service import get_relevant_clauses
from app.services.llm_service import get_llm_decision
from app.services.query_parser import parse_nl_query
from app.config import API_BEARER_TOKEN
import uuid

router = APIRouter(prefix="/hackrx", tags=["LLM Query"])
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_BEARER_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

@router.post("/run", response_model=QueryResponse)
async def run_query(
    req: QueryRequest,
    _: HTTPAuthorizationCredentials = Depends(verify_token)
):
    query_id = str(uuid.uuid4())
    try:
        # 1. Download and parse documents
        all_doc_text = []
        all_clause_chunks = []
        for url in req.documents:
            doc_text, clause_chunks = await parse_documents(str(url))
            all_doc_text.append(doc_text)
            all_clause_chunks.extend(clause_chunks)
        # 2. For each question, process
        answers = []
        for question in req.questions:
            structured_query = await parse_nl_query(question)
            relevant_clauses = await get_relevant_clauses(structured_query, all_clause_chunks)
            llm_result = get_llm_decision(question, structured_query, relevant_clauses)
            answers.append(llm_result)
        return {"answers": answers, "query_id": query_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
