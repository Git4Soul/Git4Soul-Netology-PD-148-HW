-- Таблица исполнителей
CREATE TABLE artist (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Таблица жанров
CREATE TABLE genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Связь многие-ко-многим между исполнителями и жанрами
CREATE TABLE artist_genre (
    artist_id INT REFERENCES artist(id) ON DELETE CASCADE,
    genre_id INT REFERENCES genre(id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, genre_id)
);

-- Таблица альбомов (без поля artist_id, так как связь теперь через album_artist)
CREATE TABLE album (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL
);

-- Связь многие-ко-многим между альбомами и исполнителями
CREATE TABLE album_artist (
    album_id INT REFERENCES album(id) ON DELETE CASCADE,
    artist_id INT REFERENCES artist(id) ON DELETE CASCADE,
    PRIMARY KEY (album_id, artist_id)
);

-- Таблица треков (принадлежит строго одному альбому)
CREATE TABLE song (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INT NOT NULL, 
    album_id INT NOT NULL REFERENCES album(id) ON DELETE CASCADE
);

-- Таблица сборников
CREATE TABLE compilation (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL
);

-- Связь многие-ко-многим между сборниками и треками
CREATE TABLE compilation_song (
    compilation_id INT REFERENCES compilation(id) ON DELETE CASCADE,
    song_id INT REFERENCES song(id) ON DELETE CASCADE,
    PRIMARY KEY (compilation_id, song_id)
);