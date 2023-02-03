#lab3 queries
#1
select * from Video_Recordings, Video_Categories;
#330 rows

#2
select * from Video_Recordings vr, Video_Categories vc where vr.category=vc.name;
# 55 rows

#3
select vr.category, count(vr.title) from Video_Recordings vr group by vr.category;
/* 
category	count(vr.title)
Action & Adventure	10
Comedy	10
Drama	10
Horror	8
Science Fiction	9
Suspense	8
*/

#4
select vr.category, count(vr.title) from Video_Recordings vr  
where vr.stock_count>0 group by vr.category;


select count(vr.title) from Video_Recordings vr  
where vr.stock_count=0 ;


/*
category	count(vr.title)
Action & Adventure	8
Comedy	8
Drama	9
Horror	6
Science Fiction	8
Suspense	6
*/

#5
select va.name, group_concat(vr.category) from Video_Recordings vr, Video_Actors va  
where va.recording_id=vr.recording_id group by va.name;

select count(distinct video_actors.name) from video_actors;
#335 results
#notice WIll Smoth has action adventure listed twice though

select va.name, group_concat(distinct vr.category) from Video_Recordings vr, Video_Actors va  
where va.recording_id=vr.recording_id group by va.name;

#We may have also wanted something like 
select  vr.category, group_concat(va.name)  from Video_Recordings vr, Video_Actors va  
where va.recording_id=vr.recording_id group by vr.category;
# there are 6 results

#6
select va.name, group_concat(vr.category) from Video_Recordings vr, Video_Actors va  
where (select count(r.category) from Video_Recordings r, Video_Actors a where a.recording_id=r.recording_id and a.name=va.name 
group by va.name)>1
and va.recording_id=vr.recording_id group by va.name;
#but this will show actors that have been in two movies in the same cateogry
select va.name, group_concat(distinct vr.category) from Video_Recordings vr, Video_Actors va  
where (select count(distinct r.category) from Video_Recordings r, Video_Actors a where a.recording_id=r.recording_id and a.name=va.name group by va.name)>1
and va.recording_id=vr.recording_id group by va.name;
#25 results

#7
select va.name, group_concat(vr.category) from Video_Recordings vr, Video_Actors va  
where '"Comedy"' not in 
	(select distinct r.category from Video_Recordings r, Video_Actors a 
	where a.recording_id=r.recording_id and a.name=va.name)
and va.recording_id=vr.recording_id group by va.name;
#265 results

#8
select va.name, group_concat(vr.category) from Video_Recordings vr, Video_Actors va  
where '"Comedy"' in 
	(select distinct r.category from Video_Recordings r, Video_Actors a 
    where a.recording_id=r.recording_id and a.name=va.name)
and '"Action & Adventure"' in 
	(select distinct r.category from Video_Recordings r, Video_Actors a 
    where a.recording_id=r.recording_id and a.name=va.name)
and va.recording_id=vr.recording_id group by va.name;
#there are 4 results
/*name	group_concat(vr.category)
Harvey Fierstein	Comedy,Action & Adventure
Jerry Jones	Action & Adventure,Comedy
Lady Reed	Comedy,Action & Adventure
Rudy Ray Moore	Comedy,Action & Adventure
*/

#query to load a new recordings table where, director, rating, category (and also actor, and actor_recording) are seperate tables. 

INSERT INTO recording (recordingId, categoryId, image_name, ratingId, year_released, price, stock_price, directorId, title)
SELECT vvr.id, 
	c.categoryId, 
	vvr.image_name, 
	r.ratingId, 
    vvr.year_released, 
    vvr.price, 
    vvr.stock_count, 
    d.directorId, 
    vvr.title
FROM videos.video_recordings vvr, videos.rating r, videos.category c,  videos.director d 
where  r.ratingName = vvr.rating
and  c.categoryName = vvr.category
and d.directorName = vvr.director;

#or

INSERT INTO videos.recording (recordingId, categoryId, image_name, ratingId, year_released, price, stock_price, directorId, title)
SELECT vvr.id, 
	c.categoryId, 
	vvr.image_name, 
	r.ratingId, 
    vvr.year_released, 
    vvr.price, 
    vvr.stock_count, 
    d.directorId, 
    vvr.title
FROM videos.video_recordings vvr
INNER JOIN videos.rating r on r.ratingName = vvr.rating
INNER JOIN videos.category c ON c.categoryName = vvr.category
INNER JOIN videos.director d on d.directorName = vvr.director;