
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import settings
from app.rag.embedding import get_embeddings


splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
embeddings = get_embeddings()


def load_file(file):
    """STEP 1: Read one file and return its pages as documents."""
    if file.suffix.lower() == ".pdf":
        return PyPDFLoader(str(file)).load()
    if file.suffix.lower() == ".txt":
        return TextLoader(str(file), encoding="utf-8").load()
    return []  # ignore other file types


def make_chunks(folder):
    """STEP 2: Read every file in a folder and cut it into chunks."""
    all_chunks = []
    for file in folder.iterdir():
        documents = load_file(file)
        chunks = splitter.split_documents(documents)
        for chunk in chunks:
            # Skip chunks with almost no text
            if len(chunk.page_content.strip()) < 50:
                continue
            # Metadata = labels attached to each chunk. Used for citations.
            chunk.metadata["collection"] = folder.name
            chunk.metadata["source"] = file.name
            # PyPDFLoader counts pages from 0, humans count from 1
            if "page" in chunk.metadata:
                chunk.metadata["page"] = chunk.metadata["page"] + 1
            all_chunks.append(chunk)
    return all_chunks


def store_chunks(chunks, collection_name):
    """STEP 3: Embed the chunks and save them in Qdrant."""
    QdrantVectorStore.from_documents(
        chunks,
        embeddings,
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        collection_name=collection_name,
        force_recreate=True,  # delete and rebuild, so re-running never duplicates
    )


# STEP 4: Do it for every folder inside data/
for folder in Path("data").iterdir():
    if not folder.is_dir():
        continue
    chunks = make_chunks(folder)
    if not chunks:
        print(f"{folder.name}: no chunks found, skipping")
        continue
    store_chunks(chunks, folder.name)
    print(f"{folder.name}: {len(chunks)} chunks stored")