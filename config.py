# Central config: loads env vars, exposes settings used across the app

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
NCBI_API_KEY = os.getenv("NCBI_API_KEY")

if ANTHROPIC_API_KEY is None:
    raise ValueError("ANTHROPIC_API_KEY is missing — check your .env file")