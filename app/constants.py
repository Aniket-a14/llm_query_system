# Prompt templates and constants

CLAUSE_EXTRACTION_PROMPT = """
Given the following insurance policy text, extract all clauses with their IDs (if present) and text. Return as a list of objects with 'clause_id' and 'text'.
"""

QUERY_PARSING_PROMPT = """
Parse the following user query into a structured JSON object with fields: age, gender, procedure, location, policy_duration_months. If a field is missing, set it to null.
"""

LLM_DECISION_PROMPT = """
Given the user query and the relevant policy clauses, decide if the claim should be approved or rejected, the payout amount, and provide a justification. Return a valid JSON with keys: decision, amount, justification, referenced_clauses (with clause_id and text).
"""
