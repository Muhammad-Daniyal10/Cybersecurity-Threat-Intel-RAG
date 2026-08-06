# RAG API with FastAPI & LangChain

A Retrieval-Augmented Generation (RAG) backend built to intelligently query and synthesize answers from custom documents. This project demonstrates modern AI orchestration, vector embeddings, and backend API development.

## 🚀 Tech Stack
* **API Framework:** FastAPI
* **AI Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **Environment:** Python

## 🧠 System Architecture
*(Coming soon: Architecture diagram showing the ingestion and retrieval pipelines)*

1. **Ingestion Pipeline:** Documents are parsed, split into optimized chunks, converted into vector embeddings, and stored locally in ChromaDB.
2. **Retrieval Logic:** User queries are embedded and used to perform a similarity search against the vector database to find the most relevant context.
3. **Generation Chain:** The retrieved context and original query are passed through a LangChain prompt template to an LLM, generating a highly accurate, source-backed response.

## 🛠️ Local Setup
*(Setup instructions and environment configuration steps will be documented here once the build is complete.)*

## 👨‍💻 Author
**Muhammad Daniyal**
Software Engineering, Information Technology University (ITU)