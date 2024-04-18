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
@click.argument('sqft_living')
@click.argument('sqft_lot')
@click.argument('sqft_above')
@click.argument('sqft_basement')
def addsqft(sqft_living, sqft_lot, sqft_above, sqft_basement ):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO sqft (sqft_living, sqft_lot, sqft_above, sqft_basement) VALUES (?, ?, ?, ?)''', (sqft_living, sqft_lot, sqft_above, sqft_basement,))
        id = cursor.lastrowid
        print('On id (', id, ') Adding sqft_living (', sqft_living, ') Adding sqft_lot (', sqft_lot, ') Adding sqft_above (', sqft_above, ') Adding sqft_basement (', sqft_basement, ') to table ( sqft )' )
        #print(f'inserted with name={interest}')
        


@click.command()
def getbasics():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM basics''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getsqft():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM sqft''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def gettime():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM time''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getlocation():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM location''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getamenities():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM amenities''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

cli.add_command(create)
cli.add_command(addsqft)
cli.add_command(getbasics)
cli.add_command(getsqft)
cli.add_command(gettime)
cli.add_command(getlocation)
cli.add_command(getamenities)


cli()
