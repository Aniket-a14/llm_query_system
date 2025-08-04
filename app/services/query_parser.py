from app.services.llm_service import parse_nl_query as llm_parse_nl_query

async def parse_nl_query(question: str) -> dict:
    return llm_parse_nl_query(question)
