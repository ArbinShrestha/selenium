import pytest
from pages.login_page import LoginPage
from utils.driver_setup import get_driver 
from pages.companyRegistration_page import CompanyRegistrationPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


REGISTRATION_URL = "https://willc.tai.com.np/admin/company/register"
COMPANY_REGISTRATION_KEYWORD = "会社情報登録"

@pytest.fixture
def setup():
    driver = get_driver()
    driver.get(REGISTRATION_URL)
    yield driver
    driver.quit()

def test_company_registration(setup):
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    registration = CompanyRegistrationPage(setup)
    
    # Fill in company information
    registration.company_information(
        company_type="corporate",
        company_name="Test Company 1",
        company_name_katakana="テストカンパニー",
        company_number="1234567890",
        company_email="companyemail@example.com",
        industry="IT",
        company_description="This is a test company.",
        company_logo="/path/to/logo.png",
        company_banner="/path/to/banner.png",
        postal_code="190-0001",
        building_name="Test Building",
        website="https://testcompany.com",
        main_phone_number="012345678911"
    )
    
