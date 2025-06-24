from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.BuzzPage import BuzzPage


class DashboardPage:
    _BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    _TITLE_LOCATOR = ("xpath", "//h6[text()='Dashboard']")
    _BUZZ_LOCATOR = ("xpath", "//span[text()='Buzz']")


    def __init__(
        self, driver: WebDriver, wait_timeout: int = 15, wait_poll_frequency: int = 1
    ):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, wait_timeout, wait_poll_frequency)

    def go_dashboard_page(self):
        self._driver.get(self._BASE_URL)
        assert self.is_loaded, "На странице DashboardPage отсутствуют обязательные поля"

    def go_to_buzz(self):
        assert self.is_loaded
        self.buzz_btn.click()

        return BuzzPage(self._driver, 15,  1)

    @property
    def url(self) -> str:
        return self._BASE_URL

    @property
    def title(self) -> WebElement:
        return self._driver.find_element(*self._TITLE_LOCATOR)


    @property
    def buzz_btn(self) -> WebElement:
        return self._driver.find_element(*self._BUZZ_LOCATOR)

    @property
    def is_loaded(self) -> bool:
        try:
            self._wait.until(
                EC.visibility_of_element_located(self._TITLE_LOCATOR),
                message="Не дождались появления заголовка Dashboard",
            )
            self._wait.until(
                EC.visibility_of_element_located(self._BUZZ_LOCATOR),
                message="Не дождались появления кнопки Buzz",
            )
            return True
        except TimeoutException:
            return False
