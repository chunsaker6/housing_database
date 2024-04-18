#!/usr/bin/env python3

import click
import os
import sqlite3
import sys

DB_FILE = 'housing.db'

def getdb(create=False):
    if os.path.exists(DB_FILE):
        if create:
            os.remove(DB_FILE)
    else:
        if not create:
            print('no database found')
            sys.exit(1)
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con

@click.group()
def cli():
    pass

@click.command()
def create():
    with getdb(create=True) as con:
        con.execute(
'''CREATE TABLE basics(
    id          INTEGER PRIMARY KEY,
    price       INTEGER NOT NULL,
    bedrooms    INTEGER,
    bathrooms   INTEGER
)''')


        con.execute(
'''CREATE TABLE sqft(
    id              INTEGER PRIMARY KEY,
    sqft_living     INTEGER,
    sqft_lot        INTEGER,
    sqft_above      INTEGER,
    sqft_basement   INTEGER
)''')

        con.execute(
'''CREATE TABLE time(
    id               INTEGER PRIMARY KEY,
    property_listing DATE,
    year_built       INTEGER,
    year_reno        INTEGER
)''')


        con.execute(
'''CREATE TABLE location(
    id          INTEGER PRIMARY KEY,
    zipcode     INTEGER,
    lat         FLOAT,
    longitude   FLOAT
)''')

        con.execute(
'''CREATE TABLE amenities(
    id          INTEGER PRIMARY KEY,
    floors      INTEGER,
    waterfront  INTEGER,
    the_view    INTEGER,
    condition   INTEGER,
    grade       INTEGER
)''')

    print('database created')


@click.command()
@click.argument('price')
@click.argument('bathrooms')
@click.argument('bedrooms')
def addBasics(price, bathrooms, bedrooms):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO basics (price, bathrooms, bedrooms) VALUES (?, ?, ?)''', (price, bathrooms, bedrooms,))
        id = cursor.lastrowid
        print('On id (', id, ') Adding price(', price, '), bathrooms(', bathrooms, '), bedrooms(',bedrooms, '), into table basics') 

@click.command()
@click.argument('property_listing')
@click.argument('year_built')
@click.argument('year_reno')
def addTime(property_listing, year_built, year_reno):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO sqft (property_listing, year_built, year_reno)
VALUES (?, ?, ?)''', (propery_listing, year_built, year_reno))
        id = cursor.lastrowid
        print('On id (', id, ') Adding property_listing(', property_listing, '), year_built(', year_built, '), year_reno(', year_reno, '), into table time') 

@click.command()
@click.argument('floors')
@click.argument('waterfront')
@click.argument('the_view')
@click.argument('condition')
@click.argument('grade')
def addAmenities(floors, waterfront, the_view, condition, grade):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO amenities (floors, waterfront, the_view, condition, grade)
VALUES (?, ?, ?, ?, ?)''', (floors, waterfront, the_view, condition, grade))
        id = cursor.lastrowid
        print('On id (', id, ') Adding floors (', floors, '), waterfront (', waterfront, '), view (', the_view, '), condtion (', condition, '), grade (', grade, ') into table amenities') 

@click.command()
@click.argument('zipcode')
@click.argument('lat')
@click.argument('longitude')
def addLocation(zipcode, lat, longitude):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO loaction (zipcode, lat, longitude) VALUES (?, ?, ?)''', (zipcode, lat, longitude))
        id = cursor.lastrowid
        print('On id (', id, ') Adding zipcode(', zipcode, '), lat(', lat, '), longitude(', longitude, '), into table loaction') 

@click.command()
@click.argument('zipcode')
@click.argument('lat')
@click.argument('longitude')
def addLocation(zipcode, lat, longitude):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO loaction (zipcode, lat, longitude) VALUES (?, ?, ?)''', (zipcode, lat, longitude))
        id = cursor.lastrowid
        print('Added location info')

@click.command()
@click.argument('account_id')
@click.argument('interest_id')
def addaccountinterest(account_id, interest_id):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO hasinterests (account_id, interest_id) VALUES (?, ?)''', (account_id, interest_id,))
        id = cursor.lastrowid
        print('Account (', account_id, ') has this interest (', interest_id, ')')
        #print(f'inserted with name={interest}')

