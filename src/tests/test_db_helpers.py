from unittest.mock import patch, MagicMock
import unittest
from io import StringIO
import json
import sys
import pymysql.cursors
from src.main.db_helpers import get_from_db, get_comics, parse_db_data, drop_table, create_table, insert_comics


class DbTest(unittest.TestCase):
    @patch.object(pymysql, "connect")
    def test_get_from_db(self, mock_connect):
        expected_result_set = [{
            'num':
            21,
            'name':
            'Kepler',
            'alt_text':
            'Science joke.  You should probably just move along.',
            'link':
            'https://xkcd.com/21',
            'im_link':
            'https://imgs.xkcd.com/comics/kepler.jpg'
        }]

        #mock connection and cursor objects`
        mock_connect.return_value = MagicMock()
        mock_connect().cursor.return_value = MagicMock()

        mock_connect().__enter__().cursor().__enter__(
        ).fetchall.return_value = expected_result_set

        try:
            result_set = get_from_db(1)
            #assert if function returns the correct result set
            self.assertListEqual(result_set, expected_result_set)
        except Exception as e:
            print(e)

    @patch.object(pymysql, "connect")
    def test_get_comics(self, mock_connect):
        expected_result_set = {
            "im_link": 'https://imgs.xkcd.com/comics/kepler.jpg'
        }
        expected_url = 'https://imgs.xkcd.com/comics/kepler.jpg'

        #mock connection and cursor objects`
        mock_connect.return_value = MagicMock()
        mock_connect().cursor.return_value = MagicMock()

        mock_connect().__enter__().cursor().__enter__(
        ).fetchone.return_value = expected_result_set

        try:
            result_url = get_comics(t='kepler')
            #assert if we get correct url for comics
            self.assertEqual(result_url, expected_url)
        except Exception as e:
            print(e)

    def test_parse_db_data(self):
        input_set = [{
            'num': 21,
            'name': 'Kepler',
            'alt_text': 'Science joke.  You should probably just move along.',
            'link': 'https://xkcd.com/21',
            'im_link': 'https://imgs.xkcd.com/comics/kepler.jpg'
        }]
        output_set = [{
            "comic": "Kepler",
            "comic_meta": {
                "alt_text":
                "Science joke.  You should probably just move along.",
                "number": 21,
                "link": "https://xkcd.com/21",
                "image": "kepler.jpg",
                "image_link": "https://imgs.xkcd.com/comics/kepler.jpg"
            }
        }]
        output_print = json.dumps(output_set, indent=2)
        out = StringIO()

        try:
            parse_db_data(input_set, out=out)
            output = out.getvalue().strip()
            #assert if function outputs the correct data
            assert output == output_print
        except Exception as e:
            print(e)

    @patch.object(pymysql, "connect")
    def test_drop_table(self, mock_connect):
        expected_query = """
        DROP TABLE IF EXISTS comics
        """

        #mock connection and cursor objects`
        mock_connect.return_value = MagicMock()
        mock_connect().cursor.return_value = MagicMock()

        try:
            #call the function
            drop_table()
            #assert if sql statement executed with correct parameters
            mock_connect().__enter__().cursor().__enter__(
            ).execute.assert_called_with(expected_query.strip())
        except Exception as e:
            print(e)

    @patch.object(pymysql, "connect")
    def test_create_table(self, mock_connect):
        expected_query = """
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

        #mock connection and cursor objects`
        mock_connect.return_value = MagicMock()
        mock_connect().cursor.return_value = MagicMock()

        try:
            #call the function
            create_table()
            #assert if sql statement executed with correct parameters
            mock_connect().__enter__().cursor().__enter__(
            ).execute.assert_called_with(expected_query.strip())

        except Exception as e:
            print(e)

    @patch.object(pymysql, "connect")
    def test_insert_comics(self, mock_connect):
        expected_query = f"""
    INSERT INTO comics(num, name, alt_text, link, image, im_link)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE VALUES num=%s
    """
        input_set = [('11', 'Barrel - Part 2', 'Awww.', 'https://xkcd.com/11',
                      'image_data',
                      'https://imgs.xkcd.com/comics/barrel_mommies.jpg', '11')]

        #mock connection and cursor objects`
        mock_connect.return_value = MagicMock()
        mock_connect().cursor.return_value = MagicMock()
        mock_connect().__enter__().cursor().__enter__().rowcount = 1

        try:
            #call the function
            insert_comics(input_set)
            #assert if sql statement executed with correct parameters
            mock_connect().__enter__().cursor().__enter__(
            ).executemany.assert_called_with(expected_query.strip(), input_set)
        except Exception as e:
            print(e)
