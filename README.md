# db_projekt

## Datenbank
### erforderliche Programme

* Bash
* Docker
* Flyway
* SQLPlus

### Datenbank (neu) erstellen und Daten einfügen

**Achtung**: Falls vorher schon eine Instanz erstellt wurde, wird diese gelöscht und alle Daten gelöscht!

* \> *make recreate_db*
* Warten bis die Oracle Instanz gestartet ist (dauert in der regel ~10 minuten)
* \> *make initialize_db*

### Datenbank stoppen

* \> *make stop_db*

### JDBC Url

> jdbc:oracle:thin:@127.0.0.1:1521/dbuebung

### SYS Username und Passwort

> SYS/test123 [as sysdba]

### Datenbank Projekt Username und Passwort

> dbuser/test

### Script Files

In den Verzeichnisen ./sql, ./scripts und ./data befinden sich die SQL Scripts, Bash Script und Dateien mit Datensätzen, die von dem *make initialize_db* script benutzt werden, um die Datenbank aufzusetzen und zu füllen.


## Python Webserver

Der source-code des Python-Webservers liegt im Verzeichnis src/python_sw

In diesem Ordner liegt auch ein README.md mit einer kurzen Beschreibung, wie der Webserver zu starten ist.

## Projektdokumentation

Im Verzeichnis src/latex befindet sich der Latex Source und die kompilierte main.pdf

## Data Modeller Files

Im Verzeichnis src/date_modeller
