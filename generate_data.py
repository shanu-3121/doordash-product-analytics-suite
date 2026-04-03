import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Setup
fake = Faker()
random.seed(42)
np.random.seed(42)

print("Starting data generation...")

# ============================================
# STEP 1: LOAD REAL OLIST DATA
# ============================================
orders = pd.read_csv("archive/olist_orders_dataset.csv")
customers = pd.read_csv("archive/olist_customers_dataset.csv")
payments = pd.read_csv("archive/olist_order_payments_dataset.csv")

# Keep only delivered orders
orders = orders[orders['order_status'] == 'delivered'].copy()
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

print(f"✅ Loaded {len(orders):,} real delivered orders")

# ============================================
# STEP 2: CREATE USER PROFILES
# ============================================
print("Creating user profiles...")

# Get unique customers
unique_customers = customers['customer_unique_id'].unique()[:10000]  # Use 10k users

user_profiles = []
for customer_id in unique_customers:
    # 20% are DashPass subscribers (higher retention)
    is_dashpass = random.random() < 0.20
    
    # Acquisition channel
    channel = random.choice([
        'organic_search',  # 30%
        'paid_social',     # 25%
        'referral',        # 20%
        'email',           # 15%
        'paid_search'      # 10%
    ])
    
    # Device type
    device = random.choice(['iOS', 'Android', 'Web'])
    
    # US City
    city = random.choice([
        'New York', 'Los Angeles', 'Chicago',
        'Houston', 'Phoenix', 'San Francisco',
        'Seattle', 'Austin', 'Boston', 'Miami'
    ])
    
    user_profiles.append({
        'customer_id': customer_id,
        'is_dashpass': is_dashpass,
        'acquisition_channel': channel,
        'device_type': device,
        'city': city,
        'signup_date': fake.date_between(
            start_date='-2y',
            end_date='-1y'
        )
    })

users_df = pd.DataFrame(user_profiles)
print(f"✅ Created {len(users_df):,} user profiles")

# ============================================
# STEP 3: CREATE FOOD CATEGORIES
# ============================================
print("Creating food categories...")

# Real DoorDash cuisine categories with order weights
cuisine_categories = [
    'American',   # most popular
    'Mexican',
    'Japanese',
    'Italian',
    'Chinese',
    'Indian',
    'Healthy',
    'Breakfast'
]

cuisine_weights = [0.28, 0.22, 0.12, 0.12, 0.10, 0.07, 0.05, 0.04]

# Average order values per cuisine (realistic DoorDash values)
cuisine_avg_order = {
    'American': 28,
    'Mexican': 22,
    'Japanese': 35,
    'Italian': 30,
    'Chinese': 25,
    'Indian': 27,
    'Healthy': 20,
    'Breakfast': 18
}

# ============================================
# STEP 4: CREATE ORDER EVENTS
# ============================================
print("Creating order events...")

order_events = []
for _, user in users_df.iterrows():
    
    # DashPass users order more frequently
    if user['is_dashpass']:
        num_orders = random.randint(5, 25)  # High frequency
    else:
        num_orders = random.randint(1, 8)   # Lower frequency
    
    for i in range(num_orders):
        # Pick cuisine based on real weights
        cuisine = random.choices(
            cuisine_categories,
            weights=cuisine_weights
        )[0]
        
        # Order value based on cuisine + some randomness
        base_price = cuisine_avg_order[cuisine]
        order_value = round(random.uniform(
            base_price * 0.7,
            base_price * 1.5
        ), 2)
        
        # Add delivery fee (waived for DashPass)
        delivery_fee = 0 if user['is_dashpass'] else round(random.uniform(1.99, 5.99), 2)
        
        # Random order date
        order_date = fake.date_time_between(
            start_date='-1y',
            end_date='now'
        )
        
        # Order completion (95% complete, 5% cancelled)
        status = random.choices(
            ['completed', 'cancelled'],
            weights=[0.95, 0.05]
        )[0]
        
        # Delivery time in minutes
        delivery_time = random.randint(25, 65)
        
        # Rating (higher for DashPass users due to better experience)
        if status == 'completed':
            if user['is_dashpass']:
                rating = random.choices([3, 4, 5], weights=[0.1, 0.3, 0.6])[0]
            else:
                rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.2, 0.35, 0.3])[0]
        else:
            rating = None
            
        order_events.append({
            'order_id': fake.uuid4(),
            'customer_id': user['customer_id'],
            'is_dashpass': user['is_dashpass'],
            'acquisition_channel': user['acquisition_channel'],
            'device_type': user['device_type'],
            'city': user['city'],
            'cuisine_category': cuisine,
            'order_value': order_value,
            'delivery_fee': delivery_fee,
            'order_status': status,
            'order_date': order_date,
            'delivery_time_mins': delivery_time,
            'rating': rating
        })

