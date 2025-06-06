from app.retriever import get_retriever
from app.llm_chain import get_chain  

def ask_query(user_input: str, session_id: str) -> str:
    """
    Performs semantic search and uses LLM to generate a response.
    Falls back to GPT knowledge if vector DB yields no useful context.
    Stores memory per session.
    """
    retriever = get_retriever()
    docs = retriever.get_relevant_documents(user_input)

    if docs:
        context = "\n\n".join(doc.page_content for doc in docs if doc.page_content)
        print("✅ Using retrieved context.")
    else:
        context = "None"
        print("⚠️ No results from vector DB. Falling back to GPT knowledge.")

    print("📎 Context:\n", context)

    chain = get_chain(session_id)
    response = chain.invoke({
        "input_text": user_input,
        "context": context
    })

    return response["text"]