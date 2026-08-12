import os
from dotenv import load_dotenv

#Import the google GenAI embedding model and Pinecone vector store
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

#import local ingestion logic
from services.ingestion import load_and_chunk_directory

#load API keys from .env
load_dotenv()

def create_and_upload_vector_db(directory_path: str, index_name: str = "rag-project"):
    """
    Ingests a document, converts it into embeddings using gemini, 
    and uploads the vectors to a pinecone serverless index
    """

    #load and chunk the document
    print(f"loading and chunking data from {directory_path}...")
    chunks = load_and_chunk_directory(directory_path)

    if not chunks:
        print("Error: No document chunks created")
        return None
    
    #initialize gemini embedding model
    print("Initializing Hugging Face Local embeddings.....")
    embeddings = HuggingFaceEmbeddings(
        model="BAAI/bge-base-en-v1.5"
    )

    #verify Pinecone config
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    if index_name not in pc.list_indexes().names():
        raise ValueError(
            f"Index '{index_name}' does not exist in Pinecone."
        )
    
    #upload chunks and their embeddings to pinecone
    print(f"Uploading {len(chunks)} chunks to pinecone index '{index_name}'..")

    #from_documents automatically embeds the text and handles upload
    vector_store = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=index_name
    )

    print("Upload Complete")
    return vector_store

if __name__ == "__main__":
    sample_directory_path = os.path.join(
        os.path.dirname(__file__), "../data"
    )

    try:
        create_and_upload_vector_db(sample_directory_path, "rag-project")
    except Exception as e:
        print(f"Error during database upload: {e}")