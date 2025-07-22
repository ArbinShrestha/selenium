from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.email_input =  (By.ID, "email")
        self.password_input = (By.ID, "password")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.logout_button = (By.CSS_SELECTOR,".MuiSvgIcon-root.MuiSvgIcon-fontSizeMedium.css-vwctsu")
        self.logout_confirm_button = (By.XPATH, "//button[normalize-space(text())='確認']")
        self.toast_error_selector = (By.CSS_SELECTOR, "div.Toastify__toast--error[role='alert']")
        self.inline_error_selector = (By.CSS_SELECTOR, "div.error-message")

    def login(self, email, password):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.email_input)).clear()
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.submit_button).click()

    def logout(self):
        WebDriverWait(self.driver, 5).until((EC.element_to_be_clickable(self.logout_button))).click()
        WebDriverWait(self.driver, 5).until((EC.element_to_be_clickable(self.logout_confirm_button))).click()

    def get_error_message(self):
        
        try:
            # 1. Check for toast message
            toast = self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.Toastify__toast--error[role='alert']")))
            return toast.text.strip()
        except TimeoutException:
            pass  # Continue to check inline errors

        try:
            # 2. Check for email required inline error
            email_error = self.driver.find_element(By.ID, "email-helper-text")
            if email_error.is_displayed():
                return email_error.text.strip()
        except:
            pass

        try:
            # 3. Check for password required inline error
            password_error = self.driver.find_element(By.ID, "password-helper-text")
            if password_error.is_displayed():
                return password_error.text.strip()
        except:
            pass

        try:
            # 4. Generic inline fallback for messages like 認証されていません or Invalid
            inline_error = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'認証されていません') or contains(text(),'Invalid')]")))
            return inline_error.text.strip()
        except TimeoutException:
            return "Error message not found"
