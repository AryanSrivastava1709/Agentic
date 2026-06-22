from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from dotenv import load_dotenv
import os
from rich.markdown import Markdown
from rich.panel import Panel
from rich.console import Console

console = Console()

load_dotenv()

# embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    encode_kwargs={"normalize_embeddings": True},
)

# vector db connection
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333/",
    collection_name="learning_rag",
)


# Ask something about
user_query = input("Ask something: ")

# Relevant chunks from the vector db
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join(
    [
        f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location:{result.metadata['source']}"
        for result in search_results
    ]
)

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page number.

You should only answer the user based on the following context and navigate the user to open the right page number to know more.

Context : {context}
"""

# getting the client and ai response on the context provided
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ],
)

print("\n\n")
console.print(
    Panel(
        Markdown(response.choices[0].message.content),
        title="🤖 AI",
        border_style="green",
    )
)
