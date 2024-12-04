CREATE VIEW SummaryCounts AS
SELECT 'beg_inv' AS category, (SELECT COUNT(*) FROM beginvfinal12312016) AS count_value
UNION ALL
SELECT 'end_inv', (SELECT COUNT(*) FROM endinvfinal12312016)
UNION ALL
SELECT 'sales', (SELECT COUNT(*) FROM salesfinal12312016)
UNION ALL
SELECT 'purchases', (SELECT COUNT(*) FROM purchasesfinal12312016)
UNION ALL
SELECT 'invoice_purchases', (SELECT COUNT(*) FROM invoicepurchases12312016);

SELECT * FROM SummaryCounts;