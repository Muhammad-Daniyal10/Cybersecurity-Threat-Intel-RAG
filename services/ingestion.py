import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_directory(directory_path: str):
    """
    Loads all files from a directory and splits them into smaller
    chunks optimized for embedding and vector database
    """

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"File not found at {directory_path}")


    print(f"Scanning Directory: {directory_path}...")

    #load documents into memory
    loader = DirectoryLoader(directory_path, glob="**/*.*", use_multithreading=True, show_progress=True)

    documents = loader.load()

    if not documents:
        raise ValueError("No documents found in directory")

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
    data_directory_path = os.path.join(
        os.path.dirname(__file__), "../data"
    )

    try:
        chunks = load_and_chunk_directory(data_directory_path)
        print(f"ingestion successful. Created {len(chunks)} chunks from {data_directory_path}\n")

        #display first chunk
        if chunks:
            print("--- First chunk preview ---")
            print(chunks[0].page_content[:300] + "...\n")
            print("Metadata:", chunks[0].metadata)
    except Exception as e:
        print(f"Error during ingestion: {e}")