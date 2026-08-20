# 🛡️ Cybersecurity Threat Intel RAG

A full-stack, advanced Retrieval-Augmented Generation (RAG) application engineered to analyze cybersecurity threat reports. This system allows users to interactively query threat intelligence data using a real-time streaming interface, backed by a robust, memory-aware retrieval pipeline.

## 📖 Project Description

This project goes beyond standard vector search by implementing a **Two-Stage Retrieval Architecture**. It initially fetches a wide net of context using dense embeddings and then re-scores those chunks using a Cross-Encoder model. Combined with a History-Aware Retriever, the AI maintains conversational memory across multiple turns, seamlessly understanding follow-up questions while completely filtering out irrelevant data.

## ✨ Key Features

* **Two-Stage Advanced Retrieval:** Uses Pinecone (`bge-base-en-v1.5`) for initial vector search, heavily filtered and re-scored by a Hugging Face Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) for pinpoint accuracy.
* **Multi-Turn Conversational Memory:** Implements a LangChain history-aware pipeline that secretly reformulates follow-up questions to maintain conversational context.
* **Real-Time Streaming UI:** Features a custom Vanilla JS frontend (parsing Markdown to HTML in real-time) and a FastAPI backend to stream AI responses token-by-token.
* **Optimized Containerization:** Fully containerized using Docker, strictly utilizing CPU-only PyTorch wheels to drastically reduce image size and ensure highly efficient deployments.

## 🛠️ Tech Stack

* **Backend & API:** Python 3.12, FastAPI, Uvicorn
* **AI & Orchestration:** LangChain, Groq (Llama-3.3-70b-versatile)
* **Vector Store & Embeddings:** Pinecone, Hugging Face (`bge-base-en-v1.5`)
* **Reranking:** Cross-Encoder (`ms-marco-MiniLM-L-6-v2`)
* **Frontend:** HTML, CSS, JavaScript (`marked.js`)

---

## 🚀 How to Run Locally

### Prerequisites
You will need Python 3.12+ installed, along with API keys for [Groq](https://console.groq.com/) and [Pinecone](https://www.pinecone.io/).

### 1. Clone the Repository
```bash
git clone [https://github.com/Muhammad-Daniyal10/Cybersecurity-Threat-Intel-RAG.git]
(https://github.com/Muhammad-Daniyal10/Cybersecurity-Threat-Intel-RAG)
cd Cybersecurity-Threat-Intel-RAG
```

### 2. Set Up the Environment
Create a virtual environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory and add your API keys:
```env
GROQ_API_KEY="your_groq_api_key_here"
PINECONE_API_KEY="your_pinecone_api_key_here"
```

### 4. Run the Application
Start the Uvicorn server:
```bash
uvicorn main:app --reload
```
Open your web browser and navigate to `http://127.0.0.1:8000`.

---

## 🐳 How to Run with Docker

This application is fully containerized and optimized for lightweight CPU deployment.

### 1. Build the Image
Build the Docker image. (The `--no-cache` flag ensures you are pulling the latest dependencies and code).
```bash
docker build --no-cache -t threat-intel-rag .
```

### 2. Run the Container
Spin up the container, mapping port 8000 and passing in your environment variables:
```bash
docker run --rm -p 8000:8000 --env-file .env threat-intel-rag
```
The application will be live at `http://127.0.0.1:8000`.

---

## 💡 Usage

Once the interface is running, type your query into the input box (labeled *"Ask Chatbot"*). 
* Ask initial questions like: *"What is APT29?"*
* Follow up naturally: *"What specific persistence mechanisms do they use?"* 
* The system will automatically stream the generated answer, parse tables and lists, and append the specific source documents at the end of the response.