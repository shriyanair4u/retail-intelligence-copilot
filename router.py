
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate



from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


router_prompt = ChatPromptTemplate.from_template("""
You are a router for a retail analytics application.

Classify the user's question into exactly ONE category:

RAG
SQL
BOTH

Use these rules:

RAG:
Questions about customer reviews, opinions, complaints,
satisfaction, product feedback, or review sentiment.

SQL:
Questions about sales, revenue, inventory, quantities,
products, suppliers, dates, or numerical business data.

BOTH:
Questions that require both numerical business data
and customer review information.

User question:
{question}

Return ONLY one word:
RAG, SQL, or BOTH.
""")


def route_question(question):

    messages = router_prompt.format_messages(
        question=question
    )

    response = llm.invoke(messages)

    return response.content.strip().upper()


if __name__ == "__main__":

    question = input("Enter your question: ")

    route = route_question(question)

    print("\n==============================")
    print("ROUTE")
    print("==============================")
    print(route)