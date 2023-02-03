mysql.exe -uroot -p
thisis4DB!01

CREATE SCHEMA minilab4;
USE minilab4;

//-- set autocommit to 1
SET autocommit=1;
SELECT @@autocommit;

CREATE TABLE test(num INTEGER NOT NULL) engine=InnoDB;

//--insert 3 rows into table (values auto committed)
INSERT INTO test VALUES (1), (2), (3);
SELECT * FROM test;

//-- set autocommit = 0
SET autocommit=0;
INSERT INTO test VALUES (4), (5);
SELECT * FROM test;

//-- rollback inserts to original state
ROLLBACK;
SELECT * FROM test;

//-- insert and commit (manually)
INSERT INTO test VALUES (4), (5);
COMMIT;
ROLLBACK;
SELECT * FROM test;

//-- truncate the data in the table
TRUNCATE test;
SELECT * FROM test;

//-- start a transaction (manually)
START TRANSACTION;
INSERT INTO test VALUES (1), (2);
INSERT INTO test VALUES (3), (4);
SELECT * FROM test;

//-- from original connection, commit
COMMIT;

//-- start new transaction
START TRANSACTION;
INSERT INTO test VALUES (5), (6);
INSERT INTO test VALUES (7), (8);
ROLLBACK;
SELECT * FROM test;


START TRANSACTION;
SELECT * FROM test;
INSERT INTO test VALUES (0), (0);


Assume you have the following:
- A table, test, that contains a single column, num, with 4 records
- The values of the num column are: 1, 2, 3, 4

CREATE TABLE test(num INTEGER NOT NULL) engine=InnoDB;
INSERT INTO test VALUES (5), (5);

User A and User B are both connected to the same database and trying to run the below queries.

User A: 
START TRANSACTION;
INSERT INTO test VALUES (0), (0);
ROLLBACK;
INSERT INTO test VALUES (8), (8);
COMMIT;

User B:
START TRANSACTION;
INSERT INTO test VALUES (1), (1);
COMMIT;

User C:
SELECT * FROM test;


What will be the results of User C query if User B commits before User A?
1,2,3,4,1,1,8,8

What will be the results of User C query if User A commits before User B?
1,2,3,4,8,8,1,1

Assume User A has commited their query. What will be the results of User C query if 
User C runs the query before the COMMIT clause in User Bs query?
1,2,3,4,8,8
