from unittest.mock import MagicMock, patch
import unittest
import argparse
import sys
from io import StringIO
from src.main.task_one_helpers import main
from requests import Session


class TaskOneTest(unittest.TestCase):
    @patch("src.main.task_one_helpers.parse_db_data")
    @patch("src.main.task_one_helpers.get_from_db")
    @patch.object(argparse, 'ArgumentParser')
    def test_task_one_list(self, mock_arg_parser, mock_get_from_db,
                           mock_parse_db):
        mock_get_from_db_op = [{
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

        mock_arg_parser.return_value = MagicMock()
        mock_arg_parser(
        ).add_mutually_exclusive_group.return_value = MagicMock()
        mock_arg_parser().parse_args.return_value = argparse.Namespace(
            number=None, title=None, list=True)
        mock_get_from_db.return_value = mock_get_from_db_op

        try:
            with patch('src.main.task_one_helpers.exit') as exit_mock:
                with unittest.mock.patch('sys.argv', ['prog', '-l']) as args:
                    main(args=args)

            #assert if function outputs the correct data
            mock_parse_db.assert_called_with(mock_get_from_db_op)
        except Exception as e:
            print(e)

    @patch("src.main.task_one_helpers.get_comics")
    @patch.object(argparse, 'ArgumentParser')
    def test_task_one_number(self, mock_arg_parser, mock_get_comics):
        mock_get_comics_op = 'https://imgs.xkcd.com/comics/kepler.jpg'

        mock_arg_parser.return_value = MagicMock()
        mock_arg_parser(
        ).add_mutually_exclusive_group.return_value = MagicMock()
        mock_arg_parser().parse_args.return_value = argparse.Namespace(
            number=21, title=None, list=False)
        mock_get_comics.return_value = mock_get_comics_op

        out = StringIO()

        try:
            with patch('src.main.task_one_helpers.exit') as exit_mock:
                with unittest.mock.patch('sys.argv',
                                         ['prog', '-n', '21']) as args:
                    main(args=args, out=out)
                    output = out.getvalue().strip()

            #assert if function outputs the correct data
            self.assertEqual(mock_get_comics_op, out.getvalue())
        except Exception as e:
            print(e)

    @patch("src.main.task_one_helpers.get_comics")
    @patch.object(argparse, 'ArgumentParser')
    def test_task_one_title(self, mock_arg_parser, mock_get_comics):
        mock_get_comics_op = 'https://imgs.xkcd.com/comics/kepler.jpg'

        mock_arg_parser.return_value = MagicMock()
        mock_arg_parser(
        ).add_mutually_exclusive_group.return_value = MagicMock()
        mock_arg_parser().parse_args.return_value = argparse.Namespace(
            number=None, title="kepler", list=False)
        mock_get_comics.return_value = mock_get_comics_op

        out = StringIO()

        try:
            with patch('src.main.task_one_helpers.exit') as exit_mock:
                with unittest.mock.patch('sys.argv',
                                         ['prog', '-t', 'kepler']) as args:
                    main(args=args, out=out)
                    output = out.getvalue().strip()

            #assert if function prints the correct data
            self.assertEqual(mock_get_comics_op, out.getvalue())
        except Exception as e:
            print(e)
