import pytest
from pages.login_page import LoginPage
from pages.admin_page import AdminPage
from utils.driver_setup import get_driver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()  # Load variables from .env

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

ADMIN_URL = "https://willc.tai.com.np/admin/login"
DASHBOARD_KEYWORD = "ダッシュボード"

@pytest.fixture
def setup():
    driver = get_driver()
    driver.get(ADMIN_URL)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_setup(setup):
    """Setup with logged in user"""
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    # Verify login successful
    WebDriverWait(setup, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{DASHBOARD_KEYWORD}')]"))
    )
    yield setup

def test_admin_dashboard_navigation(logged_in_setup):
    """Test admin dashboard navigation"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to dashboard
    assert admin.navigate_to_dashboard()
    
    # Get dashboard stats
    stats = admin.get_dashboard_stats()
    assert isinstance(stats, dict)
    print(f"Dashboard stats: {stats}")

def test_company_list_navigation(logged_in_setup):
    """Test navigation to company list"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to company list
    assert admin.navigate_to_company_list()
    
    # Verify table is present
    assert admin.wait_for_page_load()

def test_company_search(logged_in_setup):
    """Test company search functionality"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to company list
    admin.navigate_to_company_list()
    
    # Search for a company
    test_company = "Test Company"
    assert admin.search_company(test_company)
    
    # Verify search results
    company_row = admin.find_company_in_table(test_company)
    if company_row:
        print(f"Found company: {test_company}")
    else:
        print(f"Company {test_company} not found in search results")

def test_company_management_operations(logged_in_setup):
    """Test company management operations"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to company list
    admin.navigate_to_company_list()
    
    # Set rows per page
    assert admin.set_rows_per_page("25")
    
    # Test pagination (if available)
    try:
        next_page = logged_in_setup.find_element(By.CSS_SELECTOR, "button[aria-label='Next page']")
        if next_page.is_enabled():
            next_page.click()
            print("Successfully navigated to next page")
    except:
        print("Pagination not available or only one page")

def test_bulletin_navigation(logged_in_setup):
    """Test bulletin creation navigation"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to bulletin create
    assert admin.navigate_to_bulletin_create()
    
    # Verify we're on the bulletin creation page
    assert "bulletin" in logged_in_setup.current_url.lower()

def test_admin_toast_messages(logged_in_setup):
    """Test admin toast message handling"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to dashboard
    admin.navigate_to_dashboard()
    
    # Get any existing toast message
    toast_message = admin.get_toast_message()
    if toast_message:
        print(f"Toast message: {toast_message}")

def test_admin_page_load_performance(logged_in_setup):
    """Test admin page load performance"""
    admin = AdminPage(logged_in_setup)
    
    # Test dashboard load time
    import time
    start_time = time.time()
    admin.navigate_to_dashboard()
    load_time = time.time() - start_time
    
    print(f"Dashboard load time: {load_time:.2f} seconds")
    assert load_time < 10, f"Dashboard took too long to load: {load_time:.2f} seconds"
    
    # Test company list load time
    start_time = time.time()
    admin.navigate_to_company_list()
    load_time = time.time() - start_time
    
    print(f"Company list load time: {load_time:.2f} seconds")
    assert load_time < 10, f"Company list took too long to load: {load_time:.2f} seconds"

def test_admin_error_handling(logged_in_setup):
    """Test admin error handling"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to company list
    admin.navigate_to_company_list()
    
    # Try to search for non-existent company
    admin.search_company("NonExistentCompany12345")
    
    # Verify no errors occur
    assert admin.wait_for_page_load()

def test_admin_navigation_consistency(logged_in_setup):
    """Test admin navigation consistency"""
    admin = AdminPage(logged_in_setup)
    
    # Test multiple navigation paths
    assert admin.navigate_to_dashboard()
    assert admin.navigate_to_company_list()
    assert admin.navigate_to_bulletin_create()
    
    # Verify we can always get back to dashboard
    assert admin.navigate_to_dashboard()

def test_admin_table_functionality(logged_in_setup):
    """Test admin table functionality"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to company list
    admin.navigate_to_company_list()
    
    # Test different rows per page settings
    for rows in ["10", "25", "50"]:
        assert admin.set_rows_per_page(rows)
        print(f"Successfully set rows per page to {rows}")

def test_admin_search_functionality(logged_in_setup):
    """Test admin search functionality with various inputs"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to company list
    admin.navigate_to_company_list()
    
    # Test search with different inputs
    search_terms = ["", "Test", "Company", "123", "あいうえお"]
    
    for term in search_terms:
        assert admin.search_company(term)
        print(f"Successfully searched for: '{term}'")

def test_admin_page_elements_presence(logged_in_setup):
    """Test that all admin page elements are present"""
    admin = AdminPage(logged_in_setup)
    
    # Navigate to dashboard
    admin.navigate_to_dashboard()
    
    # Check for essential elements
    assert logged_in_setup.find_element(By.XPATH, "//*[contains(text(), 'ダッシュボード')]")
    
    # Navigate to company list
    admin.navigate_to_company_list()
    
    # Check for table presence
    assert logged_in_setup.find_element(By.CSS_SELECTOR, "table")
