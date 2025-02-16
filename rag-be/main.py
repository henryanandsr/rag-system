from data_loader import extract_text_from_pdf, chunk_text, chunk_per_row
from rag import rag_answer
from sentence_transformers import SentenceTransformer
import faiss
import groq
import numpy as np
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

vector_store_path = "../doc/vector_store.index"
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Groq client
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path)
client = groq.Client(api_key=os.environ["GROQ_API_KEY"])

# Load PDF and preprocess
pdf_text = extract_text_from_pdf("../doc/makanan-sehat.pdf")
pdf_chunks = chunk_text(pdf_text)

# Load CSV Files
df = pd.read_csv("../doc/fast-food.csv")
csv_chunks = chunk_per_row(df)

# Combine Chunks Files
chunks = pdf_chunks+csv_chunks

if os.path.exists(vector_store_path):
    print("Reload vector datastore")
    index = faiss.read_index(vector_store_path)
else: 
    # Generate embeddings and build FAISS index
    chunk_embeddings = model.encode(chunks)
    faiss.normalize_L2(chunk_embeddings)

    dimension = chunk_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(chunk_embeddings))
    faiss.write_index(index, "../doc/vector_store.index")


class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    ans = rag_answer(client, model, index, chunks, query.question)
    return {"answer": ans}