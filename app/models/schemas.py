from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    documents: List[HttpUrl]
    questions: List[str]

class Clause(BaseModel):
    clause_id: Optional[str]
    text: str

class Answer(BaseModel):
    decision: str
    amount: Optional[float]
    justification: str
    referenced_clauses: List[Clause]

class QueryResponse(BaseModel):
    answers: List[Answer]
    query_id: str
