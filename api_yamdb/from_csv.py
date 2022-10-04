import csv
import sqlite3
import datetime

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/category.csv', 'rt', encoding=('utf8')) as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['name'], i['slug']) for i in dr]

cur.executemany("INSERT INTO titles_category "
                "(id, name, slug) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/comments.csv', 'rt', encoding=('utf8')) as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['review_id'],
              i['text'], i['author'], i['pub_date']) for i in dr]

cur.executemany("INSERT INTO reviews_comment "
                "(id, review_id, text, author_id, pub_date) "
                "VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/genre_title.csv', 'rt', encoding=('utf8')) as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['title_id'], i['genre_id']) for i in dr]

cur.executemany("INSERT INTO titles_title_genre "
                "(id, title_id, genre_id) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/genre.csv', 'rt', encoding=('utf8')) as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['name'], i['slug']) for i in dr]

cur.executemany("INSERT INTO titles_genre "
                "(id, name, slug) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/review.csv', 'rt', encoding=('utf8')) as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['title_id'], i['text'],
              i['author'], i['score'], i['pub_date']) for i in dr]

cur.executemany("INSERT INTO reviews_review "
                "(id, title_id, text, author_id, score, pub_date) "
                "VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

with open('static/data/titles.csv', 'rt', encoding=('utf8')) as f:
    dr = csv.DictReader(f, delimiter=",")
    to_db = [(i['id'], i['name'], i['year'], i['category']) for i in dr]

cur.executemany("INSERT INTO titles_title "
                "(id, name, year, category_id) VALUES (?, ?, ?, ?);", to_db)
con.commit()
con.close()

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
now = datetime.datetime.now()

with open('static/data/users.csv', 'rt', encoding=('utf8')) as f:
    dr = csv.DictReader(f, delimiter=",", restval=now)
    to_db = [(i['id'], i['username'], i['email'], i['role'],
              i['bio'], i['first_name'], i['last_name'],
              i['is_superuser'], i['is_staff'], i['is_active'],
              i['date_joined'], i['password']) for i in dr]


cur.executemany("INSERT INTO users_customuser "
                "(id, username, email, role, bio, first_name, last_name, "
                "is_superuser, is_staff, is_active, date_joined, password) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
