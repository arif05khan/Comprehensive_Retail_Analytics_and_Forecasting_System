<<<<<<< HEAD
"-- Sample SQL queries" 
-- Advanced analytics queries for the Retail Analytics System

-- Monthly Sales Trends
SELECT strftime('%Y-%m', s.Date) AS Month, 
       SUM(s.Quantity * s.Price) AS TotalRevenue, 
       SUM(s.Quantity) AS TotalQuantity
FROM Sales s
GROUP BY strftime('%Y-%m', s.Date)
ORDER BY Month;

-- Customer Lifetime Value (CLV) by Region
SELECT c.Region, 
       AVG(s.TotalSpent) AS AvgCustomerValue, 
       COUNT(DISTINCT s.CustomerID) AS CustomerCount
FROM (
    SELECT CustomerID, 
           SUM(Quantity * Price) AS TotalSpent 
    FROM Sales 
    GROUP BY CustomerID
) s
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY c.Region;

-- Product Performance by Gender
SELECT p.Category, 
       c.Gender, 
       SUM(s.Quantity * s.Price) AS TotalRevenue, 
       SUM(s.Quantity) AS TotalUnitsSold
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY p.Category, c.Gender;

-- Stock Levels vs Sales Velocity
SELECT p.ProductID, 
       p.Category, 
       i.StockLevel, 
       SUM(s.Quantity) AS UnitsSoldLast30Days,
       i.StockLevel / (SUM(s.Quantity) / 30.0) AS DaysUntilStockout
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Inventory i ON s.ProductID = i.ProductID
WHERE s.Date >= date('now', '-30 days')
GROUP BY p.ProductID;

-- Top Regions by Profit Margin
SELECT c.Region, 
       SUM(s.Quantity * (s.Price - p.UnitCost)) AS TotalProfit,
       SUM(s.Quantity * s.Price) AS TotalRevenue,
       (SUM(s.Quantity * (s.Price - p.UnitCost)) / SUM(s.Quantity * s.Price) * 100) AS ProfitMargin
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY ProfitMargin DESC
LIMIT 5;

-- Sales Forecast Readiness (Prepare data for Prophet)
SELECT s.Date AS ds, 
       SUM(s.Quantity * s.Price) AS y
FROM Sales s
GROUP BY s.Date
ORDER BY s.Date;
=======
"-- Sample SQL queries" 
-- Advanced analytics queries for the Retail Analytics System

-- Monthly Sales Trends
SELECT strftime('%Y-%m', s.Date) AS Month, 
       SUM(s.Quantity * s.Price) AS TotalRevenue, 
       SUM(s.Quantity) AS TotalQuantity
FROM Sales s
GROUP BY strftime('%Y-%m', s.Date)
ORDER BY Month;

-- Customer Lifetime Value (CLV) by Region
SELECT c.Region, 
       AVG(s.TotalSpent) AS AvgCustomerValue, 
       COUNT(DISTINCT s.CustomerID) AS CustomerCount
FROM (
    SELECT CustomerID, 
           SUM(Quantity * Price) AS TotalSpent 
    FROM Sales 
    GROUP BY CustomerID
) s
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY c.Region;

-- Product Performance by Gender
SELECT p.Category, 
       c.Gender, 
       SUM(s.Quantity * s.Price) AS TotalRevenue, 
       SUM(s.Quantity) AS TotalUnitsSold
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY p.Category, c.Gender;

-- Stock Levels vs Sales Velocity
SELECT p.ProductID, 
       p.Category, 
       i.StockLevel, 
       SUM(s.Quantity) AS UnitsSoldLast30Days,
       i.StockLevel / (SUM(s.Quantity) / 30.0) AS DaysUntilStockout
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Inventory i ON s.ProductID = i.ProductID
WHERE s.Date >= date('now', '-30 days')
GROUP BY p.ProductID;

-- Top Regions by Profit Margin
SELECT c.Region, 
       SUM(s.Quantity * (s.Price - p.UnitCost)) AS TotalProfit,
       SUM(s.Quantity * s.Price) AS TotalRevenue,
       (SUM(s.Quantity * (s.Price - p.UnitCost)) / SUM(s.Quantity * s.Price) * 100) AS ProfitMargin
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY ProfitMargin DESC
LIMIT 5;

-- Sales Forecast Readiness (Prepare data for Prophet)
SELECT s.Date AS ds, 
       SUM(s.Quantity * s.Price) AS y
FROM Sales s
GROUP BY s.Date
ORDER BY s.Date;
>>>>>>> 8cd50017679ae0147a9efb214fb215ba5d665b80
