import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go  # Added for Sales Forecasting page
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler  # Added for segment_customers
import sqlite3
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Retail Analytics & Forecasting System", layout="wide")

# Database connection
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect('retail_analytics.db')
    conn.row_factory = sqlite3.Row
    return conn

# Load data using SQL
@st.cache_data
def load_data():
    conn = get_db_connection()
    sales_query = '''
        SELECT s.OrderID, s.CustomerID, s.ProductID, s.Date, s.Quantity, s.Price,
               s.Quantity * s.Price AS Revenue, c.Age, c.Gender, c.Region,
               p.Category, p.UnitCost, i.StockLevel, i.RestockDate
        FROM Sales s
        JOIN Customers c ON s.CustomerID = c.CustomerID
        JOIN Products p ON s.ProductID = p.ProductID
        JOIN Inventory i ON s.ProductID = i.ProductID
    '''
    df = pd.read_sql_query(sales_query, conn)
    df['Date'] = pd.to_datetime(df['Date'])
    df['RestockDate'] = pd.to_datetime(df['RestockDate'])
    conn.close()
    return df

# Customer segmentation
def segment_customers(df):
    customer_agg = df.groupby('CustomerID').agg({
        'Revenue': 'sum',
        'OrderID': 'count',
        'Age': 'first',
        'Region': 'first'
    }).rename(columns={'OrderID': 'OrderCount'})
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(customer_agg[['Revenue', 'OrderCount', 'Age']])
    
    kmeans = KMeans(n_clusters=4, random_state=42)
    customer_agg['Cluster'] = kmeans.fit_predict(scaled_data)
    
    cluster_labels = {
        0: 'Low-Value',
        1: 'High-Value',
        2: 'Frequent Buyers',
        3: 'New Customers'
    }
    customer_agg['Segment'] = customer_agg['Cluster'].map(cluster_labels)
    return customer_agg

# Sales forecasting
def forecast_sales(df):
    df_prophet = df.groupby('Date')['Revenue'].sum().reset_index()
    df_prophet.columns = ['ds', 'y']
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
    model.fit(df_prophet)
    future = model.make_future_dataframe(periods=60)
    forecast = model.predict(future)
    return model, forecast

# Inventory turnover
def calculate_inventory_turnover(df):
    turnover = df.groupby('ProductID').agg({
        'Quantity': 'sum',
        'StockLevel': 'first',
        'UnitCost': 'first',
        'Category': 'first'
    })
    turnover['TurnoverRate'] = turnover['Quantity'] / turnover['StockLevel']
    return turnover

# Top customers
def get_top_customers(df, n=10):
    top_customers = df.groupby('CustomerID').agg({
        'Revenue': 'sum',
        'OrderID': 'count'
    }).rename(columns={'OrderID': 'OrderCount'}).sort_values('Revenue', ascending=False).head(n)
    return top_customers

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", [
    "Overview",
    "Sales Analysis",
    "Customer Segmentation",
    "Inventory Management",
    "Sales Forecasting",
    "Top Customers"
])

# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
category = st.sidebar.multiselect("Select Product Category", options=df['Category'].unique(), default=df['Category'].unique())
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
min_date = pd.to_datetime(date_range[0])
max_date = pd.to_datetime(date_range[1])

# Filter data using SQL
conn = get_db_connection()
query_filtered = '''
    SELECT s.OrderID, s.CustomerID, s.ProductID, s.Date, s.Quantity, s.Price,
           s.Quantity * s.Price AS Revenue, c.Age, c.Gender, c.Region,
           p.Category, p.UnitCost, i.StockLevel, i.RestockDate
    FROM Sales s
    JOIN Customers c ON s.CustomerID = c.CustomerID
    JOIN Products p ON s.ProductID = p.ProductID
    JOIN Inventory i ON s.ProductID = i.ProductID
    WHERE s.Date >= ? AND s.Date <= ? AND p.Category IN ({}) AND c.Region IN ({})
'''
cat_placeholders = ','.join('?' * len(category))
reg_placeholders = ','.join('?' * len(region))
query_filtered = query_filtered.format(cat_placeholders, reg_placeholders)
filtered_df = pd.read_sql_query(query_filtered, conn, params=[min_date, max_date] + category + region)
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
filtered_df['RestockDate'] = pd.to_datetime(filtered_df['RestockDate'])
conn.close()

