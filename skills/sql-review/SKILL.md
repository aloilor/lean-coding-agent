---
name: sql-review
description: 'Review SQL queries, schemas, migrations, and database access code for security, correctness, performance optimization, and maintainability across PostgreSQL, MySQL, SQL Server, and Oracle.'
---

# sql-review

Review ${selection} (or the entire project if no selection) for security, performance, maintainability, and database best practices.

## 🔒 Security Analysis

### SQL Injection Prevention

Bind application input through the database driver; placeholder syntax varies by database.

```sql
-- ❌ CRITICAL: SQL Injection vulnerability
query = "SELECT * FROM users WHERE id = " + userInput;
query = f"DELETE FROM orders WHERE user_id = {user_id}";

-- ✅ SECURE: Parameterized queries
-- MySQL
PREPARE stmt FROM 'SELECT id, name FROM users WHERE id = ?';
EXECUTE stmt USING @user_id;

-- PostgreSQL
PREPARE find_user(integer) AS SELECT id, name FROM users WHERE id = $1;
EXECUTE find_user(42);

-- SQL Server
EXEC sp_executesql N'SELECT id, name FROM users WHERE id = @id', N'@id INT', @id = @user_id;
```

### Access Control & Permissions
- **Principle of Least Privilege**: Grant minimum required permissions
- **Role-Based Access**: Use database roles instead of direct user permissions
- **Schema Security**: Proper schema ownership and access controls
- **Function/Procedure Security**: Review DEFINER vs INVOKER rights

### Data Protection
- **Sensitive Data Exposure**: Avoid SELECT * on tables with sensitive columns
- **Audit Logging**: Ensure sensitive operations are logged
- **Data Masking**: Use views or functions to mask sensitive data
- **Encryption**: Verify encrypted storage for sensitive data

## ⚡ Performance and Query Design

### Query structure and joins

#### Query structure

```sql
-- ❌ BAD: Inefficient query patterns
SELECT DISTINCT u.id, u.name, u.email
FROM users u, orders o, products p
WHERE u.id = o.user_id
AND o.product_id = p.id
AND YEAR(o.order_date) = 2024;

-- ✅ GOOD: Optimized structure
SELECT u.id, u.name, u.email
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    INNER JOIN products p ON p.id = o.product_id
    WHERE o.user_id = u.id
      AND o.order_date >= '2024-01-01'
      AND o.order_date < '2025-01-01'
);
```

- **Join Types**: Verify appropriate join types (INNER vs LEFT vs EXISTS)
- **Join Order**: Inspect the execution plan for inefficient join choices
- **Cartesian Products**: Identify and fix missing join conditions

#### N+1 queries

```sql
-- ❌ BAD: N+1 queries in application code
for user in users:
    orders = query("SELECT id, user_id, total_amount FROM orders WHERE user_id = ?", user.id)

-- ✅ GOOD: Single optimized query
SELECT u.id AS user_id, u.name, o.id AS order_id, o.total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

#### DISTINCT masking joins

```sql
-- ❌ BAD: DISTINCT masking join issues
SELECT DISTINCT u.id, u.name
FROM users u
INNER JOIN orders o ON o.user_id = u.id;

-- ✅ GOOD: Proper join without DISTINCT
SELECT u.id, u.name
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
);
```

#### OR and UNION

For disjoint branches, compare `UNION ALL` when the `OR` plan is slow; neither form is always faster.

```sql
-- ❌ BAD: OR query when its plan scans more data than needed
SELECT id, category, price FROM products
WHERE (category = 'electronics' AND price < 1000)
   OR (category = 'books' AND price < 50);

-- ✅ GOOD: UNION ALL alternative when the branches are disjoint and its plan improves
SELECT id, category, price FROM products WHERE category = 'electronics' AND price < 1000
UNION ALL
SELECT id, category, price FROM products WHERE category = 'books' AND price < 50;
```

### Aggregation and subqueries

#### Correlated counts

```sql
-- ❌ BAD: Inefficient aggregation
SELECT user_id,
       (SELECT COUNT(*) FROM orders o2 WHERE o2.user_id = o1.user_id) as order_count
FROM orders o1
GROUP BY user_id;

-- ✅ GOOD: Efficient aggregation
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id;
```

#### Correlated averages

```sql
-- ❌ BAD: Correlated subquery
SELECT p.product_name, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(price)
    FROM products p2
    WHERE p2.category_id = p.category_id
);

-- ✅ GOOD: Set-based window alternative; compare plans for the target database
SELECT product_name, price
FROM (
    SELECT product_name, price,
           AVG(price) OVER (PARTITION BY category_id) as avg_category_price
    FROM products
    WHERE category_id IS NOT NULL
) ranked
WHERE price > avg_category_price;
```

#### Conditional aggregation

```sql
-- ❌ BAD: Multiple separate aggregation queries
SELECT COUNT(*) FROM orders WHERE status = 'pending';
SELECT COUNT(*) FROM orders WHERE status = 'shipped';
SELECT COUNT(*) FROM orders WHERE status = 'delivered';

-- ✅ GOOD: Single query with conditional aggregation
SELECT
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'shipped' THEN 1 END) as shipped_count,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count
FROM orders;
```

### Indexes

- **Missing Indexes**: Identify columns that need indexing
- **Over-Indexing**: Find unused or redundant indexes
- **Composite Indexes**: Multi-column indexes for complex queries
- **Index Maintenance**: Check for fragmented or outdated indexes

#### Composite indexes

For a query filtering by `customer_id` and a `created_at` range:

```sql
-- ❌ BAD: Leading column is unrelated to the query filter
CREATE INDEX idx_orders_status_customer_created
ON orders(status, customer_id, created_at);