@click.command()
@click.argument('text')
@click.argument('account')
def addpost(text, account):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO posts (text, account_id) VALUES (?, ?)''', (text, account))
        id = cursor.lastrowid
        print('Posted to account (', id, ')(',  text, ')')
        #print(f'inserted with comment={text}')
        
@click.command()
@click.argument('account')
@click.argument('post')
@click.argument('comment')
def addcomment(account,  post, comment):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO comments (account_id, post_id, content) VALUES (?, ?, ?)''', (account, post, comment))
        id = cursor.lastrowid
        #print(f'inserted with comment={comment}')
        print('Creating comment (', comment, ') on a post (', post, ') from account (', account, ')')


@click.command()
def getcomment():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM comments''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getpost():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM posts''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getuser():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM users''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getaccount():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM accounts''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getinterest():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM interests''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def gethasinterest():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM hasinterests''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getallsimilarinterests():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT accounts.id, a2.id, SUM(1) FROM accounts
                       JOIN hasinterests on accounts.id = hasinterests.account_id
                       JOIN interests on hasinterests.interest_id = interests.id
                       JOIN hasinterests h2 on interests.id = h2.interest_id
                       JOIN accounts a2 on a2.id = h2.account_id where accounts.id != a2.id
                       GROUP BY accounts.id, a2.id
                       ''')
        for row in cursor:
            print(row)
        #id = cursor.lastrowid

@click.command()
@click.argument('account_id')
def getsimilarinterests(account_id):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT accounts.id, a2.id, SUM(1) FROM accounts
                       JOIN hasinterests on accounts.id = hasinterests.account_id
                       JOIN interests on hasinterests.interest_id = interests.id
                       JOIN hasinterests h2 on interests.id = h2.interest_id
                       JOIN accounts a2 on a2.id = h2.account_id 
                       WHERE accounts.id != a2.id
                       AND accounts.id = (?)
                       GROUP BY accounts.id, a2.id
                       ORDER BY SUM(1) DESC
                       ''', (account_id))
        for row in cursor:
            print(row)
        #id = cursor.lastrowid
            
@click.command()
def getallsimilarcomments():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT accounts.id, a2.id, posts.id, posts.text, SUM(1) FROM accounts
                       JOIN comments on accounts.id = comments.account_id
                       JOIN posts on comments.post_id = posts.id
                       JOIN comments c2 on c2.post_id = posts.id
                       JOIN accounts a2 on a2.id = c2.account_id where accounts.id != a2.id 
                       group by accounts.id, a2.id
                       ''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
@click.argument('account_id')
def getsimilarcomments(account_id):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT accounts.id, a2.id, posts.id, posts.text, SUM(1) FROM accounts
                       JOIN comments on accounts.id = comments.account_id
                       JOIN posts on comments.post_id = posts.id
                       JOIN comments c2 on c2.post_id = posts.id
                       JOIN accounts a2 on a2.id = c2.account_id 
                       WHERE accounts.id != a2.id
                       AND accounts.id = (?)
                       GROUP BY accounts.id, a2.id
                       ORDER BY SUM(1) DESC
                       ''', (account_id))
        for row in cursor:
            print(row)
        #id = cursor.lastrowid

cli.add_command(create)
cli.add_command(adduser)
cli.add_command(addaccount)
cli.add_command(addpost)
cli.add_command(addinterest)
cli.add_command(addaccountinterest)
cli.add_command(addcomment)
cli.add_command(getcomment)
cli.add_command(getpost)
cli.add_command(getuser)
cli.add_command(getaccount)
cli.add_command(getinterest)
cli.add_command(getallsimilarinterests)
cli.add_command(getsimilarinterests)
cli.add_command(getallsimilarcomments)
cli.add_command(getsimilarcomments)

cli()
