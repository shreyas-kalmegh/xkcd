from collections import OrderedDict
import json
import sys
from typing import IO
import pymysql.cursors
from src.main.util.connections import mysql_config


def drop_table() -> None:
    """
    Drops comics table.

    Returns
    -------
    None

    Examples
    --------
    >>> drop_table()
    """

    #define query to drop comics table
    query = """
    DROP TABLE IF EXISTS comics
    """

    try:
        #create a cursor with a connection and execute query
        with pymysql.connect(**mysql_config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute(query.strip())
    except Exception as e:
        print(e)
    else:
        print("OK\n")


def create_table() -> None:
    """
    Create comics table. Checkout README.md file for schema.  

    Returns
    -------
    None

    >>> create_table()
    """

    #define query to create comics table
    query = """
    CREATE TABLE IF NOT EXISTS comics (
    num INT,
    name VARCHAR(200),
    alt_text VARCHAR(500),
    link VARCHAR(500) UNIQUE,
    image MEDIUMBLOB,
    im_link VARCHAR(500) UNIQUE,
    PRIMARY KEY(num, name)
    )  ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
    """

    try:
        #create a cursor with a connection and execute query
        with pymysql.connect(**mysql_config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute(query.strip())
    except Exception as e:
        print(e)
    else:
        print("OK\n")


def get_from_db(n: int = 5) -> list[dict]:
    """
    Get records from the comics table from the database.

    Parameters
    ----------
    n : int
        Number of records to fetch

    Returns
    -------
    list[dict]
        Returns a list of rows as dictionaries

    Examples
    --------
    >>> n = 1
    >>> get_from_db(1)
    [{'num': 21, 'name': 'Kepler', 'alt_text': 'Science joke.  You should probably just move along.', 
    'link': 'https://xkcd.com/21', 'im_link': 'https://imgs.xkcd.com/comics/kepler.jpg'}]
    """

    #define query to get n number of records from the comics table
    query = f"""
    SELECT
    num,
    name,
    alt_text,
    link,
    im_link
    FROM comics limit {n}
    """

    try:
        #create a cursor with a connection and execute query
        with pymysql.connect(**mysql_config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                #return the list of records as list of dictionaries
                return results
    except Exception as e:
        print(e)
    else:
        print("OK\n")


def get_comics(n: int = None, t: str = None) -> str:
    """
    Get comics from the comics table from the database. Parameters are mutually exclusive.

    Parameters
    ----------
    n : int
        Number of comics to fetch
    t : str
        Title of comics to fetch

    Returns
    -------
    str
        Returns url of the image of the comics

    Examples
    --------
    >>> get_comics(n=21)
    'https://imgs.xkcd.com/comics/kepler.jpg'
    >>> get_comics(t='kepler')
    'https://imgs.xkcd.com/comics/kepler.jpg'
    """

    #define query to get n number of records from the comics table
    if n and t:
        raise Exception(
            "Arguments are mutually exclusive. Provide only one argument.")
    elif n:
        field = "num"
        value = int(n)
    elif t:
        field = "lower(name)"
        value = f"'{t.lower()}'"

    query = f"""
    SELECT
    DISTINCT
    im_link
    FROM comics 
    WHERE
    {field} = {value}
    """

    try:
        #create a cursor with a connection and execute query
        with pymysql.connect(**mysql_config) as cnx:
            with cnx.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchone()
                #parse url and return it
                url = results["im_link"]
                return url
    except Exception as e:
        print(e)
    else:
        print("OK\n")


def parse_db_data(data: list[dict] = None, out: IO[str] = sys.stdout) -> None:
    """
    Parse records to a desired format. Print the records in order.

    Parameters
    ----------
    data : list[dict]
        Number of records to fetch

    Returns
    -------
    None
    
    Examples
    --------
    >>> data = get_from_db(10)
    >>> parse_db_data(data)
    {
        "comic": "Solar Plexus",
        "comic_meta": {
          "alt_text": "It hurts to be hit there, you know",
          "number": 64,
          "link": "https://xkcd.com/64",
          "image": "solar_plexus.jpg",
          "image_link": "https://imgs.xkcd.com/comics/solar_plexus.jpg"
        }
    }
    """

    #list object to hold comics data
    comic_l = []
    for row in data:
        #parse the data and store in the dictionary format
        comic_d = OrderedDict()
        comic_d["comic"] = row["name"]
        comic_meta_d = OrderedDict()
        comic_d["comic_meta"] = comic_meta_d
        comic_meta_d["alt_text"] = row["alt_text"]
        comic_meta_d["number"] = row["num"]
        comic_meta_d["link"] = row["link"]
        comic_meta_d["image"] = row["im_link"].split("comics/", 1)[1]
        comic_meta_d["image_link"] = row["im_link"]
        comic_l.append(comic_d)
    #pretty print the comics data
    out.write(json.dumps(comic_l, indent=2))


def insert_comics(data: list[tuple]) -> None:
    """
    Get records from the comics table from the database.

    Parameters
    ----------
    data : list[dict]
        Insertes the given list of records into comics.

    Returns
    -------
    None    
    """

    #query to insert data into the comics table
    query = f"""
    INSERT INTO comics(num, name, alt_text, link, image, im_link)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE VALUES num=%s
    """

    try:
        #create a cursor with a connection and execute query
        with pymysql.connect(**mysql_config) as cnx:
            with cnx.cursor() as cursor:
                #insert all records at once
                cursor.executemany(query.strip(), data)
                cnx.commit()
                print(f"{cursor.rowcount} records inserted!!\n")
    except Exception as e:
        print(e)
    else:
        print("OK\n")