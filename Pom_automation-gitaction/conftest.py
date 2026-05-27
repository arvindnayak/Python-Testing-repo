import sys
import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver

    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

@pytest.fixture
def basepage(driver):
    driver.get(r'https://tutorialsninja.com/demo/')
        
# Ensure the project root is in sys.path so 'Web_tester_pkg' can be imported
