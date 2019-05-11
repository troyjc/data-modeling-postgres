# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id serial primary key,
                                                                  start_time timestamp not null,
                                                                  user_id int,
                                                                  level level not null,
                                                                  song_id text,
                                                                  artist_id text,
                                                                  session_id int not null,
                                                                  location text,
                                                                  user_agent text,
                                                                       
                                                                  foreign key(user_id)
                                                                    references users(user_id),

                                                                  foreign key(song_id)
                                                                    references songs(song_id),

                                                                  foreign key(artist_id)
                                                                    references artists(artist_id));
""")

user_table_create = ("""CREATE TYPE sex as ENUM('F', 'M');
                        CREATE TYPE level as ENUM('free', 'paid');

                        CREATE TABLE IF NOT EXISTS users (user_id int primary key,
                                                          first_name text not null,
                                                          last_name text not null,
                                                          gender sex,
                                                          level level not null);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id text primary key,
                                                          title text not null,
                                                          artist_id text not null,
                                                          year int,
                                                          duration numeric(10, 5));
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id text primary key,
                                                              name text not null,
                                                              location text,
                                                              lattitude float,
                                                              longitude float);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time time,
                                                         hour int,
                                                         day int,
                                                         week int,
                                                         month int,
                                                         year int,
                                                         weekday int);
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                        VALUES(%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
                        VALUES(%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, lattitude, longitude)
                          VALUES(%s, %s, %s, %s, %s) 
                          ON CONFLICT (artist_id) DO UPDATE SET location = EXCLUDED.location,
                                                                lattitude = EXCLUDED.lattitude,
                                                                longitude = EXCLUDED.longitude
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                        VALUES(%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""SELECT
                    song_id,
                    artist_id
                  FROM
                    songs
                  WHERE
                    title = %s
                    AND artist_id =
                    (
                      SELECT
                        artist_id
                      FROM
                        artists
                      WHERE
                        name = %s
                    )
                    AND duration = %s;
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, song_table_create, songplay_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, artist_table_drop, song_table_drop, time_table_drop]
