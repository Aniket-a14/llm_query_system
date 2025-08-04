# LLM Query System

A FastAPI backend for LLM-powered document query and retrieval, supporting PDFs, DOCX, and emails. Uses Gemini for semantic search, clause extraction, and reasoning.

## Features
- Upload or link to policy documents (PDF, DOCX, EML)
- Chunking and semantic search over clauses
- Natural language query parsing
- Gemini LLM for decision and explainability
- API secured with Bearer token

## Setup

1. **Clone repo & install dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure `.env`**

```
GEMINI_API_KEY=your_gemini_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_env
PINECONE_INDEX_NAME=llm-doc-index
API_BEARER_TOKEN=changeme
```

3. **Run the app**

```bash
uvicorn app.main:app --reload
```

## Example Usage

**POST** `/hackrx/run`

Request body:
```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": [
    "Does this policy cover knee surgery and what are the conditions?",
    "What is the waiting period for cataract surgery?"
  ]
}
```

**Headers:**
```
Authorization: Bearer changeme
Content-Type: application/json
```

**Sample curl:**
```bash
curl -X POST http://localhost:8000/hackrx/run \
  -H "Authorization: Bearer changeme" \
  -H "Content-Type: application/json" \
  -d '{"documents": "https://example.com/policy.pdf", "questions": ["Does this policy cover knee surgery and what are the conditions?"]}'
```

**Sample Response:**
```json
{
  "answers": [
    {
      "decision": "approved",
      "amount": 200000,
      "justification": "Knee surgery is covered after 2 months per clause 4.3(b).",
      "referenced_clauses": [
        {
          "clause_id": "4.3(b)",
          "text": "Knee surgery is covered after 60 days of policy inception."
        }
      ]
    }
  ],
  "query_id": "..."
}
```

## Notes
- For production, connect Pinecone/FAISS for real semantic search.
- Gemini API key required for LLM calls.
- Handles PDF, DOCX, and EML files from URLs.
