import pandas as pd

# Load data
orders = pd.read_csv("archive/olist_orders_dataset.csv")
customers = pd.read_csv("archive/olist_customers_dataset.csv")
order_items = pd.read_csv("archive/olist_order_items_dataset.csv")
payments = pd.read_csv("archive/olist_order_payments_dataset.csv")
reviews = pd.read_csv("archive/olist_order_reviews_dataset.csv")

# Convert timestamps to dates
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

print("="*50)
print("📅 DATE RANGE OF DATA:")
print(f"First order: {orders['order_purchase_timestamp'].min()}")
print(f"Last order: {orders['order_purchase_timestamp'].max()}")

print("\n" + "="*50)
print("💰 PAYMENT ANALYSIS:")
print(f"Average order value: ${payments['payment_value'].mean():.2f}")
print(f"Highest order value: ${payments['payment_value'].max():.2f}")
print(f"Total revenue: ${payments['payment_value'].sum():,.2f}")
print("\nPayment methods used:")
print(payments['payment_type'].value_counts())

print("\n" + "="*50)
print("🔄 REPEAT CUSTOMER ANALYSIS:")
# How many customers ordered more than once?
repeat_customers = customers.groupby('customer_unique_id').size()
total_customers = len(repeat_customers)
repeat = len(repeat_customers[repeat_customers > 1])
one_time = len(repeat_customers[repeat_customers == 1])
print(f"Total unique customers: {total_customers:,}")
print(f"Customers who ordered ONCE: {one_time:,} ({one_time/total_customers*100:.1f}%)")
print(f"Customers who ordered MORE THAN ONCE: {repeat:,} ({repeat/total_customers*100:.1f}%)")

print("\n" + "="*50)
print("⏱️ DELIVERY TIME ANALYSIS:")
# Calculate delivery time in days
delivered = orders[orders['order_status'] == 'delivered'].copy()
delivered['delivery_days'] = (
    delivered['order_delivered_customer_date'] - 
    delivered['order_purchase_timestamp']
).dt.days
print(f"Average delivery time: {delivered['delivery_days'].mean():.1f} days")
print(f"Fastest delivery: {delivered['delivery_days'].min()} days")
print(f"Slowest delivery: {delivered['delivery_days'].max()} days")

print("\n" + "="*50)
print("📦 TOP 5 PRODUCT CATEGORIES:")
products = pd.read_csv("archive/olist_products_dataset.csv")
category_translation = pd.read_csv("archive/product_category_name_translation.csv")
products = products.merge(category_translation, on='product_category_name', how='left')
items_with_products = order_items.merge(products[['product_id','product_category_name_english']], on='product_id')
print(items_with_products['product_category_name_english'].value_counts().head())