# Page: Overview
if page == "Overview":
    st.title("Retail Analytics Dashboard")
    
    # KPIs
    total_sales = filtered_df['Revenue'].sum()
    total_orders = filtered_df['OrderID'].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    customer_retention = filtered_df['CustomerID'].nunique() / df['CustomerID'].nunique() * 100
    profit_margin = ((filtered_df['Revenue'].sum() - (filtered_df['Quantity'] * filtered_df['UnitCost']).sum()) / filtered_df['Revenue'].sum() * 100) if filtered_df['Revenue'].sum() > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    col4.metric("Customer Retention", f"{customer_retention:.2f}%")
    col5.metric("Profit Margin", f"{profit_margin:.2f}%")
    
    # Summary
    st.subheader("Business Summary")
    st.write(f"Analyzing {len(filtered_df)} transactions from {filtered_df['Date'].min().strftime('%Y-%m-%d')} to {filtered_df['Date'].max().strftime('%Y-%m-%d')}.")
    st.write(f"Covering {len(filtered_df['CustomerID'].unique())} unique customers and {len(filtered_df['ProductID'].unique())} products.")
    
    # Quick Stats
    st.subheader("Quick Stats")
    stats_query = '''
        SELECT p.Category, COUNT(DISTINCT s.CustomerID) AS UniqueCustomers,
               AVG(s.Quantity * s.Price) AS AvgTransaction
        FROM Sales s
        JOIN Products p ON s.ProductID = p.ProductID
        GROUP BY p.Category
    '''
    conn = get_db_connection()
    stats_df = pd.read_sql_query(stats_query, conn)
    conn.close()
    st.dataframe(stats_df)

# Page: Sales Analysis
elif page == "Sales Analysis":
    st.title("Sales Analysis")
    
    # Sales Trend
    st.subheader("Sales Trend Over Time")
    sales_trend = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
    fig1 = px.line(sales_trend, x='Date', y='Revenue', title="Daily Sales Trend")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Sales by Category
    st.subheader("Sales by Category")
    category_sales = filtered_df.groupby('Category').agg({'Revenue': 'sum', 'Quantity': 'sum'}).reset_index()
    fig2 = px.bar(category_sales, x='Category', y='Revenue', title="Sales by Product Category", text='Quantity')
    st.plotly_chart(fig2, use_container_width=True)
    
    # Sales by Region
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby('Region')['Revenue'].sum().reset_index()
    fig3 = px.pie(region_sales, names='Region', values='Revenue', title="Sales Distribution by Region")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Monthly Sales Growth
    st.subheader("Monthly Sales Growth")
    monthly_sales = filtered_df.resample('M', on='Date')['Revenue'].sum().reset_index()
    monthly_sales['Growth'] = monthly_sales['Revenue'].pct_change() * 100
    fig4 = px.bar(monthly_sales, x='Date', y='Growth', title="Monthly Sales Growth (%)")
    st.plotly_chart(fig4, use_container_width=True)

