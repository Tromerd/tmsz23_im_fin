import unittest

# TODO: fix 'ModuleNotFoundError: No module named 'FILM.parser' issue
# from ..film_app.models import *

from ..parser.kinogo_parser import get_film_list, get_html_data


class TestParsers(unittest.TestCase):

    def setUp(self):
        URL_LIST = 'https://kinogo-net.org/v2/page/3/'
        URL_ITEM = 'https://kinogo-net.org/v2/1953-v-ozhidanii-solnca-2013.html'
        self.sp = get_html_data(URL_LIST)

    def test__get_film_list(self):
        lst = get_film_list(self.sp)
        le = len(lst)
        print(le)

        self.assertEqual(10, le)

    def tearDown(self) -> None:
        del self.sp
