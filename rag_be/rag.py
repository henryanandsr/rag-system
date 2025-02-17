from data_loader import retrieve_chunks

# Generate answer using Groq API
def generate_answer(client, query, context):
    prompt = f"Gunakan informasi ini untuk menjawab pertanyaa, apabila jawaban tidak ada maka katakan saya tidak tahu.\n\nContext: {context}\n\nQuestion: {query}\nAnswer:"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# RAG pipeline
def rag_answer(client,model, index, chunks, query):
    context_chunks = retrieve_chunks(model, index, chunks, query)
    context = " ".join(context_chunks)
    return generate_answer(client, query, context)