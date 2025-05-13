# 📈 Comprehensive Retail Analytics and Forecasting System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![SQL](https://img.shields.io/badge/SQL-SQLite-green)
![ML](https://img.shields.io/badge/ML-Prophet%2BK--means-orange)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-red)

## 🌟 Project Overview
A full-stack retail analytics solution combining **Python data processing**, **SQL database operations**, and **interactive visualizations** with machine learning-powered forecasting.
Transforming Retail Data into Actionable Insights

Project Vision:
This end-to-end analytics platform empowers retail businesses to harness their sales data through advanced SQL analytics, machine learning forecasting, and interactive visualizations. Developed as a showcase of full-stack data science capabilities, the system processes 50,000+ synthetic transactions to deliver:

60-day sales predictions using Facebook's Prophet

Customer segmentation via K-means clustering

Real-time inventory optimization alerts

Executive dashboards with drill-down capabilities

Built with scalability in mind, the architecture handles complex multi-table joins while maintaining responsive performance through query optimization and caching.

Why This Matters
Retailers often struggle with:

Disconnected data (sales, inventory, customers)

Manual reporting processes

Limited forecasting capabilities

This project demonstrates how to:
✅ Centralize retail data in a query-optimized SQLite database
✅ Automate insights with Python-powered analytics
✅ Democratize access through an intuitive Streamlit UI

```python
# Sample core functionality
def forecast_sales(df):
    model = Prophet(yearly_seasonality=True)
    model.fit(df)
    return model.make_future_dataframe(periods=60)


🚀 Key Features
Feature	                                 Implementation
Multi-table SQL Analytics	            10+ complex queries with joins
Sales Forecasting	                    Facebook Prophet (60-day horizon)
Customer Segmentation	                K-means clustering (4 segments)
Inventory Optimization	                Turnover rate calculations
Interactive Dashboard	                6-page Streamlit UI


🛠 Tech Stack
Core:
Python 3.9 (Pandas, NumPy)

SQLite (50K+ records)

Streamlit (Dashboard)


ML:
Prophet 1.1.1 (Forecasting)

scikit-learn 1.2.2 (Clustering)

Viz:

Plotly (Interactive charts)

Matplotlib (Static visuals)


📂 Project Structure
Retail_Analytics_System/
├── app.py                    # Main dashboard (600+ LOC)
├── queries.sql               # Analytical queries
├── setup_database.py         # Data generator
├── requirements.txt          # Dependencies
├── test_*.py                 # Validation scripts
└── retail_analytics.db       # Sample database


⚡ Quick Start
Clone & Setup:
git clone https://github.com/arif05khan/Retail-Analytics-System.git
cd Retail-Analytics-System
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

Initialize DB:
python setup_database.py  # Generates 50K+ records
Launch Dashboard:


streamlit run app.py
🔍 SQL Examples
sql
-- Customer Lifetime Value
SELECT 
  CustomerID,
  SUM(Quantity*Price) AS LTV,
  COUNT(OrderID) AS Orders
FROM Sales
GROUP BY CustomerID
ORDER BY LTV DESC
LIMIT 10;



🤖 Machine Learning
Prophet Forecasting:

python
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True
)
forecast = model.fit(df).predict(future)
Customer Segmentation:

python
kmeans = KMeans(n_clusters=4)
customer_agg['Cluster'] = kmeans.fit_predict(scaled_data)


📊 Sample Outputs
Dashboard Pages:

Sales Trends

Customer Segments

Inventory Health

60-Day Forecasts

Top Customers

Data Export


🚨 Troubleshooting
Common Issues:

CmdStan Installation:
python -m cmdstanpy.install_cmdstan
Memory Limits:

Add indexes to SQL tables

Use st.cache_data in Streamlit


📬 Contact
Arif Rasul Khan
ark396336@gmail.com
