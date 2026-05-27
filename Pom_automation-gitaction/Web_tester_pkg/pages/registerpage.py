from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class registerpage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Locators
    PERSONAL_DETAILS_LEGEND = (By.XPATH, '//*[@id="account"]/legend')
    FIRST_NAME = (By.ID, 'input-firstname')
    LAST_NAME = (By.ID, 'input-lastname')
    EMAIL = (By.ID, 'input-email')
    TELEPHONE = (By.ID, 'input-telephone')
    PASSWORD = (By.ID, 'input-password')
    CONFIRM_PASSWORD = (By.ID, 'input-confirm')
    SUBSCRIBE_NO = (By.XPATH, "//input[@name='newsletter' and @value='0']")
    AGREE_CHECK = (By.NAME, 'agree')
    CONTINUE_BTN = (By.XPATH, "//*[@id='content']/form/div/div/input[2]")
    WARNING_MSG = (By.XPATH, "//*[@id='account-register']/div[1]")

    # Actions
    def is_on_register_page(self):
        return "Your Personal Details" in self.wait.until(EC.presence_of_element_located(self.PERSONAL_DETAILS_LEGEND)).text

    def fill_registration_form(self, fname, lname, email, phone, password):
        self.wait.until(EC.presence_of_element_located(self.FIRST_NAME)).send_keys(fname)
        self.wait.until(EC.presence_of_element_located(self.LAST_NAME)).send_keys(lname)
        self.wait.until(EC.presence_of_element_located(self.EMAIL)).send_keys(email)
        self.wait.until(EC.presence_of_element_located(self.TELEPHONE)).send_keys(phone)
        self.wait.until(EC.presence_of_element_located(self.PASSWORD)).send_keys(password)
        self.wait.until(EC.presence_of_element_located(self.CONFIRM_PASSWORD)).send_keys(password)

    def submit_registration_expecting_failure(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBSCRIBE_NO)).click()
        self.wait.until(EC.element_to_be_clickable(self.AGREE_CHECK)).click()
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()
        return self

    def get_warning_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.WARNING_MSG)).text
    