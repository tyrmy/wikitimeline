CREATE TABLE people (
	id integer PRIMARY KEY,
	fname text NOT NULL,
	lname text NOT NULL,
	bday text DEFAULT NULL,
	dday text DEFAULT NULL,
	source text DEFAULT NULL,
	logged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO people (fname, lname, bday) values ('Donald','Trump','1946-06-14');
INSERT INTO people (fname, lname, bday) values ('Bill','Gates','1955-10-28');
INSERT INTO people (fname, lname, bday) values ('Jennifer','Lopez','1969-07-24');
INSERT INTO people (fname, lname, bday) values ('Ozzy', 'Osbourne','1948-12-03');
INSERT INTO people (fname, lname, bday) values ('Billie','Eilish','2001-12-18');