# Page: Customer Segmentation
elif page == "Customer Segmentation":
    st.title("Customer Segmentation")
    
    customer_segments = segment_customers(filtered_df)
    
    # Scatter Plot
    st.subheader("Customer Segments")
    fig5 = px.scatter(customer_segments, x='OrderCount', y='Revenue', color='Segment', size='Age',
                      title="Customer Segmentation (Orders vs Revenue)",
                      hover_data=['CustomerID', 'Region'])
    st.plotly_chart(fig5, use_container_width=True)
    
    # Segment Summary
    st.subheader("Segment Summary")
    segment_summary = customer_segments.groupby('Segment').agg({
        'Revenue': ['mean', 'sum'],
        'OrderCount': 'mean',
        'Age': 'mean',
        'CustomerID': 'count'
    }).round(2)
    segment_summary.columns = ['Avg Revenue', 'Total Revenue', 'Avg Orders', 'Avg Age', 'Customer Count']
    st.dataframe(segment_summary)
    
    # Segment Distribution
    st.subheader("Segment Distribution")
    segment_dist = customer_segments['Segment'].value_counts().reset_index()
    segment_dist.columns = ['Segment', 'Count']
    fig6 = px.bar(segment_dist, x='Segment', y='Count', title="Customer Segment Distribution")
    st.plotly_chart(fig6, use_container_width=True)

# Page: Inventory Management
elif page == "Inventory Management":
    st.title("Inventory Management")
    
    turnover = calculate_inventory_turnover(filtered_df)
    
    # Turnover Rate
    st.subheader("Inventory Turnover Rate")
    fig7 = px.histogram(turnover, x='TurnoverRate', nbins=50, title="Distribution of Inventory Turnover Rates",
                        color='Category')
    st.plotly_chart(fig7, use_container_width=True)
    
    # Low Stock Alert
    st.subheader("Low Stock Alerts")
    low_stock = filtered_df[filtered_df['StockLevel'] < 20][['ProductID', 'Category', 'StockLevel', 'RestockDate']].drop_duplicates()
    st.dataframe(low_stock)
    
    # Stock vs Sales
    st.subheader("Stock vs Sales")
    stock_sales = filtered_df.groupby('ProductID').agg({'Quantity': 'sum', 'StockLevel': 'first', 'Category': 'first'}).reset_index()
    fig8 = px.scatter(stock_sales, x='StockLevel', y='Quantity', title="Stock Levels vs Sales Quantity",
                      color='Category', hover_data=['ProductID'])
    st.plotly_chart(fig8, use_container_width=True)
    
    # Overstocked Products
    st.subheader("Overstocked Products")
    overstock = turnover[turnover['TurnoverRate'] < 0.1][['ProductID', 'Category', 'StockLevel', 'TurnoverRate']]
    st.dataframe(overstock)

# Page: Sales Forecasting
elif page == "Sales Forecasting":
    st.title("Sales Forecasting")
    
    model, forecast = forecast_sales(filtered_df)
    
    # Forecast Plot
    st.subheader("Sales Forecast (Next 60 Days)")
    fig9 = go.Figure()
    fig9.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig9.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dash')))
    fig9.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dash')))
    fig9.update_layout(title="Sales Forecast", xaxis_title="Date", yaxis_title="Revenue")
    st.plotly_chart(fig9, use_container_width=True)
    
    # Forecast Components
    st.subheader("Forecast Components")
    fig10 = model.plot_components(forecast)
    st.pyplot(fig10)
    
    # Forecast Summary
    st.subheader("Forecast Summary")
    forecast_summary = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10).round(2)
    st.dataframe(forecast_summary)

# Page: Top Customers
elif page == "Top Customers":
    st.title("Top Customers")
    
    top_customers = get_top_customers(filtered_df)
    
    # Bar Plot
    st.subheader("Top 10 Customers by Revenue")
    fig11 = px.bar(top_customers, x='CustomerID', y='Revenue', title="Top Customers by Revenue",
                   text='OrderCount')
    st.plotly_chart(fig11, use_container_width=True)
    
    # Detailed Table
    st.subheader("Customer Details")
    top_customer_details = filtered_df[filtered_df['CustomerID'].isin(top_customers.index)][
        ['CustomerID', 'Age', 'Gender', 'Region', 'Revenue']
    ].groupby('CustomerID').agg({
        'Age': 'first',
        'Gender': 'first',
        'Region': 'first',
        'Revenue': 'sum'
    }).reset_index()
    st.dataframe(top_customer_details)

# Download filtered data
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "filtered_retail_data.csv", "text/csv")