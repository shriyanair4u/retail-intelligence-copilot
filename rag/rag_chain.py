from rag.hybrid_retriever import hybrid_search
import re
import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    collection_name="product_reviews",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a retail customer-review analyst.

Answer the user's question using ONLY the customer
reviews provided in the context.

If the context does not contain enough information,
say that the available reviews do not provide enough
information.

Context:
{context}

Question:
{question}

Give a concise business-friendly answer.
""")


def ask_question(question):

    documents = hybrid_search(
        question,
        k=5
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)

    return response.content, documents