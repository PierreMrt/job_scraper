# A regarder plus tard

Regarder le champs ForeignKeys dans la documentation de django

> category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)


## SQL commands to convert for Django

```sql
-- create search table
    sql = """CREATE TABLE IF NOT EXISTS search (
                id integer PRIMARY KEY,
                user text NOT NULL,
                job text,
                country text,
                search_key text
            )"""
    c.execute(sql)

-- create links table
    sql = """CREATE TABLE IF NOT EXISTS links (
                id integer PRIMARY KEY,
                country text NOT NULL,
                extension text,
                LinkedIn text,
                Monster text,
                Indeed text
            )"""
    c.execute(sql)

-- create users table
    sql = """CREATE TABLE IF NOT EXISTS users (
                id integer PRIMARY KEY,
                username text NOT NULL,
                mail text,
                password text
            )"""
    c.execute(sql)

-- create results table
    sql = """CREATE TABLE IF NOT EXISTS results (
                id integer PRIMARY KEY,
                search_key text NOT NULL,
                source text,
                job_id,
                job_title text,
                description text,
                company text,
                location text,
                country text,
                date datetime,
                link text
            )"""
  ```