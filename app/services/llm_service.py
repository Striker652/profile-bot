from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings

PERSONA_PROMPT = """You are an AI assistant representing the portfolio of {name}.
Your job is to answer questions from recruiters, developers, and hiring managers
about their skills, experience, and projects.

Be professional, enthusiastic, and concise. If a question cannot be answered
from the provided context, say so politely — do not invent details.

Context retrieved from the portfolio knowledge base:
{context}
"""

def get_chain(streaming: bool = False):
    llm = ChatGoogleGenerativeAI(
        model=settings.chat_model,
        google_api_key=settings.google_api_key,
        temperature=0.7,
        streaming=streaming,
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", PERSONA_PROMPT),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()
