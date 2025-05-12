import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
n_sales = 50000
n_customers = 1000
n_products = 500
dates = [datetime(2024, 1, 1) + timedelta(days=x) for x in range(365)]
categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
customers = [f'CUST{str(i).zfill(5)}' for i in range(1, n_customers + 1)]
products = [f'PROD{str(i).zfill(4)}' for i in range(1, n_products + 1)]

# Sales data
sales_data = {
    'OrderID': [f'ORD{str(i).zfill(6)}' for i in range(1, n_sales + 1)],
    'CustomerID': [random.choice(customers) for _ in range(n_sales)],
    'ProductID': [random.choice(products) for _ in range(n_sales)],
    'Date': [random.choice(dates) for _ in range(n_sales)],
    'Quantity': [random.randint(1, 10) for _ in range(n_sales)],
    'Price': [round(random.uniform(10, 500), 2) for _ in range(n_sales)]
}

# Customer data
customer_data = {
    'CustomerID': customers,
    'Age': [random.randint(18, 80) for _ in range(n_customers)],
    'Gender': [random.choice(['Male', 'Female']) for _ in range(n_customers)],
    'Region': [random.choice(['North', 'South', 'East', 'West']) for _ in range(n_customers)]
}

# Product data
product_data = {
    'ProductID': products,
    'Category': [random.choice(categories) for _ in range(n_products)],
    'UnitCost': [round(random.uniform(5, 200), 2) for _ in range(n_products)]
}

# Inventory data
inventory_data = {
    'ProductID': products,
    'StockLevel': [random.randint(10, 500) for _ in range(n_products)],
    'RestockDate': [random.choice(dates) for _ in range(n_products)]
}

# Create DataFrames
sales_df = pd.DataFrame(sales_data)
customer_df = pd.DataFrame(customer_data)
product_df = pd.DataFrame(product_data)
inventory_df = pd.DataFrame(inventory_data)

# Create SQLite database
conn = sqlite3.connect('retail_analytics.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        OrderID TEXT PRIMARY KEY,
        CustomerID TEXT,
        ProductID TEXT,
        Date TEXT,
        Quantity INTEGER,
        Price REAL,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID TEXT PRIMARY KEY,
        Age INTEGER,
        Gender TEXT,
        Region TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        ProductID TEXT PRIMARY KEY,
        Category TEXT,
        UnitCost REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inventory (
        ProductID TEXT PRIMARY KEY,
        StockLevel INTEGER,
        RestockDate TEXT,
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
''')

# Insert data
sales_df.to_sql('Sales', conn, if_exists='replace', index=False)
customer_df.to_sql('Customers', conn, if_exists='replace', index=False)
product_df.to_sql('Products', conn, if_exists='replace', index=False)
inventory_df.to_sql('Inventory', conn, if_exists='replace', index=False)

# Create indexes for performance
cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_date ON Sales(Date)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_customer ON Sales(CustomerID)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_sales_product ON Sales(ProductID)')

# Commit and close
conn.commit()
conn.close()

print("Database 'retail_analytics.db' created and populated successfully.")