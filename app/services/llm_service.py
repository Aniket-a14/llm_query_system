import os
from app.config import GEMINI_API_KEY
from app.constants import LLM_DECISION_PROMPT, CLAUSE_EXTRACTION_PROMPT, QUERY_PARSING_PROMPT
from typing import List, Dict, Any
import google.generativeai as genai
import json

genai.api_key = GEMINI_API_KEY

# Helper to get available models
def get_supported_model(preferred: str = "gemini-1.5-flash") -> str:
    try:
        models = [m.name for m in genai.list_models()]
        for m in models:
            if preferred in m:
                return m
        return models[0] if models else preferred
    except Exception as e:
        print(f"Error listing models: {e}")
        return preferred

GEMINI_MODEL = get_supported_model()

def clean_json_response(text: str) -> str:
    """
    Remove Markdown code block markers and extra lines from Gemini responses.
    """
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # Remove the first line (``` or ```json)
        lines = lines[1:]
        # Remove the last line if it's ```
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()

def extract_clauses_with_llm(text: str, prompt: str = None) -> List[dict]:
    """
    Extract clauses from a chunk of text using Gemini LLM.
    """
    model = genai.GenerativeModel(GEMINI_MODEL)
    if prompt is None:
        prompt = CLAUSE_EXTRACTION_PROMPT
    # Enhanced prompt for more robust extraction
    full_prompt = (
        prompt
        + "\n" + text
        + "\nReturn ONLY a valid JSON array of objects with keys 'clause_id' and 'text'. Do not include any explanation, markdown, or extra text. If no clauses are found, return an empty array []."
    )
    response = model.generate_content(full_prompt)
    try:
        cleaned = clean_json_response(response.text)
        return json.loads(cleaned)
    except Exception as e:
        print(f"extract_clauses_with_llm JSON decode error: {e}\nRaw response: {response.text}")
        return []

def extract_clauses_from_chunks(chunks: List[str]) -> List[dict]:
    """
    Process each chunk with the LLM and combine all extracted clauses.
    """
    all_clauses = []
    for i, chunk in enumerate(chunks):
        clauses = extract_clauses_with_llm(chunk)
        if isinstance(clauses, list):
            all_clauses.extend(clauses)
        else:
            print(f"Chunk {i} did not return a list, got: {type(clauses)}")
    return all_clauses

def get_embedding(text: str) -> List[float]:
    # Placeholder: Gemini embedding API or OpenAI embedding
    return [0.0] * 768

def get_llm_decision(question: str, structured_query: dict, relevant_clauses: List[dict]) -> dict:
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = (
        LLM_DECISION_PROMPT
        + f"\nUser Query: {question}\nStructured: {structured_query}\nRelevant Clauses: {relevant_clauses}\nReturn ONLY valid JSON. Do not include any explanation or markdown formatting."
    )
    response = model.generate_content(prompt)
    try:
        cleaned = clean_json_response(response.text)
        return json.loads(cleaned)
    except Exception as e:
        print(f"get_llm_decision JSON decode error: {e}\nRaw response: {response.text}")
        return {
            "decision": "error",
            "amount": None,
            "justification": "LLM output parsing failed.",
            "referenced_clauses": []
        }

def parse_nl_query(question: str) -> dict:
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = QUERY_PARSING_PROMPT + "\n" + question + "\nReturn ONLY valid JSON. Do not include any explanation or markdown formatting."
    response = model.generate_content(prompt)
    try:
        cleaned = clean_json_response(response.text)
        return json.loads(cleaned)
    except Exception as e:
        print(f"parse_nl_query JSON decode error: {e}\nRaw response: {response.text}")
        return {}
