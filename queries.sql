-- Load all data with joins
SELECT s.OrderID, s.CustomerID, s.ProductID, s.Date, s.Quantity, s.Price,
       s.Quantity * s.Price AS Revenue, c.Age, c.Gender, c.Region,
       p.Category, p.UnitCost, i.StockLevel, i.RestockDate
FROM Sales s
JOIN Customers c ON s.CustomerID = c.CustomerID
JOIN Products p ON s.ProductID = p.ProductID
JOIN Inventory i ON s.ProductID = i.ProductID;

-- Filter data by date, category, and region
SELECT s.OrderID, s.CustomerID, s.ProductID, s.Date, s.Quantity, s.Price,
       s.Quantity * s.Price AS Revenue, c.Age, c.Gender, c.Region,
       p.Category, p.UnitCost, i.StockLevel, i.RestockDate
FROM Sales s
JOIN Customers c ON s.CustomerID = c.CustomerID
JOIN Products p ON s.ProductID = p.ProductID
JOIN Inventory i ON s.ProductID = i.ProductID
WHERE s.Date >= ? AND s.Date <= ? AND p.Category IN (?, ?, ?, ?, ?) AND c.Region IN (?, ?, ?, ?);

-- Sales by category and region
SELECT p.Category, c.Region, SUM(s.Quantity * s.Price) AS TotalRevenue, SUM(s.Quantity) AS TotalQuantity
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY p.Category, c.Region;

-- Customer purchase frequency
SELECT s.CustomerID, c.Age, c.Gender, c.Region, COUNT(s.OrderID) AS OrderCount,
       SUM(s.Quantity * s.Price) AS TotalSpent
FROM Sales s
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY s.CustomerID;

-- Inventory turnover
SELECT i.ProductID, p.Category, i.StockLevel, SUM(s.Quantity) AS TotalSold,
       SUM(s.Quantity) / i.StockLevel AS TurnoverRate
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Inventory i ON s.ProductID = i.ProductID
GROUP BY i.ProductID;

-- Low stock products
SELECT p.ProductID, p.Category, i.StockLevel, i.RestockDate
FROM Products p
JOIN Inventory i ON p.ProductID = i.ProductID
WHERE i.StockLevel < 20;

-- Profit margin by product
SELECT p.ProductID, p.Category, SUM(s.Quantity * (s.Price - p.UnitCost)) AS TotalProfit,
       SUM(s.Quantity * s.Price) AS TotalRevenue,
       (SUM(s.Quantity * (s.Price - p.UnitCost)) / SUM(s.Quantity * s.Price) * 100) AS ProfitMargin
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
GROUP BY p.ProductID;

-- Category performance
SELECT p.Category, AVG(s.Quantity * s.Price) AS AvgTransaction,
       COUNT(DISTINCT s.CustomerID) AS UniqueCustomers,
       SUM(s.Quantity) AS TotalUnitsSold
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
GROUP BY p.Category;

-- Customer retention by region
SELECT c.Region, COUNT(DISTINCT s.CustomerID) AS ActiveCustomers,
       (SELECT COUNT(DISTINCT CustomerID) FROM Sales) AS TotalCustomers,
       (COUNT(DISTINCT s.CustomerID) * 100.0 / (SELECT COUNT(DISTINCT CustomerID) FROM Sales)) AS RetentionRate
FROM Sales s
JOIN Customers c ON s.CustomerID = c.CustomerID
GROUP BY c.Region;

-- Top products by revenue
SELECT p.ProductID, p.Category, SUM(s.Quantity * s.Price) AS TotalRevenue,
       SUM(s.Quantity) AS TotalQuantity
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
GROUP BY p.ProductID
ORDER BY TotalRevenue DESC
LIMIT 10;