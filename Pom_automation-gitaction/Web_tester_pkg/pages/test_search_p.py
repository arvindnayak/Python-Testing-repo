from Web_tester_pkg.pages.homepage import HomePage


def test_search_for_a_valid_product(driver, wait, basepage):
    driver.maximize_window()
    home = HomePage(driver, wait)
    home.search_for_product('HP')
    assert home.is_product_displayed()

def test_search_for_an_invalid_product(driver, wait, basepage):
    driver.maximize_window()
    home = HomePage(driver, wait)
    home.search_for_product('InvalidProduct')
    expected_message = "There is no product that matches the search criteria."
    assert home.get_no_product_message() == expected_message

def test_search_with_empty_input(driver, wait, basepage):
    driver.maximize_window()
    home = HomePage(driver, wait)
    home.search_for_product('')
    expected_message = "There is no product that matches the search criteria."
    assert home.get_no_product_message() == expected_message