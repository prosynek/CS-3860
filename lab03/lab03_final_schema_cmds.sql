mysql.exe -uroot -p
thisis4DB!01


CREATE TABLE categories
(
  category__id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (category_id)
);

CREATE TABLE actors
(
  actor_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (actor_id)
);

CREATE TABLE directors
(
  director_id INT NOT NULL auto_increment,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (director_id)
);

CREATE TABLE films
(
  film_id INT NOT NULL,
  title VARCHAR(200) NOT NULL,
  image_name VARCHAR(100) NOT NULL,
  rating VARCHAR(10) NOT NULL,
  year_released INT NOT NULL,
  price FLOAT NOT NULL,
  stock_count FLOAT NOT NULL,
  duration FLOAT NOT NULL,
  category_id INT NOT NULL,
  director_id INT NOT NULL,
  PRIMARY KEY (film_id),
  FOREIGN KEY (category__id) REFERENCES categories(category__id),
  FOREIGN KEY (director_id) REFERENCES directors(director_id)
);

CREATE TABLE actor_film
(
  film_id INT NOT NULL,
  actor_id INT NOT NULL,
  FOREIGN KEY (film_id) REFERENCES films(film_id),
  FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
);



//------------------load existing data into new tables-------------------------

                        
ALTER TABLE categories RENAME COLUMN category__id TO category_id;
ALTER TABLE films RENAME COLUMN category__id TO category_id;
ALTER TABLE directors MODIFY director_id INT NOT NULL AUTO_INCREMENT;
SET FOREIGN_KEY_CHECKS=0;
ALTER TABLE directors MODIFY director_id INT NOT NULL AUTO_INCREMENT;
SET FOREIGN_KEY_CHECKS=1;

ALTER TABLE directors
DROP COLUMN director_id;

//-----CATEGORY TABLE-----
INSERT INTO categories (category_id, name)
SELECT id, name FROM video_categories;

//-----ACTORS TABLE-----
INSERT INTO actors (actor_id, name)
SELECT id, name FROM video_actors GROUP BY name;


//-----ACTOR_FILM TABLE-----
INSERT INTO actor_film (film_id, actor_id)
SELECT DISTINCT recording_id, id FROM video_actors;


//-----DIRECTORS TABLE-----
INSERT INTO directors (name)
SELECT director FROM video_recordings
GROUP BY director;

//-----FILMS TABLE-----
INSERT INTO films (film_id, title, image_name, rating, year_released, price, stock_count, duration, category_id, director_id) 
SELECT vr.recording_id, vr.title, vr.image_name, vr.rating, vr.year_released, vr.price, vr.stock_count, vr.duration, c.category_id, d.director_id
FROM video_recordings vr
INNER JOIN directors d
  ON d.name = vr.director
INNER JOIN categories c
  ON c.name = vr.category;


inner join : https://www.sqlshack.com/a-step-by-step-walkthrough-of-sql-inner-join/


//-----PART 3-----
//--3. List the number of videos for each video category.

SELECT c.name, f.category_id, COUNT(f.film_id) AS num_videos
FROM films f, categories c
WHERE c.category_id = f.category_id
GROUP BY f.category_id;

//--4.  List the number of videos for each video category where the inventory is non-zero
SELECT c.name, f.category_id, COUNT(f.film_id) AS num_videos
FROM films f, categories c
WHERE c.category_id = f.category_id AND f.stock_count != 0
GROUP BY f.category_id;

//--5. For each actor, list the video categories that actor has appeared in.

SELECT a.actor_id, a.name, c.name
FROM actors a
INNER JOIN actor_film af
ON a.actor_id = af.actor_id
INNER JOIN films f
ON f.film_id = af.film_id
INNER JOIN categories c
ON f.category_id = c.category_id
WHERE c.category_id = f.category_id;

SELECT a.actor_id, a.name, GROUP_CONCAT(c.name)
FROM actors a 
JOIN actor_film af
ON a.actor_id = af.actor_id
JOIN films f
ON f.film_id = af.film_id
JOIN categories c
ON f.category_id = c.category_id 
WHERE c.category_id = f.category_id
GROUP BY a.actor_id;

SELECT a.actor_id, a.name, c.name
FROM actors a
INNER JOIN actor_film af INNER JOIN films f INNER JOIN categories c
ON a.actor_id = af.actor_id AND f.film_id = af.film_id ON f.category_id = c.category_id
GROUP BY a.name;

SELECT a.name, GROUP_CONCAT(c.name)
FROM actors a, films f, categories c, actor_film af
WHERE af.actor_id = a.actor_id AND af.film_id = f.film_id AND f.category_id = c.category_id
GROUP_BY a.name;

SELECT a.name, GROUP_CONCAT(c.name)
FROM actors a, films f, categories c, actor_film af
WHERE af.actor_id = a.actor_id AND af.film_id = f.film_id AND f.category_id = c.category_id
GROUP BY a.name;

//--6.  Which actors have appeared in movies in different video categories?
SELECT a.name, c.name, COUNT(*)
FROM actors a, films f, categories c, actor_film af
WHERE af.actor_id = a.actor_id AND af.film_id = f.film_id AND f.category_id = c.category_id
GROUP BY a.name;

//--7.  Which actors have not appeared in a comedy?


//--8.  Which actors have appeared in both a comedy and an action adventure movie?










