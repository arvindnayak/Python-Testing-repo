from Web_tester_pkg.pages.homepage import HomePage

class TestRegister:
    def test_register_duplicate_email(self, driver, wait, basepage):
        
        # 1. Start on the Home Page and fluently navigate to the Register Page
        home = HomePage(driver, wait)
        home.click_account_dropdown()
        register_page = home.click_register_link()
        
        # 2. Perform the Registration steps
        assert register_page.is_on_register_page()
        register_page.fill_registration_form('Arvind', 'Singh', '1234567jaga1234@gmail.com', '1234567890', 'Arvind@123')
        register_page.submit_registration_expecting_failure()
        
        # 3. Assert the expected outcome
        assert "Warning: E-Mail Address is already registered!" in register_page.get_warning_message()
