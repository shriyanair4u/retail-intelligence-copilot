import os

import pandas as pd
from sqlalchemy import create_engine

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)

query = """
SELECT
    review_id,
    product_id,
    rating,
    review_text,
    review_date
FROM reviews
"""

reviews = pd.read_sql(query, engine)

print("Reviews loaded:", len(reviews))

documents = []

for _, row in reviews.iterrows():

    document = Document(
        page_content=str(row["review_text"]),
        metadata={
            "review_id": int(row["review_id"]),
            "product_id": int(row["product_id"]),
            "rating": int(row["rating"]),
            "review_date": str(row["review_date"])
        }
    )

    documents.append(document)

print("Documents created:", len(documents))

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db",
    collection_name="product_reviews"
)

print("Documents in ChromaDB:", vectorstore._collection.count())

print("ChromaDB created successfully!")