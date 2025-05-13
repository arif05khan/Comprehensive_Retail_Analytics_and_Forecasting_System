Comprehensive Retail Analytics and Forecasting System
Hi there! I’m Arif Rasul, and this is my Comprehensive Retail Analytics and Forecasting System project, completed in May 2025. I built this to dive deep into retail data—think sales trends, customer behavior, and inventory management—using tools I love, like Python, SQLite, and Streamlit. It’s a full-fledged system with a multi-page dashboard, machine learning for forecasting and segmentation, and a ton of SQL queries to pull meaningful insights. I’ve deployed it on Streamlit Cloud (though there’s a small hiccup I’ll mention later). This project is a big part of my portfolio to showcase my skills in Python, SQL, and data visualization for HR evaluations, and I’m excited to share it with you!
What’s This Project About?
I wanted to create a system that helps retail businesses make sense of their data. I generated a synthetic dataset with 50,000 sales records, 1,000 customers, 500 products, and inventory details, all stored in an SQLite database. Using Python and SQL, I extracted insights like total sales, customer segments, and inventory turnover. I also used machine learning—K-means clustering for customer segmentation and Prophet for sales forecasting. The best part? I built an interactive dashboard with Streamlit and Plotly to visualize everything, from sales trends to low-stock alerts.
Objectives
Here’s what I set out to do:

Build a scalable analytics system using SQL to pull data efficiently.
Add advanced analytics, like clustering customers with K-means and forecasting sales with Prophet.
Create an easy-to-use, multi-page dashboard for sales, customers, and inventory insights.
Show off my skills in Python, SQL, and data visualization for HR and portfolio purposes.

Features
This project has a lot packed into it! Here’s what you’ll find:

SQL-Powered Data Extraction: I wrote over 10 complex SQL queries (check out queries.sql, analytics.sql, and advanced_queries.sql) with joins, aggregations, and filters to get the data I need.
Key Metrics: Total sales, number of orders, average order value, customer retention rate, and profit margins.
Visualizations: Interactive charts using Plotly—line charts for trends, bar charts for categories, pie charts for regions, scatter plots, histograms, and even forecast plots.
Machine Learning:
Used K-means clustering to group customers based on their behavior.
Used Prophet to forecast sales for the next 60 days.


Inventory Management: Calculated turnover rates, flagged low-stock products (under 20 units), and detected overstock.
Top Customers: Highlighted high-value customers by revenue and order count.
Export Data: You can download filtered data as a CSV right from the dashboard.

Technologies I Used
I picked tools that I’m comfortable with and that fit the project’s needs:

Python: For data processing (with Pandas and NumPy), clustering (scikit-learn), and forecasting (Prophet).
SQLite: To manage the database and run complex SQL queries.
Streamlit: To build the multi-page interactive dashboard.
Plotly: For all the dynamic charts and visualizations.
GitHub: For version control and hosting the project.

How to Set It Up
If you want to run this project locally, here’s how to get started. I’ve tested this on Windows, but it should work on other systems too with minor tweaks.

Clone the Repository:
git clone https://github.com/arif05khan/Comprehensive_Retail_Analytics_and_Forecasting_System.git
cd Comprehensive_Retail_Analytics_and_Forecasting_System/Retail_Analytics_System


Set Up a Virtual Environment:
python -m venv venv
venv\Scripts\activate  # On Windows


Install the Dependencies:I’ve included a requirements.txt file with all the packages you’ll need.
pip install -r requirements.txt


Install CmdStan for Prophet:Prophet needs CmdStan for forecasting, so let’s set that up.
python -m cmdstanpy.install_cmdstan --version 2.36.0


Set the CMDSTAN Environment Variable:On Windows, you’ll need to tell Prophet where CmdStan is.
set CMDSTAN=C:\Users\Arif Rasul Khan\.cmdstan\cmdstan-2.36.0

Replace Arif Rasul Khan with your Windows username.

Set Up the Database:I’ve included a script to create and populate the SQLite database.
python setup_database.py

You can also use the SQL files directly:

schema.sql: Creates the database tables.
seed_data.sql: Adds sample data.


Run the Streamlit App:Now you’re ready to launch the dashboard!
streamlit run app.py

Open http://localhost:8501 in your browser, and you’ll see the dashboard in action.


What’s in the Project?
Here’s a quick look at the files in the repository:

app.py: The main Streamlit app that runs the dashboard.
setup_database.py: Script to set up the SQLite database.
test_forecast_sales.py: A test script for the sales forecasting feature.
schema.sql: SQL file with the database schema.
seed_data.sql: SQL file with sample data to populate the database.
queries.sql: SQL queries for data analysis (joins, aggregations, etc.).
analytics.sql: More advanced queries, like monthly sales trends and customer lifetime value.
advanced_queries.sql: Even more SQL queries, like customer segmentation and seasonality analysis.
data/historical_sales.csv: Sample sales data for forecasting.
docs/database_schema.md: Documentation of the database tables and structure.
docs/usage_guide.md: A guide on how to use the app.
requirements.txt: List of Python packages needed.

Database Schema
I’ve documented the database structure in docs/database_schema.md. It includes four main tables:

Sales: 50,000 records with order details (OrderID, CustomerID, ProductID, Date, Quantity, Price).
Customers: 1,000 records with customer info (CustomerID, Age, Gender, Region).
Products: 500 records with product details (ProductID, Category, UnitCost).
Inventory: 500 records with inventory data (ProductID, StockLevel, RestockDate).

Deployment
I deployed the dashboard on Streamlit Cloud so anyone can access it online. However, there’s a small issue with the deployment (more on that below), so I recommend running it locally for now. If you run into any issues, let me know—I’m happy to help!
Challenges I Faced
Building this project wasn’t always smooth sailing. Here are a few challenges I ran into and how I tackled them:

Large Dataset with Complex Joins: Handling 50,000 sales records with SQL joins was slow at first. I added indexes to the database tables and optimized my queries, which made a big difference.
Streamlit Cloud Compatibility: Getting the app to work on Streamlit Cloud was tricky. I had to specify exact versions for dependencies (like holidays==0.29) and use Python 3.9 to match their runtime.
Dashboard Complexity vs. Usability: I wanted the dashboard to do a lot, but I didn’t want it to feel overwhelming. I organized it into multiple pages (like sales, customers, inventory) with clear navigation.


Screenshots



References
Here are some resources I found helpful while building this project:

Streamlit Documentation
Prophet Documentation
Plotly Documentation
SQLite Documentation
scikit-learn Documentation


Thanks for checking out my project! If you have any questions or ideas, feel free to reach out.
