CREATE TABLE people (
	id integer PRIMARY KEY,
	fname text NOT NULL,
	lname text NOT NULL,
	bday text DEFAULT '01.01.1971',
	dday text
);

INSERT INTO people (fname, lname, bday) values ('Lassi','Lehtinen','15.03.1995');
INSERT INTO people (fname, lname, bday) values ('Matilda','Lintunen','23.04.1993');
