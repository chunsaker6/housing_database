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
        cursor.execute('''INSERT INTO time (property_listing, year_built, year_reno)
VALUES (?, ?, ?)''', (property_listing, year_built, year_reno))
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
        cursor.execute('''INSERT INTO location (zipcode, lat, longitude) VALUES (?, ?, ?)''', (zipcode, lat, longitude))
        id = cursor.lastrowid
        print('On id (', id, ') Adding zipcode(', zipcode, '), lat(', lat, '), longitude(', longitude, '), into table location')

@click.command()
@click.argument('sqft_living')
@click.argument('sqft_lot')
@click.argument('sqft_above')
@click.argument('sqft_basement')
def addSqft(sqft_living, sqft_lot, sqft_above, sqft_basement ):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''INSERT INTO sqft (sqft_living, sqft_lot, sqft_above, sqft_basement) VALUES (?, ?, ?, ?)''', (sqft_living, sqft_lot, sqft_above, sqft_basement,))
        id = cursor.lastrowid
        print('On id (', id, ') Adding sqft_living (', sqft_living, ') Adding sqft_lot (', sqft_lot, ') Adding sqft_above (', sqft_above, ') Adding sqft_basement (', sqft_basement, ') to table ( sqft )' )
        #print(f'inserted with name={interest}')


@click.command()
def getBasics():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM basics''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getSqft():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM sqft''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getTime():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM time''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getLocation():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM location''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid

@click.command()
def getAmenities():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT * FROM amenities''')
        for row in cursor:
            print(row)
        id = cursor.lastrowid


@click.command()
def getAveragePriceThreeBed():
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT AVG(price) AS average_price_3_bedroom
                        FROM basics
                        WHERE bedrooms = 3;
                       ''')
        for row in cursor:
            print(row)
        #id = cursor.lastrowid


@click.command()
@click.argument('zip_code')
def getAveragePricePerSqftByZip(zip_code):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT l.zipcode,
                        AVG(b.price * 1.0 / s.sqft_lot) AS average_price_per_sqft_lot
                        FROM location l
                        JOIN basics b ON l.id = b.id
                        JOIN sqft s ON l.id = s.id
                        WHERE l.zipcode = (?)
                        GROUP BY l.zipcode;
                       ''', (zip_code))
        for row in cursor:
            print(row)
        #id = cursor.lastrowid
            

@click.command()
@click.argument('floor')
def getAvgPriceByFloor(floor):
    with getdb() as con:
        cursor = con.cursor()
        cursor.execute('''SELECT a.floors,
                        AVG(b.price) AS average_price
                        FROM basics b
                        JOIN amenities a ON b.id = a.id
                        WHERE a.floors = (?)
                        GROUP BY a.floors;
                       ''', (floor))
        for row in cursor:
            print(row)
        #id = cursor.lastrowid

cli.add_command(create)
cli.add_command(addBasics)
cli.add_command(addTime)
cli.add_command(addAmenities)
cli.add_command(addLocation)
cli.add_command(addSqft)
cli.add_command(getBasics)
cli.add_command(getSqft)
cli.add_command(getTime)
cli.add_command(getLocation)
cli.add_command(getAmenities)
cli.add_command(getAveragePriceThreeBed)
cli.add_command(getAveragePricePerSqftByZip)
cli.add_command(getAvgPriceByFloor)



cli()
