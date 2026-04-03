import pandas as pd

# Load the datasets
print("Loading data...")

orders = pd.read_csv("archive/olist_orders_dataset.csv")
customers = pd.read_csv("archive/olist_customers_dataset.csv")
order_items = pd.read_csv("archive/olist_order_items_dataset.csv")
payments = pd.read_csv("archive/olist_order_payments_dataset.csv")
reviews = pd.read_csv("archive/olist_order_reviews_dataset.csv")

print("Data loaded successfully! ✅")
print("="*50)

# How many rows in each dataset
print("\n📦 DATASET SIZES:")
print(f"Orders: {len(orders):,} rows")
print(f"Customers: {len(customers):,} rows")
print(f"Order Items: {len(order_items):,} rows")
print(f"Payments: {len(payments):,} rows")
print(f"Reviews: {len(reviews):,} rows")

print("\n📋 ORDERS - First look:")
print(orders.head())

print("\n📋 ORDERS - Column names:")
print(orders.columns.tolist())

print("\n📋 ORDER STATUS breakdown:")
print(orders['order_status'].value_counts())

print("\n📋 REVIEWS - Score breakdown:")
print(reviews['review_score'].value_counts().sort_index())


