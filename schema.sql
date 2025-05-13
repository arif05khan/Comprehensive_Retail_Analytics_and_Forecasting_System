-- Schema for Comprehensive Retail Analytics Database 
 
CREATE TABLE sales ( 
    id INTEGER PRIMARY KEY, 
    date TEXT NOT NULL, 
    amount REAL NOT NULL 
); 
 
CREATE TABLE customers ( 
    customer_id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    total_spent REAL NOT NULL 
); 
 
-- Insert sample data 
INSERT INTO sales (date, amount) VALUES ('2024-01-01', 100.50); 
INSERT INTO customers (name, total_spent) VALUES ('John Doe', 500.00); 
