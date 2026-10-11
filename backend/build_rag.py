import logging
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAG_DATABASE = PROJECT_ROOT / "rag_database"
PROMPTS_DIR = PROJECT_ROOT / "training_data" / "prompts"
SCRIPTS_DIR = PROJECT_ROOT / "training_data" / "scripts"

# 1. Initialize local persistent ChromaDB
chroma_client = chromadb.PersistentClient(path=str(RAG_DATABASE))

# 2. Load the Hugging Face model locally
huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Create Collections
prompt_collection = chroma_client.get_or_create_collection(
    name="landscape_prompts", embedding_function=huggingface_ef
)
script_collection = chroma_client.get_or_create_collection(
    name="landscape_scripts", embedding_function=huggingface_ef
)

def ingest_directory(source_dir: Path, collection, record_prefix: str) -> int:
    files = sorted(path for path in source_dir.rglob("*") if path.is_file())
    if not files:
        logger.warning("No training files found in %s", source_dir)
        return 0

    for path in files:
        relative_path = path.relative_to(source_dir).as_posix()
        document_id = f"{record_prefix}_{relative_path.replace('/', '__')}"
        collection.upsert(
            documents=[path.read_text(encoding="utf-8")],
            metadatas=[
                {
                    "filename": relative_path,
                    "category": path.parent.name if path.parent != source_dir else "general",
                }
            ],
            ids=[document_id],
        )
    return len(files)


prompt_count = ingest_directory(PROMPTS_DIR, prompt_collection, "prompt")
script_count = ingest_directory(SCRIPTS_DIR, script_collection, "script")
logger.info(
    "RAG ingestion complete: %s prompt documents and %s script documents.",
    prompt_count,
    script_count,
)