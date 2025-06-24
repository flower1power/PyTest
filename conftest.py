import pytest
import requests
from selenium import webdriver


@pytest.fixture()
def get_joke():
    response = requests.get("https://geek-jokes.sameerkumar.website/api")
    return response.text.strip().replace('"', '')

@pytest.fixture(scope="class")
def setup_driver(request):
    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    request.cls.options = options
