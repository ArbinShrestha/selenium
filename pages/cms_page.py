from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class CMSPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
        # Content management elements
        self.content_menu = (By.XPATH, "//a[contains(text(), 'コンテンツ')]")
        self.create_content_button = (By.XPATH, "//button[contains(text(), '新規作成')]")
        self.content_list_link = (By.XPATH, "//a[contains(text(), 'コンテンツ一覧')]")
        
        # Content form elements
        self.title_input = (By.ID, "title")
        self.content_input = (By.CSS_SELECTOR, ".ck-content")
        self.category_dropdown = (By.ID, "category")
        self.status_radio = (By.NAME, "status")
        self.publish_date_input = (By.CSS_SELECTOR, "input[type='datetime-local']")
        self.featured_image_input = (By.CSS_SELECTOR, "input[type='file']")
        self.tags_input = (By.ID, "tags")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.save_draft_button = (By.XPATH, "//button[contains(text(), '下書き保存')]")
        
        # Content list elements
        self.content_table = (By.CSS_SELECTOR, "table")
        self.search_content_input = (By.CSS_SELECTOR, "input[placeholder*='検索']")
        self.filter_dropdown = (By.CSS_SELECTOR, "select")
        
        # Action buttons
        self.edit_content_button = (By.CSS_SELECTOR, "button[aria-label*='編集']")
        self.delete_content_button = (By.CSS_SELECTOR, "button[aria-label*='削除']")
        self.preview_content_button = (By.CSS_SELECTOR, "button[aria-label*='プレビュー']")
        
        # Confirmation dialogs
        self.confirm_delete_button = (By.XPATH, "//button[contains(text(), '削除')]")
        self.cancel_button = (By.XPATH, "//button[contains(text(), 'キャンセル')]")
        
        # Toast messages
        self.success_toast = (By.CSS_SELECTOR, "div.Toastify__toast--success[role='alert']")
        self.error_toast = (By.CSS_SELECTOR, "div.Toastify__toast--error[role='alert']")
    
    def navigate_to_content_list(self):
        """Navigate to content list page"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.content_menu)).click()
            self.wait.until(EC.element_to_be_clickable(self.content_list_link)).click()
            self.wait.until(EC.presence_of_element_located(self.content_table))
            return True
        except TimeoutException:
            return False
    
    def navigate_to_create_content(self):
        """Navigate to content creation page"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.content_menu)).click()
            self.wait.until(EC.element_to_be_clickable(self.create_content_button)).click()
            return True
        except TimeoutException:
            return False
    
    def create_content(self, title, content, category=None, status="draft", publish_date=None, 
                      featured_image=None, tags=None):
        """Create new content"""
        try:
            # Fill title
            title_field = self.wait.until(EC.element_to_be_clickable(self.title_input))
            title_field.clear()
            title_field.send_keys(title)
            
            # Fill content
            content_field = self.wait.until(EC.element_to_be_clickable(self.content_input))
            content_field.clear()
            content_field.send_keys(content)
            
            # Select category if provided
            if category:
                self.select_category(category)
            
            # Set status
            self.set_status(status)
            
            # Set publish date if provided
            if publish_date:
                date_field = self.driver.find_element(*self.publish_date_input)
                date_field.clear()
                date_field.send_keys(publish_date)
            
            # Upload featured image if provided
            if featured_image:
                image_field = self.driver.find_element(*self.featured_image_input)
                image_field.send_keys(featured_image)
            
            # Add tags if provided
            if tags:
                self.add_tags(tags)
            
            return True
        except TimeoutException as e:
            print(f"Error creating content: {e}")
            return False
    
    def select_category(self, category_name):
        """Select a category from dropdown"""
        try:
            dropdown = self.wait.until(EC.element_to_be_clickable(self.category_dropdown))
            dropdown.click()
            
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//option[contains(text(), '{category_name}')]"))
            )
            option.click()
            return True
        except TimeoutException:
            return False
    
    def set_status(self, status):
        """Set content status (draft, published, etc.)"""
        try:
            status_radio = self.driver.find_element(
                By.XPATH, f"//input[@type='radio' and @name='status' and @value='{status}']"
            )
            status_radio.click()
            return True
        except TimeoutException:
            return False
    
    def add_tags(self, tags):
        """Add tags to content"""
        try:
            if isinstance(tags, list):
                tags_text = ", ".join(tags)
            else:
                tags_text = tags
            
            tags_field = self.wait.until(EC.element_to_be_clickable(self.tags_input))
            tags_field.clear()
            tags_field.send_keys(tags_text)
            return True
        except TimeoutException:
            return False
    
    def save_content(self, save_as_draft=False):
        """Save content (as draft or publish)"""
        try:
            if save_as_draft:
                self.wait.until(EC.element_to_be_clickable(self.save_draft_button)).click()
            else:
                self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()
            
            # Wait for success message
            self.wait.until(EC.visibility_of_element_located(self.success_toast))
            return True
        except TimeoutException:
            return False
    
    def search_content(self, search_term):
        """Search for content"""
        try:
            search_field = self.wait.until(EC.element_to_be_clickable(self.search_content_input))
            search_field.clear()
            search_field.send_keys(search_term)
            return True
        except TimeoutException:
            return False
    
    def find_content_in_table(self, title):
        """Find content row in the table"""
        try:
            content_row = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(text(), '{title}')]]"))
            )
            return content_row
        except TimeoutException:
            return None
    
    def edit_content(self, title):
        """Edit content from the list"""
        try:
            content_row = self.find_content_in_table(title)
            if content_row:
                edit_btn = content_row.find_element(*self.edit_content_button)
                edit_btn.click()
                return True
            return False
        except TimeoutException:
            return False
    
    def delete_content(self, title):
        """Delete content from the list"""
        try:
            content_row = self.find_content_in_table(title)
            if content_row:
                delete_btn = content_row.find_element(*self.delete_content_button)
                delete_btn.click()
                
                # Confirm deletion
                self.wait.until(EC.element_to_be_clickable(self.confirm_delete_button)).click()
                
                # Wait for success message
                self.wait.until(EC.visibility_of_element_located(self.success_toast))
                return True
            return False
        except TimeoutException:
            return False
    
    def preview_content(self, title):
        """Preview content"""
        try:
            content_row = self.find_content_in_table(title)
            if content_row:
                preview_btn = content_row.find_element(*self.preview_content_button)
                preview_btn.click()
                return True
            return False
        except TimeoutException:
            return False
    
    def filter_content_by_status(self, status):
        """Filter content by status"""
        try:
            filter_dropdown = self.wait.until(EC.element_to_be_clickable(self.filter_dropdown))
            filter_dropdown.click()
            
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//option[contains(text(), '{status}')]"))
            )
            option.click()
            return True
        except TimeoutException:
            return False
    
    def get_content_details(self, title):
        """Get content details from the table"""
        try:
            content_row = self.find_content_in_table(title)
            if content_row:
                cells = content_row.find_elements(By.TAG_NAME, "td")
                details = {
                    'title': cells[0].text if len(cells) > 0 else '',
                    'category': cells[1].text if len(cells) > 1 else '',
                    'status': cells[2].text if len(cells) > 2 else '',
                    'created_date': cells[3].text if len(cells) > 3 else '',
                    'updated_date': cells[4].text if len(cells) > 4 else ''
                }
                return details
            return None
        except TimeoutException:
            return None
    
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
