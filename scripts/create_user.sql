CREATE USER &1 IDENTIFIED BY &2;
GRANT ALL PRIVILEGES TO &1;
GRANT UNLIMITED TABLESPACE TO &1;
ALTER USER &1 ACCOUNT UNLOCK;
ALTER USER &1 IDENTIFIED BY &2;
EXIT;