import csv

csv.register_dialect('otg', 'excel', delimiter=';', doublequote=False )

bahnhof_map = {}
bahnsteig_map = {}

with open('data/bahnhof.csv', 'r') as file:
    reader = csv.DictReader(file, dialect='otg')
    for line in reader:
        bahnhof_map[line['name']] = line['plz']
        bahnsteig_map[line['name']] = line['bahnsteig']

with open('sql/V3.2__insert_bahnhof.sql', 'w') as file:
    for key, value in bahnhof_map.items():
        file.write(f"INSERT INTO DBUSER.BAHNHOF(NAME, ORT_PLZ) VALUES('{key}','{value}');\n")

with open('sql/V3.3__insert_bahnsteige.sql', 'w') as file:
    for key, value in bahnsteig_map.items():
        for i in range(1, int(value) + 1):
            file.write(f"INSERT INTO DBUSER.BAHNSTEIG(NR, BAHNHOF_NAME) VALUES({i}, '{key}');\n")
