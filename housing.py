#!/usr/bin/env python3

import click
import os
import sqlite3
import sys

DB_FILE = 'network.db'

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
'''CREATE TABLE users (
    id          INTEGER PRIMARY KEY,
    email       TEXT NOT NULL
)''')
        con.execute(
'''CREATE UNIQUE INDEX users_email ON users (email)''')

        con.execute(
'''CREATE TABLE accounts (
    id          INTEGER PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    username    TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
)''')
        con.execute(
'''CREATE TABLE followers (
    id          INTEGER NOT NULL,
    follower_id     INTEGER NOT NULL,

    PRIMARY KEY (id, follower_id)
    FOREIGN KEY (id) REFERENCES accounts (id) ON DELETE CASCADE ON UPDATE CASCADE
    FOREIGN KEY (follower_id) REFERENCES accounts (id) ON DELETE CASCADE ON UPDATE CASCADE
)''')
        con.execute(
'''CREATE TABLE posts (
    id          INTEGER PRIMARY KEY,
    text        TEXT NOT NULL,
    account_id  INTEGER NOT NULL,

    FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE ON UPDATE CASCADE
)''')
        con.execute(
'''CREATE TABLE interests (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL
)''')
        con.execute(
'''CREATE TABLE hasinterests (
    account_id       INTEGER NOT NULL,
    interest_id      INTEGER NOT NULL,

    PRIMARY KEY (account_id, interest_id)
    FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE ON UPDATE CASCADE
    FOREIGN KEY (interest_id) REFERENCES interests (id) ON DELETE CASCADE ON UPDATE CASCADE
)''')
        con.execute(
'''CREATE TABLE comments (
    account_id      INTEGER NOT NULL,
    post_id         INTEGER NOT NULL,
    content         TEXT NOT NULL,

    PRIMARY KEY (account_id, post_id)
    FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE ON UPDATE CASCADE
    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE ON UPDATE CASCADE
)''')
    print('database created')

@click.command()
@click.argument('email')
def adduser(email):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO users (email) VALUES (?)''', (email,))
        id = cursor.lastrowid
        print('User (', id, ') created with email address (', email, ')')

@click.command()
@click.argument('email')
@click.argument('username')
def addaccount(email, username):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO accounts (user_id, username)
VALUES ((SELECT id FROM users WHERE email = ?), ?)''', (email, username))
        id = cursor.lastrowid
        print('Account (', id, ') created with username (', username, ') for user (', id, ')(', email,')')
        #print(f'inserted with id={id}')

@click.command()
@click.argument('interest')
def addinterest(interest):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO interests (name) VALUES (?)''', (interest,))
        id = cursor.lastrowid
        print('Added this interest (', interest, ')')
        #print(f'inserted with name={interest}')

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
