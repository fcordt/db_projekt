-- Generiert von Oracle SQL Developer Data Modeler 22.2.0.165.1149
--   am/um:        2023-04-21 15:33:27 MESZ
--   Site:      Oracle Database 12cR2
--   Typ:      Oracle Database 12cR2



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE bahnhof (
    name    VARCHAR2(100) NOT NULL,
    adresse VARCHAR2(100) NOT NULL,
    ort_plz VARCHAR2(4) NOT NULL
);

ALTER TABLE bahnhof ADD CONSTRAINT bahnhof_pk PRIMARY KEY ( name );

CREATE TABLE bahnsteig (
    nr           NUMBER(2) NOT NULL,
    bahnhof_name VARCHAR2(100) NOT NULL
);

ALTER TABLE bahnsteig ADD CONSTRAINT bahnsteig_pk PRIMARY KEY ( bahnhof_name,
                                                                nr );

CREATE TABLE dauerticket (
    ticketnummer        NUMBER NOT NULL,
    kundin_kundennummer VARCHAR2(9) NOT NULL,
    dauertyp_id         VARCHAR2(10) NOT NULL
);

ALTER TABLE dauerticket ADD CONSTRAINT dauerticket_pk PRIMARY KEY ( ticketnummer );

CREATE TABLE dauerticketpreis (
    von         DATE NOT NULL,
    bis         DATE NOT NULL,
    kosten      NUMBER(10, 2) NOT NULL,
    dauertyp_id VARCHAR2(10) NOT NULL
);

ALTER TABLE dauerticketpreis ADD CONSTRAINT dauerticketpreis_pk PRIMARY KEY ( dauertyp_id,
                                                                              von );

CREATE TABLE dauertyp (
    id                VARCHAR2(10) NOT NULL,
    lange_bezeichnung VARCHAR2(100) NOT NULL
);

ALTER TABLE dauertyp ADD CONSTRAINT dauertyp_pk PRIMARY KEY ( id );

CREATE TABLE einzelticket (
    ticketnummer            NUMBER NOT NULL,
    abfahrt_bahnhof_name    VARCHAR2(100) NOT NULL,
    abfahrt_bahnsteig_nr    NUMBER(2) NOT NULL,
    ankunft_bahnhof_name    VARCHAR2(100) NOT NULL,
    ankunft_bahnsteig_nr    NUMBER(2) NOT NULL
);

ALTER TABLE einzelticket ADD CONSTRAINT einzelticket_pk PRIMARY KEY ( ticketnummer );

CREATE TABLE einzelticket_mit_spr (
    ticketnummer                NUMBER NOT NULL,
    reservierdatum              TIMESTAMP WITH LOCAL TIME ZONE,
    sitzplatz_wagon_zugnummer   NUMBER(10) NOT NULL,
    sitzplatz_wagon_reihenfolge NUMBER(3) NOT NULL,
    sitzplatz_sitzplatznummer   NUMBER(2) NOT NULL
);

ALTER TABLE einzelticket_mit_spr ADD CONSTRAINT einzelticket_mit_spr_pk PRIMARY KEY ( ticketnummer );

CREATE TABLE einzelticketpreis (
    von       DATE NOT NULL,
    bis       DATE NOT NULL,
    kosten    NUMBER(10, 2) NOT NULL,
    zugtyp_id VARCHAR2(20) NOT NULL
);

ALTER TABLE einzelticketpreis ADD CONSTRAINT einzelticketpreis_pk PRIMARY KEY ( zugtyp_id,
                                                                                von );

CREATE TABLE fahrplan (
    nr            NUMBER(10) NOT NULL,
    name          VARCHAR2(100) NOT NULL,
    von_datum     DATE NOT NULL,
    bis_datum     DATE NOT NULL,
    zug_zugnummer NUMBER(10) NOT NULL
);

ALTER TABLE fahrplan ADD CONSTRAINT fahrplan_pk PRIMARY KEY ( nr );

CREATE SEQUENCE fahrplan_seq START WITH 1;

CREATE OR REPLACE TRIGGER fahrplan_insert 
BEFORE INSERT ON fahrplan 
FOR EACH ROW

BEGIN
  SELECT fahrplan_seq.NEXTVAL
  INTO   :new.nr
  FROM   dual;
END;
/


CREATE TABLE klasse (
    id          NUMBER(2) NOT NULL,
    bezeichnung VARCHAR2(50) NOT NULL
);

ALTER TABLE klasse ADD CONSTRAINT klasse_pk PRIMARY KEY ( id );

