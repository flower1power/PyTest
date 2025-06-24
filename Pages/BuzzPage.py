from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BuzzPage:
    _BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/buzz/viewBuzz"
    _INPUT_TEXTAREA_LOCATOR = ("xpath", "//div[contains(@class, 'oxd-buzz-post--active')]//textarea[@class='oxd-buzz-post-input']")
    _POST_BTN_LOCATOR = ("xpath", "//div[contains(@class, 'oxd-buzz-post--active')]//button[@type='submit']")
    _NO_RECORDS_FOUND = ("xpath", "//div[@class='orangehrm-buzz-anniversary-nocontent']")

    def __init__(
        self, driver: WebDriver, wait_timeout: int = 15, wait_poll_frequency: int = 1
    ):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, wait_timeout, wait_poll_frequency)

    def go_buzz_page(self):
        self._driver.get(self._BASE_URL)
        assert self.is_loaded, "На странице BuzzPage отсутствуют обязательные поля"

    @property
    def url(self) -> str:
        return self._BASE_URL

    @property
    def input_textarea(self) -> WebElement:
        return self._driver.find_element(*self._INPUT_TEXTAREA_LOCATOR)

    @property
    def post_btn(self) -> WebElement:
        return self._driver.find_element(*self._POST_BTN_LOCATOR)

    @property
    def record_found(self) -> WebElement:
        return self._driver.find_element(*self._NO_RECORDS_FOUND)

    def public_post(self, post: str):
        self.input_textarea.send_keys(post)
        self.record_found.click()
        self.post_btn.click()

    def get_post_by_text(self, text: str) -> str:
        safe_snippet = text.strip()[:40].replace('"', '\\"')
        xpath = f'//div[@class="orangehrm-buzz-post-body"]/p[contains(normalize-space(.), "{safe_snippet}")]'

        post = self._wait.until(
            EC.visibility_of_element_located(("xpath", xpath))
        )

        return post.text.strip()

    def get_last_post(self) -> str:
        post = self._wait.until(
            EC.visibility_of_element_located(("xpath", f"(//div[@class='orangehrm-buzz-post-body']/p)[1]"))
        )

        return post.text.strip()


    @property
    def is_loaded(self) -> bool:
        try:
            self._wait.until(
                EC.visibility_of_element_located(self._INPUT_TEXTAREA_LOCATOR),
                message="Не дождались появления инпута для публикации поста",
            )
            self._wait.until(
                EC.visibility_of_element_located(self._POST_BTN_LOCATOR),
                message="Не дождались появления кнопки для публикации поста",
            )
            self._wait.until(
                EC.visibility_of_element_located(self._NO_RECORDS_FOUND),
                message="Не дождались появления фонда рекордов",
            )
            return True
        except TimeoutException:
            return False
