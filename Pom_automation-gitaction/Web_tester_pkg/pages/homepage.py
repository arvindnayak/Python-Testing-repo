
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Web_tester_pkg.pages.loginpage import loginpage
from Web_tester_pkg.pages.registerpage import registerpage

class HomePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Locators
    SEARCH_BOX = (By.NAME, 'search')
    SEARCH_BTN = (By.XPATH, '//*[@id="search"]/span/button')
    PRODUCT_LINK = (By.LINK_TEXT, 'HP LP3065')
    NO_PRODUCT_MSG = (By.XPATH, '//input[@id="button-search"]/following-sibling::p')
    ACCOUNT_DROPDOWN = (By.XPATH, '//a[@title="My Account"]')
    LOGIN_LINK = (By.XPATH, '//a[text()="Login"]')
    REGISTER_LINK = (By.XPATH, '//a[text()="Register"]')

    # Actions
    def search_for_product(self, product_name):
        search_box = self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
        search_box.clear()
        search_box.send_keys(product_name)
        
        search_btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BTN))
        search_btn.click()

    def is_product_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.PRODUCT_LINK)).is_displayed()

    def get_no_product_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.NO_PRODUCT_MSG)).text
    def click_account_dropdown(self):
        account_dropdown = self.wait.until(EC.element_to_be_clickable(self.ACCOUNT_DROPDOWN))
        account_dropdown.click()
    def click_login_link(self):
        login_link = self.wait.until(EC.element_to_be_clickable(self.LOGIN_LINK))
        login_link.click()
        return loginpage(self.driver,self.wait)
    def click_register_link(self):
        register_link = self.wait.until(EC.element_to_be_clickable(self.REGISTER_LINK))
        register_link.click()
        return registerpage(self.driver,self.wait)