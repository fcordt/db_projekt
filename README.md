# db_projekt

## erforderliche Programme

* Bash
* Docker
* Flyway
* SQLPlus

## Datenbank (neu) erstellen und Daten einfügen

**Achtung**: Falls vorher schon eine Instanz erstellt wurde, wird diese gelöscht und alle Daten gelöscht!

* \> *make recreate_db*
* Warten bis die Oracle Instanz gestartet ist (dauert in der regel ~10 minuten)
* \> *make initialize_db*

## Datenbank stoppen

* \> *make stop_db*

## JDBC Url

> jdbc:oracle:thin:@127.0.0.1:1521/dbuebung

## SYS Username und Passwort

> SYS/test123 [as sysdba]

## Datenbank Projekt Username und Passwort

> dbuser/test