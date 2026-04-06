import base64
import os
from dotenv import load_dotenv

from mistralai.client import Mistral

_client: Mistral | None = None

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")


def extract_text(file_bytes: bytes):
    """Extract text from a document using Mistral OCR.

    Returns extracted markdown text.
    """
    client = Mistral(api_key=api_key)

    encoded = base64.standard_b64encode(file_bytes).decode("utf-8")
    source = {
        "type": "document_url",
        "document_url": f"data:application/pdf;base64,{encoded}",
    }

    response = client.ocr.process(
        model="mistral-ocr-latest",
        document=source,
    )

    return "\n\n".join(page.markdown for page in response.pages)
