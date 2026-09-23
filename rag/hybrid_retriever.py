import os
import re

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


load_dotenv()


# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)


# ---------------------------------
# LOAD REVIEWS
# ---------------------------------

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

documents = []

for _, row in reviews.iterrows():

    documents.append(
        Document(
            page_content=str(row["review_text"]),
            metadata={
                "review_id": int(row["review_id"]),
                "product_id": int(row["product_id"]),
                "rating": int(row["rating"]),
                "review_date": str(row["review_date"])
            }
        )
    )


# ---------------------------------
# BM25 INDEX
# ---------------------------------

tokenized_documents = [
    document.page_content.lower().split()
    for document in documents
]

bm25 = BM25Okapi(tokenized_documents)


# ---------------------------------
# CHROMA
# ---------------------------------

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    collection_name="product_reviews",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


# ---------------------------------
# HYBRID SEARCH
# ---------------------------------

def hybrid_search(question, k=5):

    # Check for product number
    match = re.search(
        r"product[_\s-]?(\d+)",
        question,
        re.IGNORECASE
    )

    product_id = None

    if match:
        product_id = int(match.group(1))


    # -----------------------------
    # VECTOR SEARCH
    # -----------------------------

    if product_id:

        vector_docs = vectorstore.similarity_search(
            question,
            k=k,
            filter={
                "product_id": product_id
            }
        )

    else:

        vector_docs = vectorstore.similarity_search(
            question,
            k=k
        )


    # -----------------------------
    # BM25 SEARCH
    # -----------------------------

    query_tokens = question.lower().split()

    bm25_scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )


    bm25_docs = []

    for index in ranked_indices:

        document = documents[index]

        if product_id:

            if document.metadata["product_id"] != product_id:
                continue

        bm25_docs.append(document)

        if len(bm25_docs) >= k:
            break


    # -----------------------------
    # COMBINE RESULTS
    # -----------------------------

    combined = []

    seen_ids = set()

    for document in vector_docs + bm25_docs:

        review_id = document.metadata["review_id"]

        if review_id not in seen_ids:

            combined.append(document)

            seen_ids.add(review_id)

    return combined[:k]


# ---------------------------------
# TEST
# ---------------------------------

if __name__ == "__main__":

    question = input(
        "Enter your question: "
    )

    results = hybrid_search(
        question,
        k=5
    )

    print("\n==============================")
    print("HYBRID SEARCH RESULTS")
    print("==============================")

    print(
        "Documents retrieved:",
        len(results)
    )

    for document in results:

        print("\n------------------------------")

        print(
            "Review ID:",
            document.metadata["review_id"]
        )

        print(
            "Product ID:",
            document.metadata["product_id"]
        )

        print(
            "Rating:",
            document.metadata["rating"]
        )

        print(
            "Review:",
            document.page_content
        )