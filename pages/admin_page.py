from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class AdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
        # Navigation elements
        self.dashboard_link = (By.XPATH, "//a[contains(text(), 'ダッシュボード')]")
        self.company_menu = (By.XPATH, "//a[contains(text(), '会社')]")
        self.bulletin_menu = (By.XPATH, "//a[contains(text(), 'お知らせ')]")
        self.user_menu = (By.XPATH, "//a[contains(text(), 'ユーザー')]")
        self.settings_menu = (By.XPATH, "//a[contains(text(), '設定')]")
        
        # Dashboard elements
        self.dashboard_title = (By.XPATH, "//h1[contains(text(), 'ダッシュボード')]")
        self.stats_cards = (By.CSS_SELECTOR, ".MuiCard-root")
        
        # Company list elements
        self.company_list_link = (By.XPATH, "//a[contains(text(), '会社一覧')]")
        self.company_table = (By.CSS_SELECTOR, "table")
        self.search_input = (By.CSS_SELECTOR, "input[placeholder*='検索']")
        self.add_company_button = (By.XPATH, "//button[contains(text(), '新規登録')]")
        
        # Pagination elements
        self.rows_per_page_dropdown = (By.CSS_SELECTOR, "div.MuiSelect-select")
        self.next_page_button = (By.CSS_SELECTOR, "button[aria-label='Next page']")
        self.previous_page_button = (By.CSS_SELECTOR, "button[aria-label='Previous page']")
        
        # Action buttons
        self.edit_button = (By.CSS_SELECTOR, "button[aria-label*='編集']")
        self.delete_button = (By.CSS_SELECTOR, "button[aria-label*='削除']")
        self.view_button = (By.CSS_SELECTOR, "button[aria-label*='表示']")
        
        # Confirmation dialogs
        self.confirm_delete_button = (By.XPATH, "//button[contains(text(), '削除')]")
        self.cancel_button = (By.XPATH, "//button[contains(text(), 'キャンセル')]")
        
        # Toast messages
        self.success_toast = (By.CSS_SELECTOR, "div.Toastify__toast--success[role='alert']")
        self.error_toast = (By.CSS_SELECTOR, "div.Toastify__toast--error[role='alert']")
    
    def navigate_to_dashboard(self):
        """Navigate to the admin dashboard"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.dashboard_link)).click()
            self.wait.until(EC.presence_of_element_located(self.dashboard_title))
            return True
        except TimeoutException:
            return False
    
    def navigate_to_company_list(self):
        """Navigate to company list page"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.company_menu)).click()
            self.wait.until(EC.element_to_be_clickable(self.company_list_link)).click()
            self.wait.until(EC.presence_of_element_located(self.company_table))
            return True
        except TimeoutException:
            return False
    
    def navigate_to_bulletin_create(self):
        """Navigate to bulletin creation page"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.bulletin_menu)).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '新規作成')]"))).click()
            return True
        except TimeoutException:
            return False
    
    def search_company(self, company_name):
        """Search for a company by name"""
        try:
            search_field = self.wait.until(EC.element_to_be_clickable(self.search_input))
            search_field.clear()
            search_field.send_keys(company_name)
            return True
        except TimeoutException:
            return False
    
    def find_company_in_table(self, company_name):
        """Find a company row in the table"""
        try:
            company_row = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(text(), '{company_name}')]]"))
            )
            return company_row
        except TimeoutException:
            return None
    
    def edit_company(self, company_name):
        """Edit a company from the list"""
        try:
            company_row = self.find_company_in_table(company_name)
            if company_row:
                edit_btn = company_row.find_element(*self.edit_button)
                edit_btn.click()
                return True
            return False
        except TimeoutException:
            return False
    
    def delete_company(self, company_name):
        """Delete a company from the list"""
        try:
            company_row = self.find_company_in_table(company_name)
            if company_row:
                delete_btn = company_row.find_element(*self.delete_button)
                delete_btn.click()
                
                # Confirm deletion
                self.wait.until(EC.element_to_be_clickable(self.confirm_delete_button)).click()
                
                # Wait for success message
                self.wait.until(EC.visibility_of_element_located(self.success_toast))
                return True
            return False
        except TimeoutException:
            return False
    
    def set_rows_per_page(self, value="50"):
        """Set the number of rows per page in the table"""
        try:
            dropdown = self.wait.until(EC.element_to_be_clickable(self.rows_per_page_dropdown))
            dropdown.click()
            
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//li[@data-value='{value}']"))
            )
            option.click()
            return True
        except TimeoutException:
            return False
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        try:
            stats_cards = self.driver.find_elements(*self.stats_cards)
            stats = {}
            for card in stats_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h6").text
                    value = card.find_element(By.CSS_SELECTOR, "h4").text
                    stats[title] = value
                except:
                    continue
            return stats
        except TimeoutException:
            return {}
    
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
    
    def wait_for_page_load(self):
        """Wait for the page to fully load"""
        try:
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            return True
        except TimeoutException:
            return False
