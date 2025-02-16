import gradio as gr
import requests

API_URL = "http://backend:80"

def ask_question(question):
    try:
        response = requests.post(f"{API_URL}/ask", json={"question": question})
        response.raise_for_status()
        return response.json().get("answer", "No answer found.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

iface = gr.Interface(
    fn=ask_question,
    inputs="text",
    outputs="text",
    title="RAG System",
    description="Ask a question and get an answer from the RAG model."
)

iface.launch(server_name="0.0.0.0", server_port=7860)