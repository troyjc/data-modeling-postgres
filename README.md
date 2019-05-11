# Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The goal of this project is to create a Postgres database with tables designed to optimize queries on song play analysis.

# ETL Pipeline
See file `etl.pt` for the ETL pipeline code, `sql_queries.py` for table creation and deletion functions insertion queries. The file `create_tables.py` is used to create the tables in the `sparkifydb` database.

# Star Schema
There is one fact table named <tt>songplays</tt> and *four* dimension tables:
- <tt>users</tt>
- <tt>songs</tt>
- <tt>artists</tt>
- <tt>time</tt>

```SQL
CREATE TYPE sex as ENUM('F', 'M');
CREATE TYPE level as ENUM('free', 'paid');
```

| <tt>songplays</tt> |  |
| ----------- | ----------- |
| songplay_id | SERIAL PRIMARY KEY |
| start_time | timestamp NOT NULL |
| user_id | int REFERENCES users(user_id) |
| level | level |
| song_id | text REFERENCES songs(song_id) |
| artist_id | text REFERENCES artists(artist_id) |
| session_id | int NOT NULL |
| location | text |
| user_agent | text |

| <tt>users</tt> |  |
| ----------- | ----------- |
| user_id | int PRIMARY KEY |
| first_name | text NOT NULL |
| last_name | text NOT NULL |
| gender | sex |
| level | level NOT NULL |

| <tt>songs</tt> |  |
| ----------- | ----------- |
| song_id | text PRIMARY KEY |
| title | text NOT NULL |
| artist_id | text NOT NULL |
| year | int |
| duration | numeric(10, 5) |

| <tt>artists</tt> |  |
| ----------- | ----------- |
| artist_id | text PRIMARY KEY |
| name | text NOT NULL |
| location | text |
| lattitude | float |
| longitude | float |

| <tt>time</tt> |  |
| ----------- | ----------- |
| start_time | time |
| hour | int |
| day | int |
| week | int |
| month | int |
| year | int |
| weekday | int |

Note that I am not referencing the <tt>time</tt> table, because I elected to use a `timestamp` for the song play start time.

# Conflicts
There can be conflicts when inserting into the tables. The <tt>users</tt> and <tt>artists</tt> tables have clauses to handle this *upsert* logic:

```SQL
INSERT INTO users (user_id, first_name, last_name, gender, level)
                   VALUES(%s, %s, %s, %s, %s)
                   ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level
```

```SQL
INSERT INTO artists (artist_id, name, location, lattitude, longitude)
                     VALUES(%s, %s, %s, %s, %s)
                     ON CONFLICT (artist_id) DO UPDATE SET location = EXCLUDED.location,
                                                           lattitude = EXCLUDED.lattitude,
                                                           longitude = EXCLUDED.longitude
```
