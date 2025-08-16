from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class RolesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
        # Navigation elements
        self.roles_menu = (By.XPATH, "//a[contains(text(), 'ロール')]")
        self.roles_list_link = (By.XPATH, "//a[contains(text(), 'ロール一覧')]")
        self.create_role_button = (By.XPATH, "//button[contains(text(), '新規作成')]")
        
        # Role form elements
        self.role_name_input = (By.ID, "role-name")
        self.role_description_input = (By.ID, "role-description")
        self.permissions_checkboxes = (By.CSS_SELECTOR, "input[type='checkbox']")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.cancel_button = (By.XPATH, "//button[contains(text(), 'キャンセル')]")
        
        # Role list elements
        self.roles_table = (By.CSS_SELECTOR, "table")
        self.search_role_input = (By.CSS_SELECTOR, "input[placeholder*='検索']")
        self.filter_status_dropdown = (By.CSS_SELECTOR, "select")
        
        # Action buttons
        self.edit_role_button = (By.CSS_SELECTOR, "button[aria-label*='編集']")
        self.delete_role_button = (By.CSS_SELECTOR, "button[aria-label*='削除']")
        self.view_role_button = (By.CSS_SELECTOR, "button[aria-label*='表示']")
        self.assign_users_button = (By.CSS_SELECTOR, "button[aria-label*='ユーザー割り当て']")
        
        # Confirmation dialogs
        self.confirm_delete_button = (By.XPATH, "//button[contains(text(), '削除')]")
        self.confirm_assign_button = (By.XPATH, "//button[contains(text(), '割り当て')]")
        
        # User assignment elements
        self.user_checkboxes = (By.CSS_SELECTOR, "input[name='user']")
        self.select_all_users_checkbox = (By.CSS_SELECTOR, "input[name='select-all']")
        
        # Toast messages
        self.success_toast = (By.CSS_SELECTOR, "div.Toastify__toast--success[role='alert']")
        self.error_toast = (By.CSS_SELECTOR, "div.Toastify__toast--error[role='alert']")
    
    def navigate_to_roles_list(self):
        """Navigate to roles list page"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.roles_menu)).click()
            self.wait.until(EC.element_to_be_clickable(self.roles_list_link)).click()
            self.wait.until(EC.presence_of_element_located(self.roles_table))
            return True
        except TimeoutException:
            return False
    
    def navigate_to_create_role(self):
        """Navigate to role creation page"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.roles_menu)).click()
            self.wait.until(EC.element_to_be_clickable(self.create_role_button)).click()
            return True
        except TimeoutException:
            return False
    
    def create_role(self, role_name, description=None, permissions=None):
        """Create a new role"""
        try:
            # Fill role name
            name_field = self.wait.until(EC.element_to_be_clickable(self.role_name_input))
            name_field.clear()
            name_field.send_keys(role_name)
            
            # Fill description if provided
            if description:
                desc_field = self.driver.find_element(*self.role_description_input)
                desc_field.clear()
                desc_field.send_keys(description)
            
            # Select permissions if provided
            if permissions:
                self.select_permissions(permissions)
            
            return True
        except TimeoutException as e:
            print(f"Error creating role: {e}")
            return False
    
    def select_permissions(self, permissions):
        """Select permissions for the role"""
        try:
            if isinstance(permissions, list):
                for permission in permissions:
                    permission_checkbox = self.driver.find_element(
                        By.XPATH, f"//input[@type='checkbox' and @value='{permission}']"
                    )
                    if not permission_checkbox.is_selected():
                        permission_checkbox.click()
            return True
        except TimeoutException:
            return False
    
    def save_role(self):
        """Save the role"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()
            self.wait.until(EC.visibility_of_element_located(self.success_toast))
            return True
        except TimeoutException:
            return False
    
    def search_role(self, role_name):
        """Search for a role"""
        try:
            search_field = self.wait.until(EC.element_to_be_clickable(self.search_role_input))
            search_field.clear()
            search_field.send_keys(role_name)
            return True
        except TimeoutException:
            return False
    
    def find_role_in_table(self, role_name):
        """Find role row in the table"""
        try:
            role_row = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(text(), '{role_name}')]]"))
            )
            return role_row
        except TimeoutException:
            return None
    
    def edit_role(self, role_name):
        """Edit a role from the list"""
        try:
            role_row = self.find_role_in_table(role_name)
            if role_row:
                edit_btn = role_row.find_element(*self.edit_role_button)
                edit_btn.click()
                return True
            return False
        except TimeoutException:
            return False
    
    def delete_role(self, role_name):
        """Delete a role from the list"""
        try:
            role_row = self.find_role_in_table(role_name)
            if role_row:
                delete_btn = role_row.find_element(*self.delete_role_button)
                delete_btn.click()
                
                # Confirm deletion
                self.wait.until(EC.element_to_be_clickable(self.confirm_delete_button)).click()
                
                # Wait for success message
                self.wait.until(EC.visibility_of_element_located(self.success_toast))
                return True
            return False
        except TimeoutException:
            return False
    
    def view_role(self, role_name):
        """View role details"""
        try:
            role_row = self.find_role_in_table(role_name)
            if role_row:
                view_btn = role_row.find_element(*self.view_role_button)
                view_btn.click()
                return True
            return False
        except TimeoutException:
            return False
    
    def assign_users_to_role(self, role_name, user_emails=None, select_all=False):
        """Assign users to a role"""
        try:
            role_row = self.find_role_in_table(role_name)
            if role_row:
                assign_btn = role_row.find_element(*self.assign_users_button)
                assign_btn.click()
                
                if select_all:
                    # Select all users
                    select_all_checkbox = self.wait.until(
                        EC.element_to_be_clickable(self.select_all_users_checkbox)
                    )
                    if not select_all_checkbox.is_selected():
                        select_all_checkbox.click()
                elif user_emails:
                    # Select specific users
                    for email in user_emails:
                        user_checkbox = self.driver.find_element(
                            By.XPATH, f"//input[@type='checkbox' and @data-email='{email}']"
                        )
                        if not user_checkbox.is_selected():
                            user_checkbox.click()
                
                # Confirm assignment
                self.wait.until(EC.element_to_be_clickable(self.confirm_assign_button)).click()
                
                # Wait for success message
                self.wait.until(EC.visibility_of_element_located(self.success_toast))
                return True
            return False
        except TimeoutException:
            return False
    
    def filter_roles_by_status(self, status):
        """Filter roles by status"""
        try:
            filter_dropdown = self.wait.until(EC.element_to_be_clickable(self.filter_status_dropdown))
            filter_dropdown.click()
            
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//option[contains(text(), '{status}')]"))
            )
            option.click()
            return True
        except TimeoutException:
            return False
    
    def get_role_details(self, role_name):
        """Get role details from the table"""
        try:
            role_row = self.find_role_in_table(role_name)
            if role_row:
                cells = role_row.find_elements(By.TAG_NAME, "td")
                details = {
                    'name': cells[0].text if len(cells) > 0 else '',
                    'description': cells[1].text if len(cells) > 1 else '',
                    'permissions_count': cells[2].text if len(cells) > 2 else '',
                    'users_count': cells[3].text if len(cells) > 3 else '',
                    'created_date': cells[4].text if len(cells) > 4 else '',
                    'status': cells[5].text if len(cells) > 5 else ''
                }
                return details
            return None
        except TimeoutException:
            return None
    
    def get_role_permissions(self, role_name):
        """Get permissions for a specific role"""
        try:
            # Navigate to role details
            if self.view_role(role_name):
                permissions_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "input[type='checkbox']:checked"
                )
                permissions = [elem.get_attribute('value') for elem in permissions_elements]
                return permissions
            return []
        except TimeoutException:
            return []
    
    def get_assigned_users(self, role_name):
        """Get users assigned to a specific role"""
        try:
            # Navigate to role details
            if self.view_role(role_name):
                user_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "input[type='checkbox']:checked"
                )
                users = [elem.get_attribute('data-email') for elem in user_elements]
                return users
            return []
        except TimeoutException:
            return []
    
    def update_role_permissions(self, role_name, permissions):
        """Update permissions for an existing role"""
        try:
            if self.edit_role(role_name):
                # Clear existing permissions
                existing_permissions = self.driver.find_elements(
                    By.CSS_SELECTOR, "input[type='checkbox']:checked"
                )
                for permission in existing_permissions:
                    if permission.is_selected():
                        permission.click()
                
                # Select new permissions
                self.select_permissions(permissions)
                
                # Save changes
                return self.save_role()
            return False
        except TimeoutException:
            return False
    
    def get_toast_message(self):
        """Get the current toast message"""
        try:
            # Check for success toast first
            success_toast = self.wait.until(EC.visibility_of_element_located(self.success_toast))
            return success_toast.text.strip()
        except TimeoutException:
            try:
                # Check for error toast
                error_toast = self.wait.until(EC.visibility_of_element_located(self.error_toast))
                return error_toast.text.strip()
            except TimeoutException:
                return None
