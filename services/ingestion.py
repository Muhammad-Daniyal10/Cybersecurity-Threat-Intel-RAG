import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_documents(file_path: str):
    """
    Loads a text or Markdown file and splits it into smaller chunks
    optimized for embedding and vector database storage
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
    
    #load documents into memory
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    #initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    #perform chunking
    chunks = text_splitter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    sample_file_path = os.path.join(
        os.path.dirname(__file__), "../data/apt29_report.md"
    )

    try:
        chunks = load_and_chunk_documents(sample_file_path)
        print(f"ingestion successful. Created {len(chunks)} chunks from {sample_file_path}\n")

        #display first chunk
        if chunks:
            print("--- First chunk preview ---")
            print(chunks[0].page_content[:300] + "...\n")
            print("Metadata:", chunks[0].metadata)
    except Exception as e:
        print(f"Error during ingestion: {e}")