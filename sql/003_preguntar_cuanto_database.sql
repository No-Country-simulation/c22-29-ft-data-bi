SELECT table_schema AS "Base de Datos",
       SUM(data_length + index_length) / 1024 / 1024 AS "Tamaño (MB)"
FROM information_schema.tables
WHERE table_schema = "bottleflow"
GROUP BY table_schema;

