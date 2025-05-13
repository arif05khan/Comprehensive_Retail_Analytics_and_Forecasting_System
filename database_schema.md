# Database Schema

This document describes the database schema for the Comprehensive Retail Analytics System.

## Tables

### Sales
- `OrderID`: Integer (Primary Key)
- `CustomerID`: Integer
- `ProductID`: Integer
- `Date`: Text
- `Quantity`: Integer
- `Price`: Real

### Customers
- `CustomerID`: Integer (Primary Key)
- `Age`: Integer
- `Gender`: Text
- `Region`: Text

### Products
- `ProductID`: Integer (Primary Key)
- `Category`: Text
- `UnitCost`: Real

### Inventory
- `ProductID`: Integer (Primary Key)
- `StockLevel`: Integer
- `RestockDate`: Text