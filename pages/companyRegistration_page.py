from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CompanyRegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        # self.company_type = (By.XPATH, "//input[@type='radio' and @name='companyType' and @value='{}']")
        self.company_name = (By.ID, "representative-name")
        self.company_name_katakana = (By.ID, "representative-name-katakana")
        self.company_number = (By.ID, "corporate-number")
        self.company_email = (By.ID, "company-email")
        self.industry = (By.ID, "company-industry-id")
        self.company_description = (By.ID, "company-description")
        # self.company_logo = (By.XPATH, "//*[contains(text(),'会社のロゴを選択')]")
        # self.company_banner = (By.XPATH, "//*[contains(text(),'会社のバナーを選択')]")
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
    # in page class
    def get_company_type_locator(self, value):
        return (By.XPATH, f"//input[@type='radio' and @name='companyType' and @value='{value}']")
    

    def company_information(self, company_type, company_name, company_name_katakana, company_number, company_email, industry, company_description, company_logo, company_banner, postal_code, building_name, website, main_phone_number):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.get_company_type_locator(company_type))).click()        

        # radio_button.click()
        self.driver.find_element(*self.company_name).send_keys(company_name)
        self.driver.find_element(*self.company_name_katakana).send_keys(company_name_katakana)
        self.driver.find_element(*self.company_number).send_keys(company_number)
        self.driver.find_element(*self.company_email).send_keys(company_email)
        self.driver.find_element(*self.industry).send_keys(industry)
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
        self.driver.find_element(*self.company_tags).send_keys(company_tags)
        self.driver.find_element(*self.sub_tags).send_keys(sub_tags)
        # self.driver.find_element(*self.submit_button).click()