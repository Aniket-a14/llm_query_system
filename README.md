
# LLM Query System

A production-ready FastAPI backend for LLM-powered document query and retrieval, supporting PDFs, DOCX, and emails. Uses Gemini for semantic search, clause extraction, and reasoning.

## 🚀 Live Demo

Try the API live at: [https://llm-query-system-gjre.onrender.com/docs](https://llm-query-system-gjre.onrender.com/docs)



## Features
- Upload or link to policy documents (PDF, DOCX, EML)
- Automatic chunking and semantic search over clauses
- Natural language query parsing and structuring
- Gemini LLM for clause extraction, decision, and explainability
- API secured with Bearer token authentication
- Modular, testable, and production-ready codebase
- Ready for cloud deployment (Render, Railway, Fly.io, etc.)


## Setup & Deployment

1. **Clone the repository & install dependencies**
   ```bash
   git clone https://github.com/Aniket-a14/llm_query_system.git
   cd llm_query_system
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your keys:
     ```
     GEMINI_API_KEY=your_gemini_key
     PINECONE_API_KEY=your_pinecone_key
     PINECONE_ENV=your_pinecone_env
     PINECONE_INDEX_NAME=llm-doc-index
     API_BEARER_TOKEN=changeme
     ```

3. **Run locally**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Deploy for free**
   - Push your code to GitHub.
   - Deploy to [Render](https://render.com), [Railway](https://railway.app), or [Fly.io](https://fly.io).
   - Set your environment variables in the platform dashboard.
   - Use the start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - Your public API will be available at e.g. `https://your-app-name.onrender.com/hackrx/run`


## API Usage

### POST `/hackrx/run`

**Request body:**
```json
{
  "documents": ["https://example.com/policy.pdf"],
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
curl -X POST https://llm-query-system-gjre.onrender.com/hackrx/run \
  -H "Authorization: Bearer changeme" \
  -H "Content-Type: application/json" \
  -d '{"documents": ["https://example.com/policy.pdf"], "questions": ["Does this policy cover knee surgery and what are the conditions?"]}'
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


## Notes & Tips
- For production, connect Pinecone/FAISS for real semantic search.
- Gemini API key required for LLM calls.
- Handles PDF, DOCX, and EML files from URLs.
- All secrets and API keys should be set as environment variables, never committed to git.
- The `/docs` endpoint provides interactive API documentation.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
