-- sql to check tne search main files
USE hbnb_dev_db;

-- main 0
SELECT count(*) as all_places
FROM places;

-- main 1
SELECT count(*) as many_cities
FROM places
WHERE places.city_id in (
      SELECT cities.id
      FROM cities
      WHERE cities.name in ("Urbana", "Chicago", "Peoria", "Naperville", "San Francisco", "Fremont", "San Jose", "Sonoma", "New Orleans", "Baton Rouge", "Meridian", "Miami", "Tempe", "Calera", "Akron", "Portland"));

-- main 2


-- main 3 as 2_amenities
select count(*) as one_amenity
from place_amenity
where amenity_id in
      (select id from amenities where name = "Wireless Internet");


-- main 4 many_cities_states
SELECT count(*) as many_cities_stats
FROM places
WHERE city_id in
      (SELECT a.id
       FROM cities a
       WHERE a.name in ("Pearl City", "Douglas", "Jackson", "Tupelo", "Lafayette")
       UNION
       SELECT b.id
       FROM cities b
       JOIN states on b.state_id = states.id
       WHERE states.name in ("Illinois", "California", "Alabama")
       );
