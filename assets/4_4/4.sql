SELECT DISTINCT a.title
FROM album a
JOIN album_artist aa ON a.id = aa.album_id
JOIN artist_genre ag ON aa.artist_id = ag.artist_id
GROUP BY a.id, a.title, aa.artist_id
HAVING COUNT(DISTINCT ag.genre_id) > 1;

SELECT s.title
FROM song s
LEFT JOIN compilation_song cs ON s.id = cs.song_id
WHERE cs.song_id IS NULL;

SELECT ar.name
FROM song s
JOIN album a ON s.album_id = a.id
JOIN album_artist aa ON a.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE s.duration = (SELECT MIN(duration) FROM song);

SELECT a.title
FROM album a
LEFT JOIN song s ON a.id = s.album_id
GROUP BY a.id, a.title
HAVING COUNT(s.id) = (
    SELECT MIN(track_count)
    FROM (SELECT COUNT(s2.id) AS track_count
          FROM album a2
          LEFT JOIN song s2 ON a2.id = s2.album_id
          GROUP BY a2.id) AS counts);