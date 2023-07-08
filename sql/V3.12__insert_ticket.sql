--ticketnummer 1
INSERT INTO TICKET(TICKETNUMMER, GÜLTIGKEITSDATUM, TICKET_TYP) 
VALUES (TICKET_SEQ.NEXTVAL, TO_DATE('12122023', 'ddmmyyyy'), 'EINZELTICKET');
--ticketnummer 2
INSERT INTO TICKET(TICKETNUMMER, GÜLTIGKEITSDATUM, TICKET_TYP) 
VALUES (TICKET_SEQ.NEXTVAL, TO_DATE('12122023', 'ddmmyyyy'), 'EINZELTICKET');
--ticketnummer 3
INSERT INTO TICKET(TICKETNUMMER, GÜLTIGKEITSDATUM, TICKET_TYP) 
VALUES (TICKET_SEQ.NEXTVAL, TO_DATE('12122023', 'ddmmyyyy'), 'EINZELTICKET');

INSERT INTO EINZELTICKET(TICKETNUMMER, ABFAHRT_BAHNHOF_NAME, ABFAHRT_BAHNSTEIG_NR, ANKUNFT_BAHNHOF_NAME, ANKUNFT_BAHNSTEIG_NR)
VALUES(1, 'Salzburg Mülln-Altstadt Bahnhof', 1, 'Salzburg Sam Bahnhof', 2);
INSERT INTO EINZELTICKET(TICKETNUMMER, ABFAHRT_BAHNHOF_NAME, ABFAHRT_BAHNSTEIG_NR, ANKUNFT_BAHNHOF_NAME, ANKUNFT_BAHNSTEIG_NR)
VALUES(2, 'Salzburg Hbf', 9, 'Puch b.Hallein Urstein Bahnhof', 2);
INSERT INTO EINZELTICKET(TICKETNUMMER, ABFAHRT_BAHNHOF_NAME, ABFAHRT_BAHNSTEIG_NR, ANKUNFT_BAHNHOF_NAME, ANKUNFT_BAHNSTEIG_NR)
VALUES(3, 'Salzburg Süd Bahnhst', 2, 'Golling-Abtenau Bahnhof', 1);

INSERT INTO EINZELTICKET_MIT_SPR(TICKETNUMMER, RESERVIERDATUM, SITZPLATZ_WAGON_ZUGNUMMER, SITZPLATZ_WAGON_REIHENFOLGE, SITZPLATZ_SITZPLATZNUMMER)
VALUES(1, TO_DATE('31129999', 'ddmmyyyy'), 25769, 1, 23);
INSERT INTO EINZELTICKET_MIT_SPR(TICKETNUMMER, RESERVIERDATUM, SITZPLATZ_WAGON_ZUGNUMMER, SITZPLATZ_WAGON_REIHENFOLGE, SITZPLATZ_SITZPLATZNUMMER)
VALUES(2, TO_DATE('31129999', 'ddmmyyyy'), 25769, 2, 59);
INSERT INTO EINZELTICKET_MIT_SPR(TICKETNUMMER, RESERVIERDATUM, SITZPLATZ_WAGON_ZUGNUMMER, SITZPLATZ_WAGON_REIHENFOLGE, SITZPLATZ_SITZPLATZNUMMER)
VALUES(3, TO_DATE('31129999', 'ddmmyyyy'), 25769, 1, 23);