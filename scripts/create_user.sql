CREATE USER &1 IDENTIFIED BY &2;
GRANT CREATE SESSION TO &1;
GRANT CREATE TABLE TO &1;
GRANT UNLIMITED TABLESPACE TO &1;
EXIT;