from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(2)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		#test URL
		self.browser.get(self.live_server_url)

		# page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text 
		self.assertIn('To-Do', header_text)


		# user is invited to enter a to-do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
		)

		# User types "Buy Peacock feathers" into a text box
		inputbox.send_keys('Buy peacock feathers')

		# user hits enter, the page updates, page lists:
		# "1: Buy peacock feathers" as an item in a to-do list table
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url # assume that this url is unique to Edith's list
		self.assertRegex(edith_list_url, '/lists/.+') # look for regex match, that url includes /lists/
		self.check_for_row_in_list('1: Buy peacock feathers')

		# still a text box inviting user to add another item, user enters:
		# "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on her list
		self.check_for_row_in_list('1: Buy peacock feathers')
		self.check_for_row_in_list('2: Use peacock feathers to make a fly')

		# Now a new user, Francis, comes along to the site.

		## We use a new browser session to make sure that no information 
		## of Edith's is coming though from the cookies etc
		self.broswer.qui()
		self.broswer = webdriver.Firefox()

		# Francis visits the home page.  There is no sign of Edith's list
		self.broswer.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy Peacock', page_text)
		self.assertNotIn('make a fly', page_text)

		# Fancis starts a new list by entering a new item. He is less
		# interesting than Edith / / /
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		# Francis gets his own URL
		francis_list_url - self.broswer.current_url
		self.assertRegex(francis_list_url, 'lists/.+')
		self.asserNotEqual(francis_list_url, edith_list_url)

		# Again, there is no trace of Edith'slist
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Bue peacock', page_text)
		self.assertIn('Buy milk', page_text)


		# Edith wonders whether the stie will remember he list. Then she 
		# sees that the site has generated a unique URL for here -- there is some
		# explanatory text to that effect.
		self.fail('Finish the test')

