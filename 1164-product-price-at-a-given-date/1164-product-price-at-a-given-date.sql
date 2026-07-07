# Write your MySQL query statement below
SELECT
    p.product_id,
    COALESCE(t.new_price, 10) AS price
FROM
    (SELECT DISTINCT product_id FROM Products) p
LEFT JOIN
(
    SELECT p1.product_id, p1.new_price
    FROM Products p1
    JOIN
    (
        SELECT product_id, MAX(change_date) AS change_date
        FROM Products
        WHERE change_date <= '2019-08-16'
        GROUP BY product_id
    ) p2
    ON p1.product_id = p2.product_id
    AND p1.change_date = p2.change_date
) t
ON p.product_id = t.product_id;