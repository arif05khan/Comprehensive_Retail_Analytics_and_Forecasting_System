import sys
import traceback
import pandas as pd
import sqlite3
from prophet import Prophet

try:
    # Load data (same as in app.py)
    conn = sqlite3.connect('retail_analytics.db')
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
    conn.close()

    # Prepare data for forecasting (same as forecast_sales in app.py)
    df_prophet = df.groupby('Date')['Revenue'].sum().reset_index()
    df_prophet.columns = ['ds', 'y']

    # Run forecasting
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
    model.fit(df_prophet)
    future = model.make_future_dataframe(periods=60)
    forecast = model.predict(future)

    print("Forecasting completed successfully!")
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(5))
except Exception as e:
    print("Error:", e)
    traceback.print_exc(file=sys.stdout)