from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class loginpage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    EMAIL_INPUT = (By.ID, 'input-email')
    PASSWORD_INPUT = (By.ID, 'input-password')
    LOGIN_BTN = (By.XPATH, "//*[@id='content']/div/div[2]/div/form/input")
    WARNING_MSG = (By.XPATH, "//*[@id='account-login']/div[1]")
    EDIT_ACCOUNT_INFO = (By.LINK_TEXT, 'Edit your account information')

    def login(self, email, password):
        email_field = self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(email)
        
        password_field = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)
        
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()
        return self

    def get_warning_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.WARNING_MSG)).text

    def is_login_successful(self):
        return self.wait.until(EC.visibility_of_element_located(self.EDIT_ACCOUNT_INFO)).is_displayed()