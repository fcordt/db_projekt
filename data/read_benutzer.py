import csv

csv.register_dialect('otg', 'excel', delimiter=';', doublequote=False )

with open('data/benutzer.csv', 'r') as file:
    reader = csv.DictReader(file, dialect='otg')
    with open('sql/V3.10__insert_benutzer.sql', 'w') as file:
        for line in reader:
            file.write(f"INSERT INTO DBUSER.KUNDIN(VORNAME, NACHNAME, ADRESSE, ORT_PLZ) "
                       f"VALUES('{line['Vorname']}', '{line['Nachname']}', '{line['Adresse']}', '{line['PLZ']}');\n")
