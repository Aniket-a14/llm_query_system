import aiohttp
import tempfile
import os
from app.utils.chunking import chunk_text
from app.constants import CLAUSE_EXTRACTION_PROMPT
from app.services.llm_service import extract_clauses_from_chunks
import fitz  # PyMuPDF
import docx
import email
from email import policy

async def download_file(url: str) -> str:
    """
    Download a file from a URL and save it with the correct extension.
    """
    import urllib.parse
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to download file: {resp.status}")
            # Extract extension from URL
            parsed = urllib.parse.urlparse(url)
            filename = os.path.basename(parsed.path)
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ['.pdf', '.docx', '.eml']:
                ext = '.pdf'  # Default to .pdf if not found
            fd, temp_path = tempfile.mkstemp(suffix=ext)
            with os.fdopen(fd, 'wb') as f:
                f.write(await resp.read())
            return temp_path

def extract_text_from_pdf(path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF. Compatible with both get_text and getText.
    """
    with fitz.open(path) as doc:
        texts = []
        for page in doc:
            if hasattr(page, "get_text"):
                texts.append(page.get_text("text"))
            else:
                texts.append(page.getText("text"))
        return "\n".join(texts)

def extract_text_from_docx(path: str) -> str:
    """
    Extract text from a DOCX file using python-docx.
    """
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_eml(path: str) -> str:
    """
    Extract text from an EML file (email message).
    """
    with open(path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f, policy=policy.default)
        body = msg.get_body(preferencelist=('plain'))
        if body:
            return body.get_content()
        # Fallback: handle multipart and non-multipart
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        return payload.decode('utf-8', errors='ignore')
                    elif isinstance(payload, str):
                        return payload
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                return payload.decode('utf-8', errors='ignore')
            elif isinstance(payload, str):
                return payload
        return ""

def detect_file_type(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return 'pdf'
    elif ext == '.docx':
        return 'docx'
    elif ext == '.eml':
        return 'eml'
    else:
        raise Exception('Unsupported file type')

async def parse_documents(url: str):
    """
    Download, extract, chunk, and process a document for clause extraction.
    """
    path = await download_file(url)
    filetype = detect_file_type(path)
    if filetype == 'pdf':
        text = extract_text_from_pdf(path)
    elif filetype == 'docx':
        text = extract_text_from_docx(path)
    elif filetype == 'eml':
        text = extract_text_from_eml(path)
    else:
        raise Exception('Unsupported file type')
    os.remove(path)
    # Chunk text
    chunks = chunk_text(text)
    clause_chunks = extract_clauses_from_chunks(chunks)
    return text, clause_chunks