orders_df = pd.DataFrame(order_events)
print(f"✅ Created {len(orders_df):,} order events")

# ============================================
# STEP 5: CREATE FUNNEL EVENTS
# ============================================
print("Creating funnel events...")

funnel_events = []
for _, user in users_df.iterrows():
    
    # Simulate 30 days of app sessions
    num_sessions = random.randint(5, 40)
    
    for _ in range(num_sessions):
        session_date = fake.date_time_between(
            start_date='-30d',
            end_date='now'
        )
        
        # Every session starts with app open
        funnel_events.append({
            'customer_id': user['customer_id'],
            'event': 'app_open',
            'timestamp': session_date,
            'is_dashpass': user['is_dashpass']
        })
        
        # 70% browse restaurants
        if random.random() < 0.70:
            funnel_events.append({
                'customer_id': user['customer_id'],
                'event': 'browse_restaurants',
                'timestamp': session_date + timedelta(seconds=random.randint(10, 60)),
                'is_dashpass': user['is_dashpass']
            })
            
            # 55% select a restaurant
            if random.random() < 0.55:
                funnel_events.append({
                    'customer_id': user['customer_id'],
                    'event': 'select_restaurant',
                    'timestamp': session_date + timedelta(seconds=random.randint(60, 180)),
                    'is_dashpass': user['is_dashpass']
                })
                
                # 50% add to cart
                if random.random() < 0.50:
                    funnel_events.append({
                        'customer_id': user['customer_id'],
                        'event': 'add_to_cart',
                        'timestamp': session_date + timedelta(seconds=random.randint(180, 300)),
                        'is_dashpass': user['is_dashpass']
                    })
                    
                    # 60% reach checkout
                    if random.random() < 0.60:
                        funnel_events.append({
                            'customer_id': user['customer_id'],
                            'event': 'reach_checkout',
                            'timestamp': session_date + timedelta(seconds=random.randint(300, 420)),
                            'is_dashpass': user['is_dashpass']
                        })
                        
                        # 65% complete order
                        if random.random() < 0.65:
                            funnel_events.append({
                                'customer_id': user['customer_id'],
                                'event': 'order_completed',
                                'timestamp': session_date + timedelta(seconds=random.randint(420, 540)),
                                'is_dashpass': user['is_dashpass']
                            })

funnel_df = pd.DataFrame(funnel_events)
print(f"✅ Created {len(funnel_df):,} funnel events")

# ============================================
# STEP 6: CREATE A/B TEST DATA
# ============================================
print("Creating A/B test data...")

# Experiment: New simplified checkout flow
# Control: Old 4-step checkout
# Variant: New 2-step checkout

ab_results = []
for _, user in users_df.iterrows():
    # Randomly assign to control or variant
    group = random.choice(['control', 'variant'])
    
    # Variant (new checkout) converts better
    if group == 'control':
        converted = random.random() < 0.52  # 52% conversion
    else:
        converted = random.random() < 0.61  # 61% conversion
    
    ab_results.append({
        'customer_id': user['customer_id'],
        'experiment_group': group,
        'converted': converted,
        'device_type': user['device_type'],
        'is_dashpass': user['is_dashpass']
    })

ab_df = pd.DataFrame(ab_results)
print(f"✅ Created {len(ab_df):,} A/B test records")

# ============================================
# STEP 7: SAVE ALL DATA
# ============================================
print("\nSaving all datasets...")

users_df.to_csv("data_users.csv", index=False)
orders_df.to_csv("data_orders.csv", index=False)
funnel_df.to_csv("data_funnel.csv", index=False)
ab_df.to_csv("data_ab_test.csv", index=False)

print("\n" + "="*50)
print("🎉 ALL DATA GENERATED SUCCESSFULLY!")
print("="*50)
print(f"👤 Users:        {len(users_df):,}")
print(f"📦 Orders:       {len(orders_df):,}")
print(f"🔄 Funnel events:{len(funnel_df):,}")
print(f"🧪 A/B records:  {len(ab_df):,}")
print("\nFiles saved:")
print("  ✅ data_users.csv")
print("  ✅ data_orders.csv")
print("  ✅ data_funnel.csv")
print("  ✅ data_ab_test.csv")
