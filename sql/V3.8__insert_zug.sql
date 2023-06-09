INSERT INTO ZUG(ZUGTYP_ID, NAME, ZUGNUMMER) VALUES('S', 'S3', 25769);

INSERT INTO LOKOMOTIVENTYP(SERIENBEZEICHNUNG, NAME) VALUES('ÖBB 4024', 'Bombardier Talent');

INSERT INTO LOKOMOTIVE(LOKOMOTIVENTYP_SERIENBEZEICHNUNG, ZUG_ZUGNUMMER) VALUES('ÖBB 4024', 25769);

INSERT INTO WAGONTYP(BEZEICHNUNG) VALUES('Bombardier Talent');

INSERT INTO WAGON(REIHENFOLGE, WAGONTYP_BEZEICHNUNG, KLASSE_ID, ZUG_ZUGNUMMER)
VALUES(1, 'Bombardier Talent', 2, 25769);

INSERT INTO SITZPLATZ(SITZPLATZNUMMER, WAGON_ZUGNUMMER, WAGON_REIHENFOLGE)
SELECT LEVEL, 25769, 1 FROM DUAL CONNECT BY LEVEL <= 50;

INSERT INTO WAGON(REIHENFOLGE, WAGONTYP_BEZEICHNUNG, KLASSE_ID, ZUG_ZUGNUMMER)
VALUES(2, 'Bombardier Talent', 2, 25769);

INSERT INTO SITZPLATZ(SITZPLATZNUMMER, WAGON_ZUGNUMMER, WAGON_REIHENFOLGE)
SELECT LEVEL, 25769, 2 FROM DUAL CONNECT BY LEVEL <= 60;

INSERT INTO WAGON(REIHENFOLGE, WAGONTYP_BEZEICHNUNG, KLASSE_ID, ZUG_ZUGNUMMER)
VALUES(3, 'Bombardier Talent', 2, 25769);

INSERT INTO SITZPLATZ(SITZPLATZNUMMER, WAGON_ZUGNUMMER, WAGON_REIHENFOLGE)
SELECT LEVEL, 25769, 3 FROM DUAL CONNECT BY LEVEL <= 50;
