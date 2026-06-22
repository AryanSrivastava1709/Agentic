# 📚 Simple RAG Pipeline using LangChain, Qdrant & Gemini

A simple Retrieval-Augmented Generation (RAG) pipeline built with **LangChain**, **Qdrant**, **HuggingFace Embeddings**, and **Google Gemini**.

> **Note:** This is **not** an asynchronous RAG pipeline. The indexing and querying processes are executed sequentially.

---

## 🚀 Features

- Load PDF documents
- Split documents into overlapping chunks
- Generate vector embeddings using HuggingFace
- Store embeddings in Qdrant Vector Database
- Retrieve relevant document chunks
- Generate answers using Google Gemini based only on retrieved context

---

## 🏗️ Architecture

```
                PDF
                 │
                 ▼
         PyPDFLoader
                 │
                 ▼
      RecursiveCharacterTextSplitter
                 │
                 ▼
    HuggingFace Embeddings (BGE)
                 │
                 ▼
        Qdrant Vector Database
                 │
                 ▼
      Similarity Search (Top Chunks)
                 │
                 ▼
        Gemini Flash Lite LLM
                 │
                 ▼
             Final Answer
```

---

# Tech Stack

- Python
- LangChain
- Qdrant
- HuggingFace Embeddings
- Google Gemini API
- Rich (Terminal UI)

---

# Project Structure

```
RAG/
│
├── index.py          # Creates embeddings and stores them in Qdrant
├── chat.py           # Retrieves context and answers user questions
├── node js.pdf       # Source document
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/<your-username>/Agentic.git

cd simple-rag
```

---

## Create a virtual environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Start Qdrant

Using Docker

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or if using Docker Compose

```bash
docker compose up -d
```

---

# Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# Step 1: Index the PDF

Run

```bash
python index.py
```

This will:

- Load the PDF
- Split into chunks
- Generate embeddings
- Store vectors in Qdrant

Output

```
Starting index....

Indexing of the documents done
```

---

# Step 2: Ask Questions

Run

```bash
python chat.py
```

Example

```
Ask something:

What is Express.js?
```

Example Output

```
Express.js is a minimal and flexible Node.js web application framework...

Refer to Page 12 for more information.
```

---

# How it Works

### 1. Load PDF

```python
PyPDFLoader
```

Reads every page from the PDF.

---

### 2. Split Documents

```python
RecursiveCharacterTextSplitter
```

- Chunk Size = 1000
- Chunk Overlap = 400

This improves retrieval quality by preserving context across chunks.

---

### 3. Generate Embeddings

Uses

```
BAAI/bge-base-en-v1.5
```

with normalized embeddings.

---

### 4. Store in Qdrant

Each chunk is stored as a vector inside the `learning_rag` collection.

---

### 5. Retrieve Similar Chunks

When a user asks a question:

- The query is converted into an embedding.
- Qdrant performs similarity search.
- The most relevant chunks are returned.

---

### 6. Generate Response

The retrieved context is injected into the system prompt and sent to Gemini Flash Lite, which answers only from the provided context.

---

# Dependencies

- langchain
- langchain-community
- langchain-qdrant
- langchain-huggingface
- sentence-transformers
- qdrant-client
- python-dotenv
- openai
- rich
- pypdf

---

# Notes

- This project uses **Google Gemini** through the OpenAI-compatible API.
- Qdrant runs locally on **localhost:6333**.
- Embeddings are generated using the **BAAI/bge-base-en-v1.5** model.
- Responses are grounded in the retrieved document context.
- Page numbers and source file information are included in the retrieved context.
- **This is a synchronous RAG implementation** and does not use asynchronous execution, streaming, or parallel retrieval.

---
