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
company_logo = os.path.abspath("images/test_logo.png")
company_banner = os.path.abspath("images/company_banner.jpg")
profile_image = os.path.abspath("images/profile_image.png")

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
        company_type="solo",
        company_name="Test Company 1",
        company_name_katakana="テストカンパニー",
        company_number="1234567890123",
        company_email="companyemail@example.com",
        industry="IT・ソフトウェア・情報処理・ゲーム",
        company_description="This is a test company.",
        company_logo=company_logo,
        company_banner=company_banner,
        postal_code="190-0001",
        building_name="Test Building",
        website="https://testcompany.com",
        main_phone_number="012345678911"
    )
    #create account
    registration.create_account(
        lastname="山田",
        firstname="太郎",
        seiname="ヤマダ",
        meiname="タロウ",
        email="yamada.taro@example.com",
        password="password123",
        confirm_password="password123",
        phone_number="012345678911",
        profile_image=profile_image,
        company_tags="Default Company Tag",
        sub_tags="Company tag 1"
    )
