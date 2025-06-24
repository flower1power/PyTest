import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from Pages.DashboardPage import DashboardPage
from Pages.LoginPage import LoginPage


@pytest.mark.usefixtures("setup_driver")
class TestJokes:
    dashboard_page: DashboardPage
    LOGIN = "Admin"
    PASSWORD = "admin123"
    driver: WebDriver


    def setup_method(self):
        self.driver = webdriver.Chrome(options=self.options)

        login_page = LoginPage(self.driver)
        login_page.go_auth_page()
        self.dashboard_page = login_page.valid_auth(self.LOGIN, self.PASSWORD)



    def test_post_joke(self, get_joke):
        joke = get_joke

        buzz_page = self.dashboard_page.go_to_buzz()
        assert buzz_page.is_loaded

        buzz_page.public_post(joke)
        text_post = buzz_page.get_post_by_text(joke)

        assert text_post == joke

    def teardown_method(self):
        self.driver.quit()