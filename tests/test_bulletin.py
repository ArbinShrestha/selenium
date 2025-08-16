import pytest
from pages.login_page import LoginPage
from pages.bulletin_page import BulletinPage
from utils.driver_setup import get_driver
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

BULLETIN_URL = "https://willc.tai.com.np/admin/bulletin/create"
# BULLETIN_KEYWORD = "お知らせ"

@pytest.fixture
def setup():
    driver = get_driver()
    driver.get(BULLETIN_URL)
    yield driver
    driver.quit()

def test_bulletin_create(setup):
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    bulletin = BulletinPage(setup)

    bulletin.create_bulletin(
        title="Test Bulletin",
        designation="共通",
        status="public",
        publish__date="2023-10-01 12:00:00",
        description="This is a test description for the bulletin."
    )

    # Verify bulletin was created successfully
    assert bulletin.bulletin_created(title="Test Bulletin")

def test_bulletin_creation_with_different_statuses(setup):
    """Test bulletin creation with different statuses"""
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    bulletin = BulletinPage(setup)

    # Test with public status
    bulletin.create_bulletin(
        title="Test Bulletin Public",
        designation="共通",
        status="public",
        publish__date="2024-12-31 12:00:00",
        description="This is a public bulletin."
    )
    assert bulletin.bulletin_created(title="Test Bulletin Public")

def test_bulletin_creation_with_different_designations(setup):
    """Test bulletin creation with different designations"""
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    bulletin = BulletinPage(setup)

    # Test with different designation
    bulletin.create_bulletin(
        title="Test Bulletin Specific",
        designation="特定",
        status="public",
        publish__date="2024-12-31 12:00:00",
        description="This is a specific bulletin."
    )
    assert bulletin.bulletin_created(title="Test Bulletin Specific")

def test_bulletin_validation(setup):
    """Test bulletin validation"""
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    bulletin = BulletinPage(setup)

    # Try to create bulletin without required fields
    bulletin.create_bulletin(
        title="",
        designation="",
        status="public",
        publish__date="",
        description=""
    )

    # Check for validation errors
    error_message = bulletin.get_error_message()
    if error_message:
        print(f"Validation error: {error_message}")
        assert "required" in error_message.lower() or "必須" in error_message

def test_bulletin_creation_with_special_characters(setup):
    """Test bulletin creation with special characters"""
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    bulletin = BulletinPage(setup)

    bulletin.create_bulletin(
        title="Test Bulletin 特殊文字 @#$%",
        designation="共通",
        status="public",
        publish__date="2024-12-31 12:00:00",
        description="This is a bulletin with special characters: あいうえお"
    )
    assert bulletin.bulletin_created(title="Test Bulletin 特殊文字 @#$%")

def test_bulletin_creation_with_long_content(setup):
    """Test bulletin creation with long content"""
    login = LoginPage(setup)
    login.login(EMAIL, PASSWORD)
    bulletin = BulletinPage(setup)

    long_description = "This is a very long description for testing purposes. " * 20

    bulletin.create_bulletin(
        title="Test Bulletin Long Content",
        designation="共通",
        status="public",
        publish__date="2024-12-31 12:00:00",
        description=long_description
    )
    assert bulletin.bulletin_created(title="Test Bulletin Long Content")