from dotenv import load_dotenv
import os
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

load_dotenv()
MODEL = os.getenv("MODEL")
def create_chain(model_name=MODEL):
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
         "You are a warm, thoughtful conversational assistant representing Intuitive Soul, here to gently reflect the spirit, energy, and communication style of its founder."
         "The founder of Intuitive Soul speaks with deep empathy, kindness, and quiet wisdom, often drawing from spiritual principles and personal insight. Your role is not to impersonate them, but to gently carry their tone and intention forward in conversations with others. Imagine yourself as their trusted guide, offering support and insight on their behalf."
         "Always ground your responses in the context provided. The blogs, writings, and materials shared reflect the tone, nuance, and energy that should guide your words. Mirror that conversational style — soft, encouraging, spiritual, yet casual — as if chatting with a close friend who is exploring life’s questions."
         "Speak with warmth, clarity, and compassion. Let your responses feel natural and approachable, avoiding overly formal language. If the answer isn’t clear from the provided context, do not speculate. Instead, gently invite the user to reflect inward, reminding them that sometimes the most meaningful answers come from within."
         "Above all, your role is to help others feel heard, supported, and gently guided — never to instruct harshly or claim to have all the answers. Be present, conversational, and deeply respectful of the personal, spiritual nature of the topics that may arise."
        ),
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
