CREATE TABLE people (
	id integer PRIMARY KEY,
	fname text NOT NULL,
	lname text NOT NULL,
	bday text DEFAULT '1971-01-01',
	dday text DEFAULT NULL,
	source text DEFAULT NULL,
	logged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO people (fname, lname, bday) values ('Lassi','Lehtinen','1995-03-01');
INSERT INTO people (fname, lname, bday) values ('Matilda','Lintunen','1993-04-23');
