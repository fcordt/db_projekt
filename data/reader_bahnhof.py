import csv

csv.register_dialect('otg', 'excel', delimiter=';', doublequote=False )

with open('data/bahnhof.csv', 'r') as file:
    reader = csv.DictReader(file, dialect='otg')
    bahnhof_map = {}
    for line in reader:
        bahnhof_map[line['name']] = line['plz']

with open('sql/V3.2__insert_bahnhof.sql', 'w') as file:
    for key, value in bahnhof_map.items():
        file.write(f"INSERT INTO DBUSER.BAHNHOF(NAME, ORT_PLZ) VALUES('{key}','{value}');\n")
