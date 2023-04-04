from selenium import webdriver
import unittest
import tracemalloc

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

tracemalloc.start()

class SearchBoxWithFilterOptionsTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def search_by(self, search_box_input, filter_by):
        """
            Gets search box, filter dropdown and search button and
            confirms if search box input is in search results
        """
        search_box = self.driver.find_element(By.ID, "search-input")
        search_box.send_keys(search_box_input)

        filter_dropdown = self.driver.find_element(By.ID, "filter-options")
        filter_dropdown.click()
        filter_option = self.driver.find_element(By.ID, filter_by)
        filter_option.click()

        search_button = self.driver.find_element(By.ID, "search-btn")
        search_button.click()

        return self.driver.find_elements(By.XPATH, "//table/tbody/tr")

    def test_user_landing_on_home_page(self):
        """
            The User landed on the Sage Integration API Home Page
        """
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        # The User Saw the web pages name/title was Dashboard Transactions
        self.assertIn("Dashboard", self.driver.title)

    def test_user_sees_list_of_transactions(self):
        """
            A list of all transactions that they would like to process starting from the date 20221213
            Was Displayed in a table
        """
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        # Get first transaction in the table and check that it is the one we are looking for
        first_transaction = self.driver.find_element(By.XPATH, "//table/tbody/tr[1]")
        self.assertIsNotNone(first_transaction)

    def test_user_searches_by_vendor_id(self):
        """ Test if user can search for a transaction by vendor id """
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("ZTCL-ZMW", "vendor_id")
        for row in table_rows:
            self.assertIn("ZTCL-ZMW", row.text)

    # The Then Realised that they could perform other filter options and tried them out as follows:
    def test_user_searches_by_invoice_id(self):
        """ Test if user can search for a transaction by invoice id """
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("PP00000000980", "invoice_id")

        for row in table_rows:
            self.assertIn("PP00000000980", row.text)

    def test_user_search_by_date(self):
        """ Test if user can search for a transaction by date """
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("20221213", "date")

        for row in table_rows:
            self.assertIn("20221213", row.text)

    # 3. Search by amount
    def test_user_search_by_amount(self):
        """ Test if user can search for a transaction by amount """
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("5000", "amount")

        for row in table_rows:
            self.assertIn("5000", row.text)

    def test_user_search_by_bank(self):
        """ Test if user can search for a transaction by bank name """
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("FNB", "bank_name")

        for row in table_rows:
            self.assertIsNotNone(row.text)

    # 5. Search by sort code
    def test_user_search_by_sort_code(self):
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("10052", "sort_code")

        for row in table_rows:
            self.assertIn("10052", row.text)

    # 6. Search by account number
    def test_user_search_by_account_number(self):
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("5690213500249", "account_name")

        for row in table_rows:
            self.assertIn("5690213500249", row.text)

    # 7. Search by account name
    def test_user_search_by_account_name(self):
        """ Test if user can search for a transaction by account name """
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        table_rows = self.search_by("Mupuma", "sort_code")

        for row in table_rows:
            self.assertIn("10052", row.text)

    def test_if_user_can_process_transactions(self):
        """ Test if user can process transactions """
        self.driver.refresh()
        self.driver.get("http://localhost:8000/payment-api/dashboard/transactions/")

        # The User then selected the transactions that they would like to process by clicking the checkbox
        # next to each transaction
        checkboxes = self.driver.find_elements(By.XPATH, "//table/tbody/tr/td[1]/input")
        for checkbox in checkboxes:
            checkbox.click()

        # The User then clicked the post transactions button
        post_transactions_button = self.driver.find_element(By.ID, "post-transactions-btn")
        post_transactions_button.click()

        # The User Then saw a model pop up with a list of the transactions that they had selected
        # and a button to post the transactions
        modal = self.driver.find_element(By.ID, "post-transactions-modal")
        self.assertIsNotNone(modal)


if __name__ == "__main__":
    unittest.main()