CREATE TABLE kundin (
    vorname      VARCHAR2(100) NOT NULL,
    nachname     VARCHAR2(100) NOT NULL,
    kundennummer VARCHAR2(9) NOT NULL,
    adresse      VARCHAR2(100) NOT NULL,
    ort_plz      VARCHAR2(4) NOT NULL
);

ALTER TABLE kundin ADD CONSTRAINT kundin_pk PRIMARY KEY ( kundennummer );


CREATE SEQUENCE kundin_seq START WITH 1;

CREATE OR REPLACE TRIGGER kundin_insert 
BEFORE INSERT ON kundin 
FOR EACH ROW

BEGIN
  SELECT LPAD(to_char(kundin_seq.NEXTVAL), 9, '0')
  INTO   :new.kundennummer
  FROM   dual;
END;
/

CREATE TABLE lokomotive ( 
    lokomotiventyp_serienbezeichnung VARCHAR2(100) NOT NULL,
    zug_zugnummer                    NUMBER(10) NOT NULL
);

ALTER TABLE lokomotive ADD CONSTRAINT lokomotive_pk PRIMARY KEY ( zug_zugnummer,
                                                                  lokomotiventyp_serienbezeichnung );

CREATE TABLE lokomotiventyp (
    serienbezeichnung VARCHAR2(100) NOT NULL,
    name              VARCHAR2(100) NOT NULL
);

ALTER TABLE lokomotiventyp ADD CONSTRAINT lokomotiventyp_pk PRIMARY KEY ( serienbezeichnung );

CREATE TABLE ort (
    plz  VARCHAR2(4) NOT NULL,
    name VARCHAR2(100) NOT NULL
);

ALTER TABLE ort ADD CONSTRAINT ort_pk PRIMARY KEY ( plz );

CREATE TABLE preis_je_haltestelle (
    von    DATE NOT NULL,
    bis    DATE NOT NULL,
    kosten NUMBER(10, 2) NOT NULL
);

ALTER TABLE preis_je_haltestelle ADD CONSTRAINT preis_je_haltestelle_pk PRIMARY KEY ( von );

CREATE TABLE reservierungsaufschlag (
    von                  DATE NOT NULL,
    bis                  DATE NOT NULL,
    kosten               NUMBER(10, 2) NOT NULL,
    wagontyp_bezeichnung VARCHAR2(50) NOT NULL
);

ALTER TABLE reservierungsaufschlag ADD CONSTRAINT reservierungsaufschlag_pk PRIMARY KEY ( von,
                                                                                          wagontyp_bezeichnung );

CREATE TABLE sitzplatz (
    sitzplatznummer   NUMBER(2) NOT NULL,
    wagon_zugnummer   NUMBER(10) NOT NULL,
    wagon_reihenfolge NUMBER(3) NOT NULL
);

ALTER TABLE sitzplatz
    ADD CONSTRAINT sitzplatz_pk PRIMARY KEY ( wagon_zugnummer,
                                              wagon_reihenfolge,
                                              sitzplatznummer );

CREATE TABLE streckenabschnitt (
    id                      NUMBER NOT NULL,
    abfahrtszeit            TIMESTAMP WITH LOCAL TIME ZONE NOT NULL,
    ankunftszeit            TIMESTAMP WITH LOCAL TIME ZONE NOT NULL,
    fahrplan_nr             NUMBER(10) NOT NULL,
    abfahrt_bahnsteig_nr    NUMBER(2) NOT NULL,
    ankunft_bahnsteig_nr    NUMBER(2) NOT NULL,
    abfahrt_bahnhof_name    VARCHAR2(100) NOT NULL,
    ankunft_bahnhof_name    VARCHAR2(100) NOT NULL
);

ALTER TABLE streckenabschnitt ADD CONSTRAINT streckenabschnitt_pk PRIMARY KEY ( id );

CREATE SEQUENCE streckenabschnitt_seq START WITH 1;

CREATE OR REPLACE TRIGGER streckenabschnitt_insert 
BEFORE INSERT ON streckenabschnitt 
FOR EACH ROW

BEGIN
  SELECT streckenabschnitt_seq.NEXTVAL
  INTO   :new.id
  FROM   dual;
END;
/

CREATE TABLE ticket (
    ticketnummer     NUMBER NOT NULL,
    gültigkeitsdatum DATE NOT NULL,
    ticket_typ       VARCHAR2(20) NOT NULL
);

ALTER TABLE ticket
    ADD CONSTRAINT ch_inh_ticket CHECK ( ticket_typ IN ( 'DAUERTICKET', 'EINZELTICKET', 'EINZELTICKET_MIT_SPR', 'TICKET' ) );

