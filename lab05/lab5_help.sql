#create schema test;
#use test;
drop table one;
create table one (
date varchar(20) unique,
second int, 
third int,

PRIMARY KEY(date)
);

insert into one values ("1-1-22", 1, null);
insert into one values ("1-2-22", 2, null);
insert into one values ("1-3-22", 3, null);
insert into one values ("1-4-22", 4, null);
insert into one values ("1-5-22", 5, null);

    UPDATE
        one p, one m 
	SET
        p.third = p.second+
        (select m.second where m.date="1-1-22") ;

# or select the close value for the first date from the individual stock table
