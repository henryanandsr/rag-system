import PyPDF2
import faiss

# Extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# Extract information from csv
def chunk_per_row(df):
    chunks = []
    for _, row in df.iterrows():
        chunk = ','.join([f"{col}: {row[col]}" for col in df.columns])
        chunks.append(chunk)
    return chunks

# Chunk text
def chunk_text(text, chunk_size=512, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Retrieve relevant chunks for a query
def retrieve_chunks(model, index, chunks, query,top_k=3):
    query_embedding = model.encode([query])
    faiss.normalize_L2(query_embedding)
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]
