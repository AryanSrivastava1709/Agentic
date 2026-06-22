from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

print("\n\n")

print("Starting index....")

PDF_PATH = Path(__file__).parent / "node js.pdf"

# load the file into python
loader = PyPDFLoader(file_path=PDF_PATH)
docs = loader.load()

# chunking the docs
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents=docs)

# creating the vector embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    encode_kwargs={"normalize_embeddings": True},
)

# creating vector db
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333/",
    collection_name="learning_rag",
)

print("Indexing of the documents done")
