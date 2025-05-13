-- Advanced SQL queries for deeper insights

-- Customer Segmentation by Spending Tiers
SELECT c.CustomerID, 
       c.Region, 
       SUM(s.Quantity * s.Price) AS TotalSpent,
       CASE 
           WHEN SUM(s.Quantity * s.Price) > 1000 THEN 'High Spender'
           WHEN SUM(s.Quantity * s.Price) BETWEEN 500 AND 1000 THEN 'Medium Spender'
           ELSE 'Low Spender'
       END AS SpendingTier
FROM Sales s
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY c.CustomerID;

-- Sales Growth Rate by Category
WITH MonthlySales AS (
    SELECT p.Category, 
           strftime('%Y-%m', s.Date) AS Month, 
           SUM(s.Quantity * s.Price) AS Revenue
    FROM Sales s
    JOIN Products p ON s.ProductID = p.ProductID
    GROUP BY p.Category, strftime('%Y-%m', s.Date)
)
SELECT Category, 
       Month, 
       Revenue,
       (Revenue - LAG(Revenue) OVER (PARTITION BY Category ORDER BY Month)) / LAG(Revenue) OVER (PARTITION BY Category ORDER BY Month) * 100 AS GrowthRate
FROM MonthlySales
ORDER BY Category, Month;

-- Inventory Restock Alerts
SELECT p.ProductID, 
       p.Category, 
       i.StockLevel, 
       i.RestockDate,
       SUM(s.Quantity) AS UnitsSoldLast7Days,
       CASE 
           WHEN i.StockLevel < SUM(s.Quantity) * 2 THEN 'Urgent Restock Needed'
           ELSE 'Monitor Stock'
       END AS RestockStatus
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Inventory i ON s.ProductID = i.ProductID
WHERE s.Date >= date('now', '-7 days')
GROUP BY p.ProductID;

-- Regional Sales Seasonality
SELECT c.Region, 
       strftime('%m', s.Date) AS Month, 
       SUM(s.Quantity * s.Price) AS TotalRevenue
FROM Sales s
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY c.Region, strftime('%m', s.Date)
ORDER BY c.Region, Month;