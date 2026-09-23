import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI


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

db = SQLDatabase(engine)


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True
)


if __name__ == "__main__":

    question = input(
        "Ask a business question: "
    )

    response = agent.invoke({
        "input": question
    })

    print("\n==============================")
    print("ANSWER")
    print("==============================")
    print(response["output"])