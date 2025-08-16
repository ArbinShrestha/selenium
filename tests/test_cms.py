import pytest
from pages.login_page import LoginPage
from pages.cms_page import CMSPage
from utils.driver_setup import get_driver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()  # Load variables from .env

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

CMS_URL = "https://willc.tai.com.np/admin/login"
DASHBOARD_KEYWORD = "ダッシュボード"

@pytest.fixture
def setup():
    driver = get_driver()
    driver.get(CMS_URL)
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

def test_cms_navigation(logged_in_setup):
    """Test CMS navigation"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    assert cms.navigate_to_content_list()
    
    # Navigate to create content
    assert cms.navigate_to_create_content()

def test_content_creation_basic(logged_in_setup):
    """Test basic content creation"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to create content
    cms.navigate_to_create_content()
    
    # Create basic content
    test_title = "Test Content Basic"
    test_content = "This is a test content for basic creation."
    
    assert cms.create_content(
        title=test_title,
        content=test_content,
        status="draft"
    )
    
    # Save as draft
    assert cms.save_content(save_as_draft=True)

def test_content_creation_full(logged_in_setup):
    """Test full content creation with all fields"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to create content
    cms.navigate_to_create_content()
    
    # Create full content
    test_title = "Test Content Full"
    test_content = "This is a comprehensive test content with all fields filled."
    test_category = "General"
    test_tags = ["test", "automation", "selenium"]
    
    assert cms.create_content(
        title=test_title,
        content=test_content,
        category=test_category,
        status="published",
        publish_date="2024-12-31T12:00",
        tags=test_tags
    )
    
    # Save content
    assert cms.save_content(save_as_draft=False)

def test_content_editing(logged_in_setup):
    """Test content editing functionality"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Search for test content
    test_title = "Test Content"
    cms.search_content(test_title)
    
    # Edit content
    if cms.edit_content(test_title):
        # Update content
        updated_content = "This is updated test content."
        content_field = logged_in_setup.find_element(By.CSS_SELECTOR, ".ck-content")
        content_field.clear()
        content_field.send_keys(updated_content)
        
        # Save changes
        assert cms.save_content(save_as_draft=False)
    else:
        print(f"Content '{test_title}' not found for editing")

def test_content_deletion(logged_in_setup):
    """Test content deletion"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Search for test content to delete
    test_title = "Test Content Delete"
    cms.search_content(test_title)
    
    # Delete content
    if cms.delete_content(test_title):
        print(f"Successfully deleted content: {test_title}")
    else:
        print(f"Content '{test_title}' not found for deletion")

def test_content_search(logged_in_setup):
    """Test content search functionality"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Test search with different terms
    search_terms = ["Test", "Content", "Automation", "Selenium"]
    
    for term in search_terms:
        assert cms.search_content(term)
        print(f"Successfully searched for: '{term}'")

def test_content_filtering(logged_in_setup):
    """Test content filtering by status"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Test filtering by different statuses
    statuses = ["draft", "published", "archived"]
    
    for status in statuses:
        if cms.filter_content_by_status(status):
            print(f"Successfully filtered by status: {status}")
        else:
            print(f"Filter option for status '{status}' not available")

def test_content_preview(logged_in_setup):
    """Test content preview functionality"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Search for test content
    test_title = "Test Content"
    cms.search_content(test_title)
    
    # Preview content
    if cms.preview_content(test_title):
        print(f"Successfully previewed content: {test_title}")
    else:
        print(f"Content '{test_title}' not found for preview")

def test_content_details_retrieval(logged_in_setup):
    """Test retrieving content details"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Search for test content
    test_title = "Test Content"
    cms.search_content(test_title)
    
    # Get content details
    details = cms.get_content_details(test_title)
    if details:
        print(f"Content details: {details}")
        assert 'title' in details
        assert 'status' in details
    else:
        print(f"Content '{test_title}' not found")

def test_content_validation(logged_in_setup):
    """Test content validation"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to create content
    cms.navigate_to_create_content()
    
    # Try to save without required fields
    cms.save_content(save_as_draft=False)
    
    # Check for validation errors
    error_message = cms.get_error_message()
    if error_message:
        print(f"Validation error: {error_message}")
        assert "required" in error_message.lower() or "必須" in error_message

def test_content_categories(logged_in_setup):
    """Test content category selection"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to create content
    cms.navigate_to_create_content()
    
    # Test different categories
    categories = ["General", "News", "Announcement", "Guide"]
    
    for category in categories:
        if cms.select_category(category):
            print(f"Successfully selected category: {category}")
        else:
            print(f"Category '{category}' not available")

def test_content_status_selection(logged_in_setup):
    """Test content status selection"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to create content
    cms.navigate_to_create_content()
    
    # Test different statuses
    statuses = ["draft", "published", "archived"]
    
    for status in statuses:
        if cms.set_status(status):
            print(f"Successfully set status: {status}")
        else:
            print(f"Status '{status}' not available")

def test_content_tags_functionality(logged_in_setup):
    """Test content tags functionality"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to create content
    cms.navigate_to_create_content()
    
    # Test different tag formats
    tag_sets = [
        "single-tag",
        ["tag1", "tag2", "tag3"],
        "tag1, tag2, tag3",
        "日本語タグ, English Tag"
    ]
    
    for tags in tag_sets:
        if cms.add_tags(tags):
            print(f"Successfully added tags: {tags}")
        else:
            print(f"Failed to add tags: {tags}")

def test_cms_performance(logged_in_setup):
    """Test CMS performance"""
    cms = CMSPage(logged_in_setup)
    
    # Test content list load time
    import time
    start_time = time.time()
    cms.navigate_to_content_list()
    load_time = time.time() - start_time
    
    print(f"Content list load time: {load_time:.2f} seconds")
    assert load_time < 10, f"Content list took too long to load: {load_time:.2f} seconds"
    
    # Test content creation page load time
    start_time = time.time()
    cms.navigate_to_create_content()
    load_time = time.time() - start_time
    
    print(f"Content creation page load time: {load_time:.2f} seconds")
    assert load_time < 10, f"Content creation page took too long to load: {load_time:.2f} seconds"

def test_cms_error_handling(logged_in_setup):
    """Test CMS error handling"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Try to search for non-existent content
    cms.search_content("NonExistentContent12345")
    
    # Verify no errors occur
    assert cms.get_toast_message() is None or "error" not in cms.get_toast_message().lower()

def test_cms_navigation_consistency(logged_in_setup):
    """Test CMS navigation consistency"""
    cms = CMSPage(logged_in_setup)
    
    # Test multiple navigation paths
    assert cms.navigate_to_content_list()
    assert cms.navigate_to_create_content()
    
    # Verify we can navigate back to content list
    cms.navigate_to_content_list()

def test_cms_toast_messages(logged_in_setup):
    """Test CMS toast message handling"""
    cms = CMSPage(logged_in_setup)
    
    # Navigate to content list
    cms.navigate_to_content_list()
    
    # Get any existing toast message
    toast_message = cms.get_toast_message()
    if toast_message:
        print(f"Toast message: {toast_message}")