-- ✅ GOOD: Key order matches the query predicates
CREATE INDEX idx_orders_customer_created
ON orders(customer_id, created_at);
```

#### Covering indexes

This SQL Server example is an alternative to the preceding index when these extra columns must be covered.

```sql
-- ✅ GOOD: SQL Server covering index for this query pattern
CREATE INDEX idx_orders_covering
ON orders(customer_id, created_at)
INCLUDE (total_amount, status);  -- SQL Server syntax
```

#### Partial indexes

```sql
-- ✅ GOOD: PostgreSQL partial index for a frequently queried subset
CREATE INDEX idx_orders_active
ON orders(created_at)
WHERE status IN ('pending', 'processing');
```

### Pagination

```sql
-- ❌ BAD: Large OFFSET requires skipping rows
SELECT id, name, created_at FROM products
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 10000;

-- ✅ GOOD: Cursor-based pagination with a unique tie-breaker
SELECT id, name, created_at FROM products
WHERE created_at < '2024-06-15 10:30:00'
   OR (created_at = '2024-06-15 10:30:00' AND id < 1000)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Or using ID-based cursor
SELECT id, name FROM products
WHERE id > 1000
ORDER BY id
LIMIT 20;
```

### Batch operations

```sql
-- ❌ BAD: Row-by-row operations
INSERT INTO products (name, price) VALUES ('Product 1', 10.00);
INSERT INTO products (name, price) VALUES ('Product 2', 15.00);
INSERT INTO products (name, price) VALUES ('Product 3', 20.00);

-- ✅ GOOD: Batch insert
INSERT INTO products (name, price) VALUES
('Product 1', 10.00),
('Product 2', 15.00),
('Product 3', 20.00);
```

### Temporary tables

```sql
-- ✅ GOOD: MySQL/PostgreSQL temporary table for reused calculations
CREATE TEMPORARY TABLE temp_calculations AS
SELECT customer_id,
       SUM(total_amount) as total_spent,
       COUNT(*) as order_count
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY customer_id;

-- Use the temp table for further calculations
SELECT c.name, tc.total_spent, tc.order_count
FROM temp_calculations tc
JOIN customers c ON tc.customer_id = c.id
WHERE tc.total_spent > 1000;
```

### Monitoring

```sql
-- For MySQL:
SELECT query_time, lock_time, rows_sent, rows_examined, sql_text
FROM mysql.slow_log
ORDER BY query_time DESC;

-- For PostgreSQL when pg_stat_statements is enabled:
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC;

-- For SQL Server:
SELECT
    qs.total_elapsed_time/qs.execution_count as avg_elapsed_time,
    qs.execution_count,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
        ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) as query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;
```

## 🛠️ Code Quality & Maintainability

### SQL Style & Formatting
```sql
-- ❌ BAD: Poor formatting and style
select u.id,u.name,o.total from users u left join orders o on u.id=o.user_id where u.status='active' and o.order_date>='2024-01-01';

-- ✅ GOOD: Clean, readable formatting
SELECT u.id,
       u.name,
       o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
  AND o.order_date >= '2024-01-01';
```

### Naming Conventions
- **Consistent Naming**: Tables, columns, constraints follow consistent patterns
- **Descriptive Names**: Clear, meaningful names for database objects
- **Reserved Words**: Avoid using database reserved words as identifiers
- **Case Sensitivity**: Consistent case usage across schema
- **Comments**: Explain complex logic where its purpose is not apparent
- **Error Handling**: Check failures in routines and calling code

### Schema Design Review
- **Normalization**: Appropriate normalization level (avoid over/under-normalization)
- **Data Types**: Optimal data type choices for storage and performance
- **Constraints**: Proper use of PRIMARY KEY, FOREIGN KEY, CHECK, NOT NULL
- **Default Values**: Appropriate default values for columns

## 🗄️ Database-Specific Best Practices

### PostgreSQL
```sql
-- Use JSONB for JSON data
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- GIN index for JSONB queries
CREATE INDEX idx_events_data ON events USING gin(data);

-- Array types for multi-value columns
CREATE TABLE tags (
    post_id INT,
    tag_names TEXT[]
);
```

### MySQL
```sql
-- Use appropriate storage engines
CREATE TABLE sessions (
    id VARCHAR(128) PRIMARY KEY,
    data TEXT,
    expires TIMESTAMP
) ENGINE=InnoDB;

-- Optimize for InnoDB
ALTER TABLE large_table
ADD INDEX idx_covering (status, created_at, id);
```

### SQL Server
```sql
-- Use appropriate data types
CREATE TABLE products (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE()
);

-- Columnstore indexes for analytics
CREATE COLUMNSTORE INDEX idx_sales_cs ON sales;
```

### Oracle
```sql
-- Use sequences for auto-increment
CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;

CREATE TABLE users (
    id NUMBER DEFAULT user_id_seq.NEXTVAL PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);
```

## 🧪 Data Integrity Checks

```sql
-- Verify referential integrity
SELECT o.user_id
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;

-- Check for data consistency
SELECT COUNT(*) as inconsistent_records
FROM products
WHERE price < 0 OR stock_quantity < 0;
```
