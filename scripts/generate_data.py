import os
import pandas as pd
import numpy as np
from faker import Faker


# Create Faker object
fake = Faker()

# Make results reproducible
np.random.seed(42)


# ==================================================
# 1. PRODUCTS
# ==================================================

categories = [
    "Skincare",
    "Haircare",
    "Makeup",
    "Fragrance",
    "Bath & Body"
]

brands = [
    "GlowCare",
    "PureSkin",
    "BeautyPlus",
    "NatureGlow",
    "FreshAura"
]

products = []

for i in range(1, 101):

    products.append({
        "product_id": i,
        "product_name": f"Product_{i}",
        "category": np.random.choice(categories),
        "brand": np.random.choice(brands),
        "price": round(np.random.uniform(10, 100), 2),
        "supplier_id": np.random.randint(1, 11)
    })

products_df = pd.DataFrame(products)


# ==================================================
# 2. SUPPLIERS
# ==================================================

suppliers = []

for i in range(1, 11):

    suppliers.append({
        "supplier_id": i,
        "supplier_name": f"Supplier_{i}",
        "delivery_days": np.random.randint(2, 15),
        "delayed_orders": np.random.randint(0, 50)
    })

suppliers_df = pd.DataFrame(suppliers)


# ==================================================
# 3. SALES
# ==================================================

sales = []

for i in range(1, 5001):

    product_id = np.random.randint(1, 101)

    quantity = np.random.randint(1, 10)

    product_price = products_df.loc[
        products_df["product_id"] == product_id,
        "price"
    ].iloc[0]

    sales.append({
        "order_id": i,
        "product_id": product_id,
        "store_id": np.random.randint(1, 21),
        "quantity": quantity,
        "sales_amount": round(product_price * quantity, 2),
        "order_date": fake.date_between(
            start_date="-12m",
            end_date="today"
        )
    })

sales_df = pd.DataFrame(sales)


# ==================================================
# 4. INVENTORY
# ==================================================

inventory = []

for product_id in range(1, 101):

    inventory.append({
        "product_id": product_id,
        "store_id": np.random.randint(1, 21),
        "stock_quantity": np.random.randint(0, 200),
        "reorder_level": np.random.randint(20, 80)
    })

inventory_df = pd.DataFrame(inventory)


# ==================================================
# 5. REVIEWS
# ==================================================

positive_reviews = [
    "Very good product",
    "I really liked this product",
    "Excellent quality",
    "Works very well",
    "Amazing product",
    "Good value for money",
    "Highly recommended"
]

negative_reviews = [
    "Very poor quality",
    "Product caused irritation",
    "Packaging was damaged",
    "Not worth the price",
    "Very disappointed",
    "Product quality was poor",
    "I would not buy this again"
]

reviews = []

for i in range(1, 2001):

    rating = np.random.randint(1, 6)

    if rating >= 4:
        review_text = np.random.choice(positive_reviews)
    else:
        review_text = np.random.choice(negative_reviews)

    reviews.append({
        "review_id": i,
        "product_id": np.random.randint(1, 101),
        "rating": rating,
        "review_text": review_text,
        "review_date": fake.date_between(
            start_date="-12m",
            end_date="today"
        )
    })

reviews_df = pd.DataFrame(reviews)


# ==================================================
# 6. CREATE DATA FOLDER
# ==================================================

os.makedirs("data", exist_ok=True)


# ==================================================
# 7. SAVE CSV FILES
# ==================================================

products_df.to_csv(
    "data/products.csv",
    index=False
)

suppliers_df.to_csv(
    "data/suppliers.csv",
    index=False
)

sales_df.to_csv(
    "data/sales.csv",
    index=False
)

inventory_df.to_csv(
    "data/inventory.csv",
    index=False
)

reviews_df.to_csv(
    "data/reviews.csv",
    index=False
)


# ==================================================
# 8. SUCCESS MESSAGE
# ==================================================

print("================================")
print("Retail data generated!")
print("================================")

print("Products:", len(products_df))
print("Suppliers:", len(suppliers_df))
print("Sales:", len(sales_df))
print("Inventory:", len(inventory_df))
print("Reviews:", len(reviews_df))