import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls): # set up is called once instead of before every test method
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://{}'.format(arg.split('=')[1])
                return
        super().setUpClass() # if not new live server in command line, setup as normal
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.close()
        # pass

    def check_for_row_in_list(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


