from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import ( DATA_PATH, CHUNK_OVERLAP,CHUNK_SIZE,TOP_K_RETRIVAL,TEXT_EMBEDDING_MODEL)
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

def load_and_split() -> list[Document]:
    loader = PyPDFLoader(str(DATA_PATH))
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)

def build_vector_store() ->InMemoryVectorStore:
    chunks = load_and_split()
    embeddings = OpenAIEmbeddings(model= TEXT_EMBEDDING_MODEL)
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(chunks)
    return vector_store

def build_retriever():
    vector_store = build_vector_store()
    return vector_store.as_retriever(search_kwargs={"k": TOP_K_RETRIVAL})

def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


