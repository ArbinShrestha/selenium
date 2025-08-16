import pytest
import os
from dotenv import load_dotenv
from utils.driver_setup import get_driver

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application"""
    return "https://willc.tai.com.np"

@pytest.fixture(scope="session")
def admin_credentials():
    """Admin credentials from environment variables"""
    return {
        "email": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD")
    }

@pytest.fixture(scope="function")
def driver():
    """WebDriver fixture for each test"""
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver, admin_credentials):
    """WebDriver fixture with logged in user"""
    from pages.login_page import LoginPage
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Navigate to login page
    driver.get("https://willc.tai.com.np/admin/login")
    
    # Login
    login_page = LoginPage(driver)
    login_page.login(admin_credentials["email"], admin_credentials["password"])
    
    # Verify login successful
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ダッシュボード')]"))
    )
    
    yield driver

@pytest.fixture(scope="function")
def test_data():
    """Test data for various test scenarios"""
    return {
        "company": {
            "name": "Test Company Automation",
            "name_katakana": "テストカンパニーオートメーション",
            "number": "1234567890123",
            "email": "testcompany@example.com",
            "industry": "IT・ソフトウェア・情報処理・ゲーム",
            "description": "This is a test company for automation testing.",
            "postal_code": "100-0001",
            "building_name": "Test Building",
            "website": "https://testcompany.com",
            "phone": "01234567890"
        },
        "user": {
            "lastname": "山田",
            "firstname": "太郎",
            "lastname_katakana": "ヤマダ",
            "firstname_katakana": "タロウ",
            "email": "yamada.taro@example.com",
            "password": "password123",
            "phone": "09012345678"
        },
        "bulletin": {
            "title": "Test Bulletin Automation",
            "designation": "共通",
            "status": "public",
            "publish_date": "2024-12-31 12:00:00",
            "description": "This is a test bulletin for automation testing."
        },
        "content": {
            "title": "Test Content Automation",
            "content": "This is test content for automation testing.",
            "category": "General",
            "status": "draft",
            "tags": ["test", "automation", "selenium"]
        },
        "role": {
            "name": "Test Role Automation",
            "description": "This is a test role for automation testing.",
            "permissions": ["read", "write", "delete"]
        }
    }

@pytest.fixture(scope="function")
def image_paths():
    """Paths to test images"""
    return {
        "company_logo": os.path.abspath("images/test_logo.png"),
        "company_banner": os.path.abspath("images/company_banner.jpg"),
        "profile_image": os.path.abspath("images/profile_image.png")
    }

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "login: mark test as login related"
    )
    config.addinivalue_line(
        "markers", "company: mark test as company related"
    )
    config.addinivalue_line(
        "markers", "bulletin: mark test as bulletin related"
    )
    config.addinivalue_line(
        "markers", "admin: mark test as admin related"
    )
    config.addinivalue_line(
        "markers", "cms: mark test as CMS related"
    )
    config.addinivalue_line(
        "markers", "roles: mark test as roles related"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names"""
    for item in items:
        # Add smoke marker to basic functionality tests
        if any(keyword in item.name.lower() for keyword in ["login", "basic", "navigation"]):
            item.add_marker(pytest.mark.smoke)
        
        # Add specific markers based on test names
        if "login" in item.name.lower():
            item.add_marker(pytest.mark.login)
        elif "company" in item.name.lower():
            item.add_marker(pytest.mark.company)
        elif "bulletin" in item.name.lower():
            item.add_marker(pytest.mark.bulletin)
        elif "admin" in item.name.lower():
            item.add_marker(pytest.mark.admin)
        elif "cms" in item.name.lower():
            item.add_marker(pytest.mark.cms)
        elif "role" in item.name.lower():
            item.add_marker(pytest.mark.roles)
        
        # Add regression marker to all tests
        item.add_marker(pytest.mark.regression)