ALTER TABLE ticket ADD CONSTRAINT ticket_pk PRIMARY KEY ( ticketnummer );

CREATE SEQUENCE ticket_seq START WITH 1;

CREATE OR REPLACE TRIGGER ticket_insert 
BEFORE INSERT ON ticket 
FOR EACH ROW

BEGIN
  SELECT ticket_seq.NEXTVAL
  INTO   :new.ticketnummer
  FROM   dual;
END;
/

CREATE TABLE wagon (
    reihenfolge          NUMBER(3) NOT NULL,
    wagontyp_bezeichnung VARCHAR2(50) NOT NULL,
    klasse_id            NUMBER(2) NOT NULL,
    zug_zugnummer        NUMBER(10) NOT NULL
);

ALTER TABLE wagon ADD CONSTRAINT wagon_pk PRIMARY KEY ( zug_zugnummer,
                                                        reihenfolge );

CREATE TABLE wagontyp (
    bezeichnung VARCHAR2(50) NOT NULL
);

ALTER TABLE wagontyp ADD CONSTRAINT wagontyp_pk PRIMARY KEY ( bezeichnung );

CREATE TABLE zug (
    zugnummer NUMBER(10) NOT NULL,
    name      VARCHAR2(100) NOT NULL,
    zugtyp_id VARCHAR2(20) NOT NULL
);

ALTER TABLE zug ADD CONSTRAINT zug_pk PRIMARY KEY ( zugnummer );

CREATE TABLE zugtyp (
    id   VARCHAR2(20) NOT NULL,
    name VARCHAR2(100) NOT NULL
);

ALTER TABLE zugtyp ADD CONSTRAINT zugtyp_pk PRIMARY KEY ( id );

ALTER TABLE bahnhof
    ADD CONSTRAINT bahnhof_ort_fk FOREIGN KEY ( ort_plz )
        REFERENCES ort ( plz );

ALTER TABLE bahnsteig
    ADD CONSTRAINT bahnsteig_bahnhof_fk FOREIGN KEY ( bahnhof_name )
        REFERENCES bahnhof ( name );

ALTER TABLE dauerticket
    ADD CONSTRAINT dauerticket_dauertyp_fk FOREIGN KEY ( dauertyp_id )
        REFERENCES dauertyp ( id );

ALTER TABLE dauerticket
    ADD CONSTRAINT dauerticket_kundin_fk FOREIGN KEY ( kundin_kundennummer )
        REFERENCES kundin ( kundennummer );

ALTER TABLE dauerticket
    ADD CONSTRAINT dauerticket_ticket_fk FOREIGN KEY ( ticketnummer )
        REFERENCES ticket ( ticketnummer );

ALTER TABLE dauerticketpreis
    ADD CONSTRAINT dauerticketpreis_dauertyp_fk FOREIGN KEY ( dauertyp_id )
        REFERENCES dauertyp ( id );

ALTER TABLE einzelticket
    ADD CONSTRAINT einzelticket_abfahrt_bahnsteig_fk FOREIGN KEY ( abfahrt_bahnhof_name,
                                                           abfahrt_bahnsteig_nr )
        REFERENCES bahnsteig ( bahnhof_name,
                               nr );


ALTER TABLE einzelticket
    ADD CONSTRAINT einzelticket_ankunft_bahnsteig_fk FOREIGN KEY ( ankunft_bahnhof_name,
                                                             ankunft_bahnsteig_nr )
        REFERENCES bahnsteig ( bahnhof_name,
                               nr );

ALTER TABLE einzelticket_mit_spr
    ADD CONSTRAINT einzelticket_mit_spr_einzelticket_fk FOREIGN KEY ( ticketnummer )
        REFERENCES einzelticket ( ticketnummer );

ALTER TABLE einzelticket_mit_spr
    ADD CONSTRAINT einzelticket_mit_spr_sitzplatz_fk FOREIGN KEY ( sitzplatz_wagon_zugnummer,
                                                                   sitzplatz_wagon_reihenfolge,
                                                                   sitzplatz_sitzplatznummer )
        REFERENCES sitzplatz ( wagon_zugnummer,
                               wagon_reihenfolge,
                               sitzplatznummer );

ALTER TABLE einzelticket
    ADD CONSTRAINT einzelticket_ticket_fk FOREIGN KEY ( ticketnummer )
        REFERENCES ticket ( ticketnummer );

