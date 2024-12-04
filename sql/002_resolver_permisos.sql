SELECT user, host FROM mysql.user;

SHOW GRANTS FOR 'lucel-pm'@'%';
SHOW GRANTS FOR 'vicen_bot_etl'@'%';
SHOW GRANTS FOR 'robertogial'@'%';

GRANT SELECT ON `bottleflow`.* TO `lucel-pm`@`%`;
GRANT SELECT ON `bottleflow`.* TO `vicen_bot_etl`@`%`;
GRANT SELECT ON `bottleflow`.* TO `robertogial`@`%`;
REVOKE `cloudsqlsuperuser` FROM `lucel-pm`@`%`;
REVOKE `cloudsqlsuperuser` FROM `vicen_bot_etl`@`%`;
REVOKE `cloudsqlsuperuser` FROM `robertogial`@`%`;
REVOKE SELECT ON `mi_base_de_datos`.* FROM `lucel-pm`@`%`;
GRANT INSERT, UPDATE, DELETE ON `bottleflow`.* TO 'lucel-pm'@'%';
GRANT INSERT, UPDATE, DELETE ON `bottleflow`.* TO 'vicen_bot_etl'@'%';
REVOKE INSERT, UPDATE, DELETE ON `bottleflow`.* FROM 'lucel-pm'@'%';

-- Otros usuarios
GRANT CREATE VIEW, SELECT ON bottleflow.* TO 'robertogial'@'%';
-- GRANT CREATE VIEW, SELECT ON bottleflow.* TO 'usuario'@'%';
-- GRANT CREATE VIEW, SELECT ON bottleflow.* TO 'usuario'@'%';
-- GRANT CREATE VIEW, SELECT ON bottleflow.* TO 'usuario'@'%';

-- Del borrado xD
SHOW GRANTS FOR 'root'@'%';
GRANT DROP ON `bottleflow`.* TO `lucel-pm`@`%`;
REVOKE DROP ON `bottleflow`.* FROM `lucel-pm`@`%`;





