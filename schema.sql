CREATE TABLE basics(
    id          INTEGER PRIMARY KEY,
    price       INTEGER NOT NULL,
    bedrooms    INTEGER,
    bathrooms   INTEGER,
);

CREATE TABLE sqft(
    id              INTEGER PRIMARY KEY,
    sqft_living     INTEGER,
    sqft_lot        INTEGER,
    sqft_above      INTEGER,
    sqft_basement   INTEGER,
    
);

CREATE TABLE time(
    id               INTEGER PRIMARY KEY,
    property_listing DATE,
    year_built       INTEGER,
    year_reno        INTEGER,
    
);

CREATE TABLE location(
    id          INTEGER PRIMARY KEY,
    zipcode     INTEGER,
    lat         FLOAT,
    longitude   FLOAT,
);

CREATE TABLE amenities(
    id          INTEGER PRIMARY KEY,
    floors      INTEGER,
    waterfront  INTEGER,
    the_view    INTEGER,
    condition   INTEGER,
    grade       INTEGER,
);
