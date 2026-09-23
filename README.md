# Retail Intelligence Copilot

AI-powered retail analytics copilot that combines SQL analytics and RAG-based customer review analysis.

## Project Overview

Retail Intelligence Copilot allows business users to ask natural-language questions about:

- Sales and revenue
- Product performance
- Inventory
- Suppliers
- Customer reviews
- Product feedback

The application automatically routes questions to the appropriate system.

## Architecture

User → Streamlit → LLM Router → SQL Agent / RAG / BOTH → Business Answer

### SQL Agent
- PostgreSQL
- LangChain SQL Agent
- SQLAlchemy
- GPT-4o-mini

Used for structured business questions such as:

> What are the top 5 products by revenue?

### RAG Pipeline
- LangChain
- ChromaDB
- OpenAI Embeddings
- BM25
- GPT-4o-mini

Used for unstructured customer review questions such as:

> What are the main complaints about Product_13?

### Hybrid Retrieval

The RAG system combines:

- Vector similarity search
- BM25 keyword search
- Product metadata filtering

This improves retrieval accuracy for product-specific questions.

## Tech Stack

- Python
- LangChain
- OpenAI
- PostgreSQL
- ChromaDB
- BM25
- Streamlit
- SQLAlchemy
- Pandas
- Scikit-learn

## Project Structure

```text
retail-intelligence-copilot/
│
├── data/
├── rag/
│   ├── hybrid_retriever.py
│   ├── rag_chain.py
│   └── vector_db.py
│
├── scripts/
│   ├── generate_data.py
│   └── load_data.py
│
├── sql/
│   └── sql_agent.py
│
├── app.py
├── router.py
├── .gitignore
└── README.md


## Key Features

Natural-language retail analytics
Automatic question routing
SQL-based business analytics
RAG-based review analysis
Hybrid retrieval
Product-specific filtering
Streamlit chat interface
PostgreSQL integration
ChromaDB vector search
## Example Questions

What are the top 5 products by revenue?

What are the complaints about Product_13?

What are the sales of Product_13 and what do customers think about it?

## Future Improvements

RAG evaluation metrics
SQL safety layer
Conversation memory
Logging and monitoring
Docker deployment
Production deployment
