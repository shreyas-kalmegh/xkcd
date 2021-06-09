from unittest.mock import Mock, patch
import unittest
from src.main.api_helpers import download_image, get_random_comics
from requests import Session


class ApiTest(unittest.TestCase):
    @patch.object(Session, 'get')
    def test_download_image(self, mock_get):
        image = "image_data"
        url = r"http://test.com"

        mock_get.return_value.status_code = 200
        mock_get.return_value.content = image

        try:
            response = download_image(url)
            #assert if the function returns the correct data
            self.assertEqual(response, image)
        except Exception as e:
            print(e)

    @patch("src.main.api_helpers.download_image")
    @patch.object(Session, 'get')
    def test_get_random_comics(self, mock_get, mock_download_image):
        image = "image_data"
        comic_d = {
            'month': '1',
            'num': 11,
            'link': '',
            'year': '2006',
            'news': '',
            'safe_title': 'Barrel - Part 2',
            'transcript':
            '[[A boy sits in a barrel which is floating in an ocean.]]\nBoy: None of the places i floated had mommies.\n{{Alt: Awww.}}',
            'alt': 'Awww.',
            'img': 'https://imgs.xkcd.com/comics/barrel_mommies.jpg',
            'title': 'Barrel - Part 2',
            'day': '1'
        }
        comic_l = [('11', 'Barrel - Part 2', 'Awww.', 'https://xkcd.com/11',
                    'image_data',
                    'https://imgs.xkcd.com/comics/barrel_mommies.jpg', '11')]

        mock_download_image.return_value = image
        mock_get().json.return_value = comic_d

        try:
            data = get_random_comics(1)
            #assert if the function returns correct data
            self.assertListEqual(data, comic_l)
        except Exception as e:
            print(e)
