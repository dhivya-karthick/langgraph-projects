from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

TEXT_EMBEDDING_MODEL = os.getenv("TEXT_EMBEDDING_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")
TEMPERATURE = os.getenv("TEMPERATURE")
TOP_K_RETRIVAL = int(os.getenv("TOP_K_RETRIVAL"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
DATA_PATH = Path("src/data/order_info.pdf")