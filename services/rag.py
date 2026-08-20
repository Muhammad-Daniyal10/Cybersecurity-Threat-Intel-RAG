import os
from dotenv import load_dotenv

# models and vector store
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore

# langchain orchestration
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv(override=True)

print("Groq Key Found:", bool(os.getenv("GROQ_API_KEY")))
print("Pinecone Key Found:", bool(os.getenv("PINECONE_API_KEY")))

def generate_rag_response(user_query: str, index_name: str = "rag-project"):
    """
    take a user query, retrieve relevant chunks from Pinecone and
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

    # convert vector store into retriever to fetch top 3 chunks 
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # initialize text gen model
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5
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


def stream_rag_response(user_query: str, chat_history: list | None, index_name: str = "rag-project"):
    """
    takes a user query and chat history, retrieves relevant chunks and streams
    the generated response back token by token with citations
    """
    if chat_history is None:
        chat_history = []

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.5)

    # 1. Format the incoming history array into LangChain message objects
    formatted_history = []
    for msg in chat_history:
        if msg.get("role") == "user":
            formatted_history.append(HumanMessage(content=msg.get("content")))
        elif msg.get("role") == "assistant":
            formatted_history.append(AIMessage(content=msg.get("content")))

    # 2. History-Aware Retriever Prompt
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 3. Main Q&A Prompt
    qa_system_prompt = (
        "You are a cybersecurity expert analyzing a threat report. "
        "Use the following retrieved context to answer the user's question. "
        "Keep your answer concise and factual.\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # stream output
    print(f"Streaming RAG pipeline for query: '{user_query}' \n")

    retrieved_docs = []

    # Pass in both the query and the formatted chat history
    for chunk in rag_chain.stream({"input": user_query, "chat_history": formatted_history}):
        if "context" in chunk:
            retrieved_docs = chunk["context"]

        if "answer" in chunk:
            yield chunk["answer"]

    if retrieved_docs:
        yield "\n\n**Sources:**\n"

        unique_sources = set()
        for doc in retrieved_docs:
            source_path = doc.metadata.get("source", "Unknown Document")
            clean_source = source_path.split("/")[-1].split("\\")[-1]
            unique_sources.add(clean_source)

        for source in unique_sources:
            yield f"- {source}\n"