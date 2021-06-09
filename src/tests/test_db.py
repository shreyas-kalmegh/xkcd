import unittest
import pymysql.cursors
from unittest.mock import Mock, patch
from src.main.util.connections import mysql_config, mysql_test_config


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db = mysql_config["database"]
        cnx = pymysql.connect(**mysql_test_config)

        try:
            cursor = cnx.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        except pymysql.Error as err:
            print(f"Failed creating database: {err}\n")
        finally:
            cursor.close()
            cnx.close

        cnx = pymysql.connect(**mysql_config)

        query = """
        CREATE TABLE IF NOT EXISTS comics (
        num INT,
        name VARCHAR(200),
        alt_text VARCHAR(500),
        link VARCHAR(500) UNIQUE,
        im_link VARCHAR(500) UNIQUE,
        PRIMARY KEY(num, name)
        )  ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
        """

        try:
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
        except pymysql.Error as err:
            print("table creation faile\n")
            print(f"{err}")
        else:
            print("OK")
        finally:
            cursor.close()

        insert_data = [
            ('11', 'Barrel - Part 2', 'Awww.', 'https://xkcd.com/11',
             'https://imgs.xkcd.com/comics/barrel_mommies.jpg')
        ]
        insert_data_query = """INSERT INTO comics VALUES (%s, %s, %s, %s, %s)
                            """
        try:
            cursor = cnx.cursor()
            cursor.executemany(insert_data_query, insert_data)
            cnx.commit()
            print("Data successfully inserted\n")
        except pymysql.Error as err:
            print(f"Data insertion to test_table failed {err}\n")
        finally:
            cursor.close()

        cnx.close()

    @classmethod
    def tearDownClass(cls):

        # drop test database
        try:
            db = mysql_config["database"]
            cnx = pymysql.connect(**mysql_config)
            cursor = cnx.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {db}")
            cnx.commit()
        except pymysql.Error as err:
            print(f"{err}")
        finally:
            cursor.close()
            cnx.close()

    def testSelect(self):
        expected_data = [{
            'num':
            11,
            'name':
            'Barrel - Part 2',
            'alt_text':
            'Awww.',
            'link':
            'https://xkcd.com/11',
            'im_link':
            'https://imgs.xkcd.com/comics/barrel_mommies.jpg'
        }]

        # select data
        try:
            db = mysql_config["database"]
            cnx = pymysql.connect(**mysql_config)
            cursor = cnx.cursor()
            query = """
            SELECT
            *
            FROM comics
            """

            cursor.execute(query.strip())
            results = cursor.fetchall()
            self.assertListEqual(results, expected_data)
        except pymysql.Error as err:
            print(f"{err}")
        finally:
            cursor.close()
            cnx.close()
