# Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The goal of this project is to create a Postgres database with tables designed to optimize queries on song play analysis.

# ETL Pipeline
See file `etl.pt` for the ETL pipeline code, `sql_queries.py` for table creation and deletion functions insertion queries. The file `create_tables.py` is used to create the tables in the `sparkifydb` database.

# Star Schema
There is one fact table named <tt>songplays</tt> and four dimension tables:

```SQL
CREATE TYPE sex as ENUM('F', 'M');
CREATE TYPE level as ENUM('free', 'paid');
```

![ERD Diagram](https://github.com/troyjc/data-modeling-postgres/blob/master/docs/Postgres%20Modeling%20ERD.png)

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
