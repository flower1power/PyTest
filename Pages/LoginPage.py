from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Pages.DashboardPage import DashboardPage


class LoginPage:
    _BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    _LOGIN_FIELD_LOCATOR = ("xpath", "//input[@name='username']")
    _PASSWORD_FIELD_LOCATOR = ("xpath", "//input[@name='password']")
    _LOGIN_BTN_LOCATOR = (
        "xpath",
        "//button[@type='submit' and normalize-space(.)='Login']",
    )
    _INVALID_CREDENTIAL_LOCATOR = (
        "xpath",
        "//div[@role='alert']//p[text()='Invalid credentials']",
    )

    def __init__(
        self, driver: WebDriver, wait_timeout: int = 15, wait_poll_frequency: int = 1
    ):
        self._driver = driver
        self._wait = WebDriverWait(
            self._driver, wait_timeout, poll_frequency=wait_poll_frequency
        )

    def go_auth_page(self):
        self._driver.get(self._BASE_URL)
        assert self.is_loaded, "На странице LoginPage отсутствуют обязательные поля"

    @property
    def url(self) -> str:
        return self._BASE_URL

    @property
    def login_field(self) -> WebElement:
        return self._driver.find_element(*self._LOGIN_FIELD_LOCATOR)

    @property
    def password_field(self) -> WebElement:
        return self._driver.find_element(*self._PASSWORD_FIELD_LOCATOR)

    @property
    def login_btn(self) -> WebElement:
        return self._driver.find_element(*self._LOGIN_BTN_LOCATOR)

    @property
    def is_invalid_credential(self) -> bool:
        try:
            self._wait.until(
                EC.visibility_of_element_located(self._INVALID_CREDENTIAL_LOCATOR),
                "Не дождались появления текста 'Invalid credentials'",
            )
            return True
        except TimeoutException:
            return False

    @property
    def is_loaded(self) -> bool:
        try:
            self._wait.until(
                EC.element_to_be_clickable(self._LOGIN_FIELD_LOCATOR),
                "Не дождались поля login",
            )
            self._wait.until(
                EC.element_to_be_clickable(self._PASSWORD_FIELD_LOCATOR),
                "Не дождались поля password",
            )
            self._wait.until(
                EC.element_to_be_clickable(self._LOGIN_BTN_LOCATOR),
                "Не дождались кнопки login",
            )
            return True
        except TimeoutException:
            return False

    def fill_auth_field(self, login: str, password: str):
        self.login_field.clear()
        self.login_field.send_keys(login)
        assert (
            self.login_field.get_attribute("value") == login
        ), "Неверное значение в поле логина"

        self.password_field.clear()
        self.password_field.send_keys(password)
        assert (
            self.password_field.get_attribute("value") == password
        ), "Неверное значение в поле пароля"

    def valid_auth(self, login: str, password: str) -> DashboardPage:
        self.fill_auth_field(login, password)

        self.login_btn.click()

        return DashboardPage(self._driver, 15,  1)

    def invalid_auth(self, login: str, password: str) -> bool:
        self.fill_auth_field(login, password)
        self.login_btn.click()

        assert (
            self.is_invalid_credential
        ), "Ожидали сообщение 'Invalid credentials', но оно не появилось"
        return True
