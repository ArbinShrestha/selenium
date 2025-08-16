import pytest
from pages.login_page import LoginPage
from pages.roles_page import RolesPage
from utils.driver_setup import get_driver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()  # Load variables from .env

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

ROLES_URL = "https://willc.tai.com.np/admin/login"
DASHBOARD_KEYWORD = "ダッシュボード"

@pytest.fixture
def setup():
    driver = get_driver()
    driver.get(ROLES_URL)
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

def test_roles_navigation(logged_in_setup):
    """Test roles navigation"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    assert roles.navigate_to_roles_list()
    
    # Navigate to create role
    assert roles.navigate_to_create_role()

def test_role_creation_basic(logged_in_setup):
    """Test basic role creation"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to create role
    roles.navigate_to_create_role()
    
    # Create basic role
    test_role_name = "Test Role Basic"
    test_description = "This is a basic test role."
    
    assert roles.create_role(
        role_name=test_role_name,
        description=test_description
    )
    
    # Save role
    assert roles.save_role()

def test_role_creation_with_permissions(logged_in_setup):
    """Test role creation with permissions"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to create role
    roles.navigate_to_create_role()
    
    # Create role with permissions
    test_role_name = "Test Role With Permissions"
    test_description = "This is a test role with specific permissions."
    test_permissions = ["read", "write", "delete"]
    
    assert roles.create_role(
        role_name=test_role_name,
        description=test_description,
        permissions=test_permissions
    )
    
    # Save role
    assert roles.save_role()

def test_role_editing(logged_in_setup):
    """Test role editing functionality"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # Edit role
    if roles.edit_role(test_role_name):
        # Update role description
        updated_description = "This is an updated test role description."
        desc_field = logged_in_setup.find_element(By.ID, "role-description")
        desc_field.clear()
        desc_field.send_keys(updated_description)
        
        # Save changes
        assert roles.save_role()
    else:
        print(f"Role '{test_role_name}' not found for editing")

def test_role_deletion(logged_in_setup):
    """Test role deletion"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role to delete
    test_role_name = "Test Role Delete"
    roles.search_role(test_role_name)
    
    # Delete role
    if roles.delete_role(test_role_name):
        print(f"Successfully deleted role: {test_role_name}")
    else:
        print(f"Role '{test_role_name}' not found for deletion")

def test_role_search(logged_in_setup):
    """Test role search functionality"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Test search with different terms
    search_terms = ["Test", "Role", "Admin", "User"]
    
    for term in search_terms:
        assert roles.search_role(term)
        print(f"Successfully searched for: '{term}'")

def test_role_filtering(logged_in_setup):
    """Test role filtering by status"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Test filtering by different statuses
    statuses = ["active", "inactive", "archived"]
    
    for status in statuses:
        if roles.filter_roles_by_status(status):
            print(f"Successfully filtered by status: {status}")
        else:
            print(f"Filter option for status '{status}' not available")

def test_role_viewing(logged_in_setup):
    """Test role viewing functionality"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # View role
    if roles.view_role(test_role_name):
        print(f"Successfully viewed role: {test_role_name}")
    else:
        print(f"Role '{test_role_name}' not found for viewing")

def test_user_assignment_to_role(logged_in_setup):
    """Test assigning users to a role"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # Assign users to role
    test_user_emails = ["user1@example.com", "user2@example.com"]
    
    if roles.assign_users_to_role(test_role_name, user_emails=test_user_emails):
        print(f"Successfully assigned users to role: {test_role_name}")
    else:
        print(f"Role '{test_role_name}' not found for user assignment")

def test_select_all_users_assignment(logged_in_setup):
    """Test assigning all users to a role"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # Assign all users to role
    if roles.assign_users_to_role(test_role_name, select_all=True):
        print(f"Successfully assigned all users to role: {test_role_name}")
    else:
        print(f"Role '{test_role_name}' not found for user assignment")

def test_role_details_retrieval(logged_in_setup):
    """Test retrieving role details"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # Get role details
    details = roles.get_role_details(test_role_name)
    if details:
        print(f"Role details: {details}")
        assert 'name' in details
        assert 'description' in details
    else:
        print(f"Role '{test_role_name}' not found")

def test_role_permissions_retrieval(logged_in_setup):
    """Test retrieving role permissions"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # Get role permissions
    permissions = roles.get_role_permissions(test_role_name)
    if permissions:
        print(f"Role permissions: {permissions}")
        assert isinstance(permissions, list)
    else:
        print(f"Role '{test_role_name}' not found or no permissions")

