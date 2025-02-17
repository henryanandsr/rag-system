# **Processed Summary of RAG System**  

- **Synthetic Data Artifacts (PDF):**  
  - Collected from various internet sources and generated using an LLM.  

- **Synthetic Data Artifacts (SQL):**  
  - Sourced from open datasets on Kaggle, cleaned, and anonymized for privacy.  

- **RAG Chatbot Interface:**  
  - **Backend:** [Railway App Deployment](https://rag-system-production.up.railway.app)  
  - **Frontend:** [Hugging Face Space](https://huggingface.co/spaces/henryanand11/rag)  

- **Formatted Synthetic PDF for Fine-Tuning:**  
  - Uses **header-based structuring**:  
    - **H1 & H2 headers → "Instruction"**  
    - **Following text → "Output"**  
  - Helps create instruction-based training data for fine-tuning the model.  

## RAG Process
The system is designed to provide a RAG-based chatbot that answers questions using a combination of PDF and CSV data sources. It utilizes a retrieval-based approach with embedding models and vector search to find relevant information and uses an LLM (Groq API) to generate answers based on the context.

### Chunking Strategy
- PDF Chunking : using Py2PDF and split around 512 token with 50 token overlap
- CSV Chunking : Process row by row, each row is converted to key-value pair which key is column name

### Vector Store Setup
- Use sentence transformer to generate embedding vector for chunks
- Embedding vector will be normalized and stored inside faiss index then saved into `vector_store.index`

###  RAG Chatbot Architecture

- Retrieval:
The system retrieves the top relevant chunks for a given query using the FAISS index.
- Answer Generation:
Once the context is retrieved, the system sends the query and context to the Groq API to generate an answer based on the retrieved information.
- FastAPI:
A simple FastAPI-based server is used to expose an endpoint (/ask) where users can query the chatbot. It returns the generated answer as a response.


### Testing and Evaluation
Test Scenarios:
The chatbot was tested using various types of queries related to fast food and healthy eating based on the available data (PDF and CSV).
Evaluating the chatbot's performance involves checking if the retrieved context was accurate and if the generated answer was relevant.