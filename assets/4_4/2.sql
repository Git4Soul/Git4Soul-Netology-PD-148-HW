SELECT title, duration
FROM song
WHERE duration = (SELECT MAX(duration) FROM song);

SELECT title
FROM song
WHERE duration >= 210;

SELECT title
FROM compilation
WHERE release_year BETWEEN 2018 AND 2020;

SELECT name
FROM artist
WHERE name NOT LIKE '% %';

SELECT title
FROM song
WHERE 
    title ILIKE 'мой %'
    OR title ILIKE '% мой'
    OR title ILIKE '% мой %'
    OR title ILIKE 'мой'
    OR title ILIKE 'my %'
    OR title ILIKE '% my'
    OR title ILIKE '% my %'
    OR title ILIKE 'my';

SELECT title
FROM song
WHERE string_to_array(lower(title), ' ') && ARRAY['мой', 'my'];

SELECT title
FROM song
WHERE title ~* '\m(мой|my)\M';