def test_assigned_users_retrieval(logged_in_setup):
    """Test retrieving users assigned to a role"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # Get assigned users
    users = roles.get_assigned_users(test_role_name)
    if users:
        print(f"Assigned users: {users}")
        assert isinstance(users, list)
    else:
        print(f"Role '{test_role_name}' not found or no assigned users")

def test_role_permissions_update(logged_in_setup):
    """Test updating role permissions"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Search for test role
    test_role_name = "Test Role"
    roles.search_role(test_role_name)
    
    # Update permissions
    new_permissions = ["read", "write", "admin"]
    
    if roles.update_role_permissions(test_role_name, new_permissions):
        print(f"Successfully updated permissions for role: {test_role_name}")
    else:
        print(f"Role '{test_role_name}' not found for permission update")

def test_role_validation(logged_in_setup):
    """Test role validation"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to create role
    roles.navigate_to_create_role()
    
    # Try to save without required fields
    roles.save_role()
    
    # Check for validation errors
    error_message = roles.get_toast_message()
    if error_message:
        print(f"Validation error: {error_message}")
        assert "required" in error_message.lower() or "必須" in error_message

def test_permission_selection(logged_in_setup):
    """Test permission selection functionality"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to create role
    roles.navigate_to_create_role()
    
    # Test different permission sets
    permission_sets = [
        ["read"],
        ["read", "write"],
        ["read", "write", "delete"],
        ["admin", "user_management", "content_management"]
    ]
    
    for permissions in permission_sets:
        if roles.select_permissions(permissions):
            print(f"Successfully selected permissions: {permissions}")
        else:
            print(f"Failed to select permissions: {permissions}")

def test_roles_performance(logged_in_setup):
    """Test roles performance"""
    roles = RolesPage(logged_in_setup)
    
    # Test roles list load time
    import time
    start_time = time.time()
    roles.navigate_to_roles_list()
    load_time = time.time() - start_time
    
    print(f"Roles list load time: {load_time:.2f} seconds")
    assert load_time < 10, f"Roles list took too long to load: {load_time:.2f} seconds"
    
    # Test role creation page load time
    start_time = time.time()
    roles.navigate_to_create_role()
    load_time = time.time() - start_time
    
    print(f"Role creation page load time: {load_time:.2f} seconds")
    assert load_time < 10, f"Role creation page took too long to load: {load_time:.2f} seconds"

def test_roles_error_handling(logged_in_setup):
    """Test roles error handling"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Try to search for non-existent role
    roles.search_role("NonExistentRole12345")
    
    # Verify no errors occur
    assert roles.get_toast_message() is None or "error" not in roles.get_toast_message().lower()

def test_roles_navigation_consistency(logged_in_setup):
    """Test roles navigation consistency"""
    roles = RolesPage(logged_in_setup)
    
    # Test multiple navigation paths
    assert roles.navigate_to_roles_list()
    assert roles.navigate_to_create_role()
    
    # Verify we can navigate back to roles list
    roles.navigate_to_roles_list()

def test_roles_toast_messages(logged_in_setup):
    """Test roles toast message handling"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to roles list
    roles.navigate_to_roles_list()
    
    # Get any existing toast message
    toast_message = roles.get_toast_message()
    if toast_message:
        print(f"Toast message: {toast_message}")

def test_role_creation_with_special_characters(logged_in_setup):
    """Test role creation with special characters"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to create role
    roles.navigate_to_create_role()
    
    # Create role with special characters
    test_role_name = "Test Role 特殊文字 @#$%"
    test_description = "This is a test role with special characters: あいうえお"
    
    assert roles.create_role(
        role_name=test_role_name,
        description=test_description
    )
    
    # Save role
    assert roles.save_role()

def test_role_creation_with_long_text(logged_in_setup):
    """Test role creation with long text"""
    roles = RolesPage(logged_in_setup)
    
    # Navigate to create role
    roles.navigate_to_create_role()
    
    # Create role with long description
    test_role_name = "Test Role Long"
    test_description = "This is a very long description for testing purposes. " * 10
    
    assert roles.create_role(
        role_name=test_role_name,
        description=test_description
    )
    
    # Save role
    assert roles.save_role()
