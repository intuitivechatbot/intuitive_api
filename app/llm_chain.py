from dotenv import load_dotenv
import os
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

load_dotenv()

def create_chain(model_name="gpt-4o-mini"):
    """
    Returns a memory-aware LLMChain that supports both vector-retrieved context
    and persistent conversational memory.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    llm = ChatOpenAI(
        model_name=model_name,
        openai_api_key=api_key,
        temperature=0.7
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are the founder of Intuitive Soul. Speak warmly, empathetically, spiritually."
         "Ground all answers on the provided context. If unsure, gently encourage self-reflection."
         "Speak with the tone and nuance that is represented in the blogs provided as context, encapsulate the speaker to the best of your abilites"
         "Refer to the context for tone and nuance of response."
         "Respond to users in casual conversational tone, as if you were speaking to a friend."),
        MessagesPlaceholder(variable_name="history"),
        ("system", "Retrieved context:\n{context}"),
        ("human", "{input_text}")
    ])

    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="history",
        input_key="input_text"
    )

    return LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

session_chains = {}

def get_chain(session_id: str):
    if session_id not in session_chains:
        session_chains[session_id] = create_chain()
    return session_chains[session_id]
