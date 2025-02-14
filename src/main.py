from data_loader import extract_text_from_pdf, chunk_text
from rag import rag_answer
from sentence_transformers import SentenceTransformer
import faiss
import groq
import numpy as np
import os
from dotenv import load_dotenv
from pathlib import Path

# Load PDF and preprocess
pdf_text = extract_text_from_pdf("doc/telkomsel.pdf")
chunks = chunk_text(pdf_text)

# Generate embeddings and build FAISS index
model = SentenceTransformer('all-MiniLM-L6-v2')
chunk_embeddings = model.encode(chunks)
faiss.normalize_L2(chunk_embeddings)
dimension = chunk_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(chunk_embeddings))

# Initialize Groq client
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path)
client = groq.Client(api_key=os.environ["GROQ_API_KEY"])

# Interactive loop
while True:
    q = input("Ask a question (or type 'exit' to quit): ")
    if q.lower() == "exit":
        break
    ans = rag_answer(client,model,index, chunks, q)
    print("Answer:", ans)