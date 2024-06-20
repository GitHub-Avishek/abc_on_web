-- ---------------------------------------------------------------- #MySQL DB SETUP# ------------------------------------------------------------------

CREATE DATABASE abc_frmwrk_db;

CREATE USER 'app_master'@'%' identified by '@dmin%P$wd'; 
CREATE USER 'app_devlpr'@'%' identified by 'D3v1p%P$wd'; 
CREATE USER 'app_reader'@'%' identified by 'R3adr%P$wd';

GRANT SELECT ON abc_frmwrk_db.* TO 'app_reader'@'%';
GRANT SELECT,INSERT,UPDATE,DELETE,EXECUTE,CREATE TEMPORARY TABLES ON abc_frmwrk_db.* TO 'app_devlpr'@'%';
GRANT ALL ON abc_frmwrk_db.* TO 'app_master'@'%';
