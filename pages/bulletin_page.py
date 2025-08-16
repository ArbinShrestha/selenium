from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BulletinPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.title = (By.ID, "title")
        self.designation = (By.ID, "designation")
        self.publish__date = (By.CSS_SELECTOR, ".MuiInputBase-input.MuiFilledInput-input.MuiInputBase-inputAdornedEnd")
        self.description = (By.CSS_SELECTOR, ".ck-blurred ck.ck-content")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")
    
    def get_status(self, value):
        return (By.XPATH, f"//input[@type='radio' and @name='status' and @value='{value}']")
    
    def create_bulletin(self, title, status, designation, publish__date, description):
        """Create a new bulletin"""
        try:
            # Fill title
            title_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.title))
            title_field.clear()
            title_field.send_keys(title)
            
            # Fill designation
            designation_field = self.driver.find_element(*self.designation)
            designation_field.clear()
            designation_field.send_keys(designation)
            
            # Set status
            status_radio = self.driver.find_element(*self.get_status(status))
            status_radio.click()
            
            # Set publish date
            date_field = self.driver.find_element(*self.publish__date)
            date_field.clear()
            date_field.send_keys(publish__date)
            
            # Fill description
            desc_field = self.driver.find_element(*self.description)
            desc_field.clear()
            desc_field.send_keys(description)
            
            # Submit
            self.driver.find_element(*self.submit_button).click()
            
            return True
        except TimeoutException as e:
            print(f"Error creating bulletin: {e}")
            return False
    
    def bulletin_created(self, title):
        """Verify bulletin was created successfully"""
        try:
            # Wait for success message
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'お知らせが正常に作成されました')]"))
            )
            
            # Check for bulletin title on confirmation screen
            title_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//h5[contains(text(), '{title}')]"))
            )
            
            actual_title = title_element.text.strip()
            assert title in actual_title, f"Expected bulletin title '{title}' not found. Got: '{actual_title}'"
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not confirm bulletin creation: {e}")
            return False
    
    def get_error_message(self):
        """Get error message if any"""
        try:
            # Check for toast message
            toast = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.Toastify__toast--error[role='alert']")))
            return toast.text.strip()
        except TimeoutException:
            pass

        try:
            error_locator = (By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error")
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(error_locator))
            errors = self.driver.find_elements(*error_locator)
            for e in errors:
                print("Validation Error:", e.text)
        except TimeoutException:
            print("No validation errors found")
    
