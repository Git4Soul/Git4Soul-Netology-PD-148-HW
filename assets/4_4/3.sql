SELECT g.name, COUNT(ag.artist_id) AS artist_count
FROM genre g
LEFT JOIN artist_genre ag ON g.id = ag.genre_id
GROUP BY g.id, g.name;

SELECT COUNT(s.id) AS track_count
FROM song s
JOIN album a ON s.album_id = a.id
WHERE a.release_date BETWEEN '2019-01-01' AND '2020-12-31';

SELECT a.id, a.title, AVG(s.duration) AS avg_duration
FROM album a
LEFT JOIN song s ON a.id = s.album_id
GROUP BY a.id, a.title;

SELECT DISTINCT ar.name
FROM artist ar
WHERE ar.id NOT IN (
    SELECT aa.artist_id
    FROM album_artist aa
    JOIN album a ON aa.album_id = a.id
    WHERE EXTRACT(YEAR FROM a.release_date) = 2020);

SELECT DISTINCT c.title
FROM compilation c
JOIN compilation_song cs ON c.id = cs.compilation_id
JOIN song s ON cs.song_id = s.id
JOIN album a ON s.album_id = a.id
JOIN album_artist aa ON a.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE ar.name = 'ДДТ';