ALTER TABLE einzelticketpreis
    ADD CONSTRAINT einzelticketpreis_zugtyp_fk FOREIGN KEY ( zugtyp_id )
        REFERENCES zugtyp ( id );

ALTER TABLE fahrplan
    ADD CONSTRAINT fahrplan_zug_fk FOREIGN KEY ( zug_zugnummer )
        REFERENCES zug ( zugnummer );

ALTER TABLE kundin
    ADD CONSTRAINT kundin_ort_fk FOREIGN KEY ( ort_plz )
        REFERENCES ort ( plz );

ALTER TABLE lokomotive
    ADD CONSTRAINT lokomotive_lokomotiventyp_fk FOREIGN KEY ( lokomotiventyp_serienbezeichnung )
        REFERENCES lokomotiventyp ( serienbezeichnung );

ALTER TABLE lokomotive
    ADD CONSTRAINT lokomotive_zug_fk FOREIGN KEY ( zug_zugnummer )
        REFERENCES zug ( zugnummer );

ALTER TABLE reservierungsaufschlag
    ADD CONSTRAINT reservierungsaufschlag_wagontyp_fk FOREIGN KEY ( wagontyp_bezeichnung )
        REFERENCES wagontyp ( bezeichnung );

ALTER TABLE sitzplatz
    ADD CONSTRAINT sitzplatz_wagon_fk FOREIGN KEY ( wagon_zugnummer,
                                                    wagon_reihenfolge )
        REFERENCES wagon ( zug_zugnummer,
                           reihenfolge );

ALTER TABLE streckenabschnitt
    ADD CONSTRAINT streckenabschnitt_abfahrt_bahnsteig_fk FOREIGN KEY ( abfahrt_bahnhof_name,
                                                                abfahrt_bahnsteig_nr )
        REFERENCES bahnsteig ( bahnhof_name,
                               nr );

ALTER TABLE streckenabschnitt
    ADD CONSTRAINT streckenabschnitt_ankunft_bahnsteig_fk FOREIGN KEY ( ankunft_bahnhof_name,
                                                                  ankunft_bahnsteig_nr )
        REFERENCES bahnsteig ( bahnhof_name,
                               nr );

ALTER TABLE streckenabschnitt
    ADD CONSTRAINT streckenabschnitt_fahrplan_fk FOREIGN KEY ( fahrplan_nr )
        REFERENCES fahrplan ( nr );

ALTER TABLE wagon
    ADD CONSTRAINT wagon_klasse_fk FOREIGN KEY ( klasse_id )
        REFERENCES klasse ( id );

ALTER TABLE wagon
    ADD CONSTRAINT wagon_wagontyp_fk FOREIGN KEY ( wagontyp_bezeichnung )
        REFERENCES wagontyp ( bezeichnung );

ALTER TABLE wagon
    ADD CONSTRAINT wagon_zug_fk FOREIGN KEY ( zug_zugnummer )
        REFERENCES zug ( zugnummer );

ALTER TABLE zug
    ADD CONSTRAINT zug_zugtyp_fk FOREIGN KEY ( zugtyp_id )
        REFERENCES zugtyp ( id );

CREATE OR REPLACE TRIGGER arc_fkarc_1_einzelticket BEFORE
    INSERT OR UPDATE OF ticketnummer ON einzelticket
    FOR EACH ROW
DECLARE
    d VARCHAR2(20);
BEGIN
    SELECT
        a.ticket_typ
    INTO d
    FROM
        ticket a
    WHERE
        a.ticketnummer = :new.ticketnummer;

    IF ( d IS NULL OR d <> 'EINZELTICKET' ) THEN
        raise_application_error(-20223, 'FK Einzelticket_Ticket_FK in Table Einzelticket violates Arc constraint on Table Ticket - discriminator column ticket_typ doesn''t have value ''EINZELTICKET'''
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/

CREATE OR REPLACE TRIGGER arc_fkarc_1_dauerticket BEFORE
    INSERT OR UPDATE OF ticketnummer ON dauerticket
    FOR EACH ROW
DECLARE
    d VARCHAR2(20);
BEGIN
    SELECT
        a.ticket_typ
    INTO d
    FROM
        ticket a
    WHERE
        a.ticketnummer = :new.ticketnummer;

    IF ( d IS NULL OR d <> 'DAUERTICKET' ) THEN
        raise_application_error(-20223, 'FK Dauerticket_Ticket_FK in Table Dauerticket violates Arc constraint on Table Ticket - discriminator column ticket_typ doesn''t have value ''DAUERTICKET'''
        );
    END IF;

EXCEPTION
    WHEN no_data_found THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;
END;
/
