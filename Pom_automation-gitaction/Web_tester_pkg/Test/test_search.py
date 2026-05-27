import pytest
from Web_tester_pkg.pages.homepage import HomePage


class TestSearch:
    def test_search_for_a_valid_product(self, driver, wait, basepage):
        home = HomePage(driver, wait)
        home.search_for_product('HP')
        assert home.is_product_displayed()

    @pytest.mark.parametrize("search_term", ['InvalidProduct', ''])
    def test_search_no_results(self, driver, wait, basepage, search_term):
        home = HomePage(driver, wait)
        home.search_for_product(search_term)
        expected_message = "There is no product that matches the search criteria."
        assert home.get_no_product_message() == expected_message