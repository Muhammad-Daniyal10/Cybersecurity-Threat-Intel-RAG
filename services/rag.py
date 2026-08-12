import os
from dotenv import load_dotenv

# models and vector store
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore

# langchain orchestration
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

print("Google Key Found:", bool(os.getenv("GOOGLE_API_KEY")))
print("Groq Key Found:", bool(os.getenv("GROQ_API_KEY")))
print("Pinecone Key Found:", bool(os.getenv("PINECONE_API_KEY")))

def generate_rag_response(user_query: str, index_name: str = "rag-project"):
    """
    take a user query, retrive revalant chunks from Pinecone and
    generate a grounded response using gemini
    """

    # initialize embedding model
    embeddings = HuggingFaceEmbeddings(
        model="BAAI/bge-base-en-v1.5"
    )

    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )

    #convert vector store into retriever to fetch top 3 chunks 
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    #initializ text gen model
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3
    )


    # system prompt
    system_prompt = (
        "You are a cybersecurity expert analyzing a threat report. "
        "Use the following retrieved context to answer the user's question. "
        "If you don't know the answer based ONLY on the context, say that you don't know. "
        "Keep your answer concise and factual.\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # RAG chain
    question_answer_chain = create_stuff_documents_chain(llm , prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # execute pipeline
    print(f"Executing RAG pipeline for query: '{user_query}' ...\n")
    response = rag_chain.invoke({"input": user_query})

    return response["answer"]

if __name__ == "__main__":
    test_query = "what are the primary tactics and techniques used by Midnight Blizzard / APT29?"

    try:
        answer = generate_rag_response(test_query)
        print("-- Generated Answer --")
        print(answer)

    except Exception as e:
        print(f"Error during RAG execution: {e}")