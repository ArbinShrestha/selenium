import pytest
from utils.driver_setup import get_driver 
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

LOGIN_URL = "https://willc.tai.com.np/admin/login"
DASHBOARD_KEYWORD = "ダッシュボード"

@pytest.fixture
def setup():
    driver = get_driver()
    driver.get(LOGIN_URL)
    yield driver
    driver.quit()

def test_valid_login(setup):    
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    dashboard_element = WebDriverWait(setup, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(., 'ダッシュボード')]"))
)
    assert DASHBOARD_KEYWORD in dashboard_element.text

def test_invalid_login(setup):
    login = LoginPage(setup)
    login.login("invalid@domain.com", "wrongpassword")
    error_message = login.get_error_message()
    assert error_message in [
    "認証されていません。",
    "メールが必須です。",
    "パスワードは必須です"
]

def test_empty_login(setup):
    login = LoginPage(setup)
    login.login("", "somepassword")
    error_message = login.get_error_message()
    assert error_message in [
    "メールアドレスは必須です"
]

def test_empty_password(setup):
    login = LoginPage(setup)
    login.login("valid-email@domain.com", "")
    error_message = login.get_error_message()
    assert error_message in [
    "パスワードは必須です"
]

def test_logout(setup):
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    # Verify that the user is logged in by checking for the dashboard keyword
    WebDriverWait(setup, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{DASHBOARD_KEYWORD}')]")))
    # Perform logout
    login.logout()
    # Verify that the user is redirected to the login page after logout
    WebDriverWait(setup, 10).until(EC.url_contains(LOGIN_URL))
    assert False

    