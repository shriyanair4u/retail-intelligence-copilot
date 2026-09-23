import pandas as pd
from sqlalchemy import create_engine


# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Shriya_4u@localhost:5432/retail_copilot"
)


# Read CSV files
products = pd.read_csv("data/products.csv")
suppliers = pd.read_csv("data/suppliers.csv")
sales = pd.read_csv("data/sales.csv")
inventory = pd.read_csv("data/inventory.csv")
reviews = pd.read_csv("data/reviews.csv")


print("CSV files loaded successfully!")

print("Products:", len(products))
print("Suppliers:", len(suppliers))
print("Sales:", len(sales))
print("Inventory:", len(inventory))
print("Reviews:", len(reviews))


# Load into PostgreSQL
products.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False
)

suppliers.to_sql(
    "suppliers",
    engine,
    if_exists="append",
    index=False
)

sales.to_sql(
    "sales",
    engine,
    if_exists="append",
    index=False
)

inventory.to_sql(
    "inventory",
    engine,
    if_exists="append",
    index=False
)

reviews.to_sql(
    "reviews",
    engine,
    if_exists="append",
    index=False
)


print("Data loaded into PostgreSQL successfully!")

