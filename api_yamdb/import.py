import csv
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()


with open('static/data/users.csv', 'rt') as f:
    for line in f:
        split_line = line.split(',')
        if 'id' in split_line:
            listed = list(split_line)
            number = len(listed)
    dr = csv.DictReader(f, delimiter=',')
    to_db = [(i['id'], i['username'], i['email'], i['role'], i['bio'], i['first_name'], i['last_name']) for i in dr]
    
cur.executemany("INSERT INTO users_customuser (id, username, email, role, bio, first_name, last_name) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
cur.execute("SELECT sqlite_manager")
con.commit()
con.close()