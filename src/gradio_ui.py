import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"

def ask_question(question):
    response = requests.post(f"{API_URL}/ask", json={"question": question})
    return response.json().get("answer", "No answer found.")

iface = gr.Interface(
    fn=ask_question,
    inputs="text",
    outputs="text",
    title="RAG System",
    description="Ask a question and get an answer from the RAG model."
)

iface.launch()