from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CompanyRegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        self.company_name = (By.ID, "representative-name")
        self.company_name_katakana = (By.ID, "representative-name-katakana")
        self.company_number = (By.ID, "corporate-number")
        self.company_email = (By.ID, "company-email")
        # self.industry = (By.ID, "company-industry-id")
        self.company_description = (By.ID, "company-description")
        self.company_logo = (By.XPATH, "//input[@type='file' and @id='company-logo']")
        self.company_banner = (By.XPATH, "//input[@type='file' and @id='company-banner']")
        self.postal_code = (By.ID, "postal-code")
        self.building_name = (By.ID, "building-name")
        self.website = (By.ID, "website-link")
        self.main_phone_number = (By.ID, "main-phone-number")
        self.next_button = (By.CSS_SELECTOR, "button[type='submit']")

        self.lastname = (By.NAME, "lastName")
        self.firstname = (By.NAME, "firstName")
        self.seiname = (By.NAME, "lastNamekatakana")
        self.meiname = (By.NAME, "firstNamekatakana")
        self.email = (By.NAME, "email")
        self.password = (By.NAME, "password")
        self.confirm_password = (By.NAME, "confirmPassword")
        self.phone_number = (By.NAME, "phone")
        self.profile_image = (By.ID, "user-avatar-input")
        self.company_tags = (By.ID, "companyTagsCategories")
        self.sub_tags = (By.ID, "tags")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")

        # self.toast_message = (By.CSS_SELECTOR, "div.Toastify__toast--success[role='alert']")
    # in page class
    def get_company_type_locator(self, value):
        return (By.XPATH, f"//input[@type='radio' and @name='companyType' and @value='{value}']")
    
    def select_industry(self, industry_name):
        # Step 1: Click the dropdown
        industry_dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "company-industry-id")))
        industry_dropdown.click()

        # Step 2: Wait for and click the correct list item
        option_xpath = f"//li[contains(text(), '{industry_name}')]"
        industry_option = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, option_xpath)))
        industry_option.click()
    
    def select_tags(self, company_tags, sub_tags):
        # Step 1: Click the company tags input
        company_tags_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.company_tags))
        company_tags_input.click()
        # Step 2: Enter the company tags
        
        company_tags_options = f"//li[contains(text(), '{company_tags}')]"
        first_suggestion = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, company_tags_options)))
        first_suggestion.click()

        # Step 4: Click the sub tags input
        sub_tags_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.sub_tags))
        sub_tags_input.click()
        
        sub_tags_options = f"//li[contains(text(), '{sub_tags}')]"
        first_sub_suggestion = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, sub_tags_options)))
        first_sub_suggestion.click()

    def company_information(self, company_type, company_name, company_name_katakana, company_number, company_email, industry, company_description, company_logo, company_banner, postal_code, building_name, website, main_phone_number):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.get_company_type_locator(company_type))).click()        

        # radio_button.click()
        self.driver.find_element(*self.company_name).send_keys(company_name)
        self.driver.find_element(*self.company_name_katakana).send_keys(company_name_katakana)
        self.driver.find_element(*self.company_number).send_keys(company_number)
        self.driver.find_element(*self.company_email).send_keys(company_email)
        self.select_industry(industry)

        self.driver.find_element(*self.company_description).send_keys(company_description)
        self.driver.find_element(*self.company_logo).send_keys(company_logo)
        self.driver.find_element(*self.company_banner).send_keys(company_banner)
        self.driver.find_element(*self.postal_code).send_keys(postal_code)
        self.driver.find_element(*self.building_name).send_keys(building_name)
        self.driver.find_element(*self.website).send_keys(website)
        self.driver.find_element(*self.main_phone_number).send_keys(main_phone_number)
        self.driver.find_element(*self.next_button).click()
        
        # Wait and check for validation error message
        try:
            error_locator = (By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error")
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(error_locator))
            errors = self.driver.find_elements(*error_locator)
            for e in errors:
                print("Validation Error:", e.text)
        except TimeoutException:
            print("No validation errors found")

    def create_account(self, lastname, firstname, seiname, meiname, email, password, confirm_password, phone_number, profile_image, company_tags, sub_tags):

        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.lastname)).send_keys(lastname)
        # self.driver.find_element(*self.lastname).send_keys(lastname)
        self.driver.find_element(*self.firstname).send_keys(firstname)
        self.driver.find_element(*self.seiname).send_keys(seiname)
        self.driver.find_element(*self.meiname).send_keys(meiname)
        self.driver.find_element(*self.email).send_keys(email)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.confirm_password).send_keys(confirm_password)
        self.driver.find_element(*self.phone_number).send_keys(phone_number)
        self.driver.find_element(*self.profile_image).send_keys(profile_image)
        self.select_tags(company_tags, sub_tags)
        # self.driver.find_element(*self.submit_button).click()

        try:
            error_locator = (By.CSS_SELECTOR, ".MuiFormHelperText-root.Mui-error")
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(error_locator))
            errors = self.driver.find_elements(*error_locator)
            for e in errors:
                print("Validation Error:", e.text)
        except TimeoutException:
            print("No validation errors found")

    def company_registered(self, company_name): #need to fix this
        try: 
            success = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.company_name))
            # Check if the success message contains the company name

            assert "登録が完了" in success.text

            # Navigate to the company list page to verify registration
            self.driver.get("https://willc.tai.com.np/admin/companies")

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{company_name}')]")))
            return True
        except:
            return False
        
    #delete not implemented
    # def delete_company(self, company_name):
    #     self.driver.get("https://willc.tai.com.np/admin/company/list")

    #     # Wait for table and find row
    #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    #     row = self.driver.find_element(By.XPATH, f"//tr[td[contains(text(), '{company_name}')]]")
    #     delete_btn = row.find_element(By.XPATH, ".//button[contains(@aria-label, '削除')]")  # adjust selector if needed
    #     delete_btn.click()

    #     # Confirm modal
    #     confirm_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '削除')]")))
    #     confirm_button.click()

    #     # Assert deletion
    #     WebDriverWait(self.driver, 5).until_not(EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{company_name}')]")))