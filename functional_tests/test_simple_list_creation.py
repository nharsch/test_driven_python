from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        #test URL
        self.browser.get(self.server_url)

        # page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        # user is invited to enter a to-do item
        inputbox = self.get_item_input_box()
        self.assertEqual(
                        inputbox.get_attribute('placeholder'),
                        'Enter a to-do item'
        )

        # User types "Buy Peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')
        # When she hits enter, she is taken to a new URL,
        # and now the page lists "1: Buy Peacock feathers" as
        # an item in the to-do list table
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url # assume that this url is unique to Edith's list
        self.assertRegex(edith_list_url, '/lists/.+') # look for regex match, that url includes /lists/
        self.check_for_row_in_list('1: Buy peacock feathers')

        # still a text box inviting user to add another item, user enters:
        # "Use peacock feathers to make a fly"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list('1: Buy peacock feathers')
        self.check_for_row_in_list('2: Use peacock feathers to make a fly')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming though from the cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's list
        # import pdb; pdb.set_trace()
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock', page_text)
        self.assertNotIn('make a fly', page_text)

        # Fancis starts a new list by entering a new item. He is less
        # interesting than Edith / / /
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, 'lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith'slist
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock', page_text)
        self.assertIn('Buy milk', page_text)


        # Edith wonders whether the stie will remember he list. Then she
        # sees that the site has generated a unique URL for here -- there is some
        # explanatory text to that effect.
        # self.fail('Finish the test')

