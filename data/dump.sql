PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE people (
	id integer PRIMARY KEY,
	fname text NOT NULL,
	lname text NOT NULL,
	bday text DEFAULT '1971-01-01',
	dday text DEFAULT NULL,
	source text DEFAULT NULL,
	logged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO "people" VALUES(1,'Lassi','Lehtinen','1995-03-01',NULL,NULL,'2020-05-05 13:12:15');
INSERT INTO "people" VALUES(2,'Matilda','Lintunen','1993-04-23',NULL,NULL,'2020-05-05 13:12:15');
INSERT INTO "people" VALUES(3,'Tarja','Halonen','1943-12-24','None','https://fi.wikipedia.org/wiki/Tarja_Halonen','2020-05-05 13:12:32');
INSERT INTO "people" VALUES(4,'Ben','Stiller','1965-11-30','None','https://fi.wikipedia.org/wiki/Ben_Stiller','2020-05-05 13:12:47');
INSERT INTO "people" VALUES(5,'Richard','Wagner','1813-05-22','1883-02-13','https://fi.wikipedia.org/wiki/Richard_Wagner','2020-05-05 13:13:11');
INSERT INTO "people" VALUES(6,'Benito','Mussolini','1883-07-29','1945-04-28','https://fi.wikipedia.org/wiki/Benito_Mussolini','2020-05-05 13:13:30');
INSERT INTO "people" VALUES(7,'Pablo','Escobar','1949-12-01','1993-12-02','https://fi.wikipedia.org/wiki/Pablo_Escobar','2020-05-05 13:13:39');
INSERT INTO "people" VALUES(8,'Amy','Winehouse','1983-09-14','2011-07-23','https://fi.wikipedia.org/wiki/Amy_Winehouse','2020-05-05 13:13:45');
INSERT INTO "people" VALUES(9,'Paavo','Lipponen','1941-04-23','None','https://fi.wikipedia.org/wiki/Paavo_Lipponen','2020-05-05 13:14:00');
INSERT INTO "people" VALUES(10,'Justin','Bieber','1994-03-01','None','https://fi.wikipedia.org/wiki/Justin_Bieber','2020-05-05 13:14:09');
INSERT INTO "people" VALUES(11,'Adolf','Hitler','1889-04-20','1945-04-30','https://fi.wikipedia.org/wiki/Adolf_Hitler','2020-05-05 13:14:25');
INSERT INTO "people" VALUES(12,'Alan','Turing','1912-06-23','1954-06-07','https://fi.wikipedia.org/wiki/Alan_Turing','2020-05-05 13:14:44');
INSERT INTO "people" VALUES(13,'John','Kennedy','1917-05-29','1963-11-22','https://fi.wikipedia.org/wiki/John_Kennedy','2020-05-05 13:14:52');
INSERT INTO "people" VALUES(14,'Werner','Heisenberg','1901-12-05','1976-02-01','https://fi.wikipedia.org/wiki/Werner_Heisenberg','2020-05-05 13:15:01');
INSERT INTO "people" VALUES(15,'Ilkka','Kanerva','1948-01-28','None','https://fi.wikipedia.org/wiki/Ilkka_Kanerva','2020-05-05 13:21:44');
INSERT INTO "people" VALUES(16,'Josef','Stalin','1878-12-18','1953-03-05','https://fi.wikipedia.org/wiki/Josef_Stalin','2020-05-05 13:25:00');
INSERT INTO "people" VALUES(17,'Aki','Sirkesalo','1962-07-25','2004-12-26','https://fi.wikipedia.org/wiki/Aki_Sirkesalo','2020-05-05 13:26:55');
INSERT INTO "people" VALUES(18,'Irwin','Goodman','1943-09-14','1991-01-14','https://fi.wikipedia.org/wiki/Irwin_Goodman','2020-05-05 13:27:59');
INSERT INTO "people" VALUES(19,'Vexi','Salmi','1942-09-21','None','https://fi.wikipedia.org/wiki/Vexi_Salmi','2020-05-05 13:28:08');
INSERT INTO "people" VALUES(20,'Virve','Rosti','1958-11-10','None','https://fi.wikipedia.org/wiki/Virve_Rosti','2020-05-05 13:28:21');
COMMIT;
