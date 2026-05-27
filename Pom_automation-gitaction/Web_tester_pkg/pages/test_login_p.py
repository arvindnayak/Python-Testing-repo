import pytest
from Web_tester_pkg.pages.homepage import HomePage

def test_login_with_valid_credentials(driver, wait, basepage):
    driver.maximize_window()
    home = HomePage(driver, wait)
    home.click_account_dropdown()
    login_page = home.click_login_link()
    
    login_page.login('1234567jaga1234@gmail.com', 'Arvind@123')
    assert login_page.is_login_successful()

@pytest.mark.parametrize("email, password", [
    ('1234567jaga1234@gmail.com', 'Arvidsfdsfg'),       # Invalid password
    ('12345sdfgh67jaga1234@gmail.com', 'Arvind@123'),   # Invalid email
    ('', '')                                            # Empty credentials
])
def test_login_with_invalid_credentials(driver, wait, basepage, email, password):
    driver.maximize_window()
    home = HomePage(driver, wait)
    home.click_account_dropdown()
    login_page = home.click_login_link()
    
    login_page.login(email, password)
    assert "Warning: No match for E-Mail Address and/or Password." in login_page.get_warning_message()
