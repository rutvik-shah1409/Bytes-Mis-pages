import unittest
import os
import time
import traceback
import tempfile
from enum import Enum
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from env_sender import smtp_send
from dotenv import load_dotenv


class ElementLocators(Enum):
    # Common Form fields
    NAME_FIELD = (By.ID, "SingleLine1")
    EMAIL_FIELD = (By.ID, "Email")
    PHONE_FIELD = (By.ID, "mobile_label")

    # For Book Consultation / Contact Us
    COMPANY_FIELD = (By.NAME, "SingleLine")
    MESSAGE_FIELD = (By.NAME, "MultiLine")
    SERVICE_DROPDOWN = (By.ID, "service_label")
    BUDGET_DROPDOWN = (By.ID, "budget_label")
    START_DROPDOWN = (By.ID, "start_label")
    REQUIREMENT_DROPDOWN = (By.NAME, "Dropdown3")

    # For PPC form
    PPC_SERVICE_DROPDOWN = (By.ID, "service_label")
    PPC_PROJECT_DETAIL = (By.NAME, "MultiLine")

    # For Service Page Form
    SERVICE_PROJECT_DETAIL = (By.NAME, "MultiLine")

    # For Service Popup Form
    POPUP_NAME_FIELD = (By.ID, "popup_name")
    POPUP_BUSINESS_EMAIL = (By.ID, "popup_business_email")
    POPUP_PHONE = (By.ID, "popup_phone")
    POPUP_PROJECT_DETAILS = (By.ID, "popup_business_details")
    POPUP_SUBMIT_BUTTON = (By.XPATH, '//*[@id="btn-validates"]')

    # For Hire Form
    HIRE_PROJECT_DETAIL = (By.NAME, "MultiLine")

    # Buttons
    SUBMIT_BUTTON = (By.XPATH, '//*[@id="btn-validate"]')

    # Job Opening Fields
    JOB_NAME = (By.ID, "name")
    JOB_EMAIL = (By.ID, "email")
    JOB_PHONE = (By.NAME, "phone_number")
    JOB_GENDER = (By.ID, "gender")
    JOB_NOTICE_PERIOD = (By.ID, "notice_period")
    JOB_LOCATION = (By.ID, "preferred_job_city")
    JOB_CURRENT_TITLE = (By.ID, "enter_your_current_job_title")
    JOB_TOTAL_EXP = (By.ID, "total_year_experience")
    JOB_RELEVANT_EXP = (By.ID, "enter_your_relevant_experience_year")
    JOB_CURRENT_EMPLOYER = (By.ID, "enter_your_current_employer")
    JOB_CURRENT_SALARY = (By.ID, "enter_your_current_salary_in_lacs")
    JOB_EXPECTED_SALARY = (By.ID, "enter_your_expected_salary_in_lacs")
    JOB_ADDITIONAL_INFO = (By.ID, "additional_info")
    JOB_RESUME_UPLOAD = (By.ID, "resume_upload")
    JOB_SUBMIT = (By.XPATH, '//*[@id="carrer_form_submit"]')


# URLs for all pages
URLS = {
    "book_consultation": [
        ("Global", "https://magnetoitsolutions.com/book-a-free-consultation/?qa=test"),
        ("Canada", "https://magnetoitsolutions.com/canada/book-a-free-consultation/?qa=test"),
        ("United Kingdom", "https://magnetoitsolutions.com/uk/book-a-free-consultation/?qa=test"),
        ("Australia", "https://magnetoitsolutions.com/au/book-a-free-consultation/?qa=test"),
        ("Kuwait", "https://magnetoitsolutions.com/kuwait/book-a-free-consultation/?qa=test"),
        ("Saudi Arabia", "https://magnetoitsolutions.com/sa/book-a-free-consultation/?qa=test"),
        ("South Africa", "https://magnetoitsolutions.com/za/book-a-free-consultation/?qa=test"),
        ("UAE", "https://magnetoitsolutions.com/dubai/book-a-free-consultation/?qa=test"),
    ],
    "contact_us": [
        ("Global", "https://magnetoitsolutions.com/contact/?qa=test"),
        ("Canada", "https://magnetoitsolutions.com/canada/contact/?qa=test"),
        ("United Kingdom", "https://magnetoitsolutions.com/uk/contact/?qa=test"),
        ("Australia", "https://magnetoitsolutions.com/au/contact/?qa=test"),
        ("Kuwait", "https://magnetoitsolutions.com/kuwait/contact/?qa=test"),
        ("Saudi Arabia", "https://magnetoitsolutions.com/sa/contact/?qa=test"),
        ("South Africa", "https://magnetoitsolutions.com/za/contact/?qa=test"),
        ("UAE", "https://magnetoitsolutions.com/dubai/contact/?qa=test"),
    ],
    "ppc_form": [
        ("Global", "https://magnetoitsolutions.com/ppc/headless-commerce/?qa=test"),
        ("UK", "https://magnetoitsolutions.com/uk/ppc/headless-commerce/?qa=test"),
        ("Dubai", "https://magnetoitsolutions.com/dubai/ppc/erpnext/?qa=test"),
        ("SA", "https://magnetoitsolutions.com/sa/ppc/headless-commerce/?qa=test"),
    ],
    "service_page_form": [
        ("Global", "https://magnetoitsolutions.com/services/pimcore-development-company/?qa=test"),
    ],
    "hire_form": [
        ("Global", "https://magnetoitsolutions.com/hire/magento-developer/?qa=test"),
        ("Canada", "https://magnetoitsolutions.com/canada/magento-developer/?qa=test"),
        ("SA", "https://magnetoitsolutions.com/sa/bigcommerce-developers/?qa=test"),
        ("UK", "https://magnetoitsolutions.com/uk/salesforce-developer/?qa=test"),
        ("Australia", "https://magnetoitsolutions.com/au/hire-magento-developers/?qa=test"),
        ("Dubai", "https://magnetoitsolutions.com/dubai/magento-developer/?qa=test"),
        ("Kuwait", "https://magnetoitsolutions.com/kuwait/magento-developer/?qa=test"),
    ],
    "career_page_form": [
        ("Global","http://magnetoitsolutions.com/current-opening/testing_opening/?qa=test")
    ],
    
}


class UnifiedAutomation(unittest.TestCase):
    counter_file = "email_counter.txt"
    passed_urls = []
    failed_urls = []

    @classmethod
    def setUpClass(cls):
        """Setup Chrome driver with headless mode and unique user-data-dir"""
        options = webdriver.ChromeOptions()

        # Headless mode for CI/CD or server runs
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")

        # ✅ Use unique temporary user-data-dir to avoid conflicts
        user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={user_data_dir}")

        # Initialize Chrome WebDriver
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.set_window_size(1920, 1080)

        # Initialize email counter
        if os.path.exists(cls.counter_file):
            with open(cls.counter_file, 'r') as f:
                cls.email_counter = int(f.read().strip())
        else:
            cls.email_counter = 1

    def generate_custom_email(self, base_name="ilfas.mansuri", domain="bytestechnolab.com"):
        custom_email = f"{base_name}+{self.email_counter}@{domain}"
        self.email_counter += 1
        return custom_email

    def close_service_popup_if_present(self, timeout=15):
        """Close popup if it appears on service pages"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".popup_wpr.popup_show"))
            )
            print("Popup appeared.")
            close_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close_img_btn"))
            )
            close_btn.click()
            print("Popup closed successfully.")
            return True
        except:
            print("No popup found.")
            return False

    def close_hire_popup_if_present(self, timeout=15):
        """Close popup if it appears on hire pages"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".popup_wpr.popup_show"))
            )
            print("Popup appeared.")
            close_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close_img_btn"))
            )
            close_btn.click()
            print("Popup closed successfully.")
            return True
        except:
            print("No popup found.")
            return False

    def test_book_consultation(self):
        """Test Book Free Consultation Page"""
        self.run_tests(URLS["book_consultation"], "Book Free Consultation")

    def test_contact_us(self):
        """Test Contact Us Page"""
        self.run_tests(URLS["contact_us"], "Contact Us")

    def test_ppc_form(self):
        """Test PPC Form Page"""
        self.run_tests(URLS["ppc_form"], "PPC Form")

    def test_service_page_form(self):
        """Test Service Page Form"""
        self.run_tests(URLS["service_page_form"], "Service Page Form")

    def test_hire_form(self):
        """Test Hire Form Page"""
        self.run_tests(URLS["hire_form"], "Hire Form")

    def test_career_page_form(self):
        """Test Career Page Form"""
        self.run_tests(URLS["career_page_form"], "Career Page Form")

    def run_tests(self, url_list, page_type):
        for country_name, url in url_list:
            with self.subTest(country=country_name, page=page_type):
                try:
                    print(f"Testing {page_type} for {country_name} at {url}")
                    self.driver.get(url)
                    time.sleep(5)

                    # ⬇️ SCROLL WHEN CAREER PAGE IS OPENED
                    if page_type == "Career Page Form":
                        self.driver.execute_script("window.scrollBy(0, 800);")
                        time.sleep(3)

                    # Fill Common fields
                    if page_type != "Career Page Form":
                        self.driver.find_element(*ElementLocators.NAME_FIELD.value).send_keys("Test Automation")
                        time.sleep(2)
                        email_field = self.driver.find_element(*ElementLocators.EMAIL_FIELD.value)
                        custom_email = self.generate_custom_email()
                        email_field.send_keys(custom_email)
                        print(f"Email Entered: {custom_email}")
                        time.sleep(2)
                        self.driver.find_element(*ElementLocators.PHONE_FIELD.value).send_keys("9909701409")
                        time.sleep(5)

                    if page_type in ["Book Free Consultation", "Contact Us"]:
                        # Extra fields for these forms
                        self.driver.find_element(*ElementLocators.COMPANY_FIELD.value).send_keys("Test Company")
                        time.sleep(1)

                        Select(self.driver.find_element(*ElementLocators.SERVICE_DROPDOWN.value)).select_by_index(2)
                        time.sleep(1)

                        Select(self.driver.find_element(*ElementLocators.BUDGET_DROPDOWN.value)).select_by_index(2)
                        time.sleep(1)

                        Select(self.driver.find_element(*ElementLocators.START_DROPDOWN.value)).select_by_index(1)
                        time.sleep(1)

                        Select(self.driver.find_element(*ElementLocators.REQUIREMENT_DROPDOWN.value)).select_by_index(2)
                        time.sleep(1)

                        self.driver.find_element(*ElementLocators.MESSAGE_FIELD.value).send_keys(
                            "This is a test automation script running."
                        )
                        time.sleep(2)

                    elif page_type == "PPC Form":
                        # Fields specific to PPC form
                        Select(self.driver.find_element(*ElementLocators.PPC_SERVICE_DROPDOWN.value)).select_by_index(2)
                        time.sleep(1)

                        self.driver.find_element(*ElementLocators.PPC_PROJECT_DETAIL.value).send_keys(
                            "This is a PPC form automation test project detail."
                        )
                        time.sleep(10)

                    elif page_type == "Service Page Form":
                        # Clear cookies and cache
                        self.driver.delete_all_cookies()
                        try:
                            self.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
                            self.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
                            print("Cookies and cache cleared.")
                        except Exception as cache_exc:
                            print(f"Could not clear cache/cookies: {cache_exc}")

                        # Close browser and open new incognito window
                        print("Closing browser and opening new incognito window...")
                        self.driver.quit()
                        time.sleep(2)
                        options = webdriver.ChromeOptions()
                        options.add_argument("--incognito")
                        options.add_argument("--headless=new")
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--window-size=1920,1080")
                        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
                        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                        # self.driver.maximize_window()
                        print("New incognito browser opened.")

                        # Reopen the service page URL
                        self.driver.get(url)
                        print(f"Reopened URL: {url}")
                        
                        # Simulate user interaction to trigger lazy loading
                        self.driver.execute_script("window.scrollTo(0, 1000);")
                        time.sleep(2)
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        self.driver.execute_script("window.scrollTo(0, 500);")
                        
                        try:
                            actions = ActionChains(self.driver)
                            actions.move_by_offset(100, 100).perform()
                            actions.move_by_offset(100, 100).perform()
                        except:
                            pass

                        # Force activate lazyJs if they are still there
                        lazy_scripts = self.driver.find_elements(By.CSS_SELECTOR, "script[type='lazyJs']")
                        if len(lazy_scripts) > 0:
                            self.driver.execute_script("document.dispatchEvent(new Event('mousemove'));")
                            self.driver.execute_script("document.dispatchEvent(new Event('scroll'));")
                            self.driver.execute_script("document.dispatchEvent(new Event('touchstart'));")

                        time.sleep(25)  # Wait for popup to appear (20-30s)

                        # Fill popup form with increased wait and retry
                        popup_found = False
                        for attempt in range(1, 5):  # Try up to 4 times
                            try:
                                WebDriverWait(self.driver, 30 + attempt * 15).until(
                                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".popup_wpr.popup_show"))
                                )
                                print(f"Popup detected on attempt {attempt}. Filling popup form...")
                                self.driver.find_element(*ElementLocators.POPUP_NAME_FIELD.value).send_keys("Test Automation")
                                time.sleep(1)
                                self.driver.find_element(*ElementLocators.POPUP_BUSINESS_EMAIL.value).send_keys("test@yopmail.com")
                                time.sleep(1)
                                self.driver.find_element(*ElementLocators.POPUP_PHONE.value).send_keys("9876543210")
                                time.sleep(1)
                                self.driver.find_element(*ElementLocators.POPUP_PROJECT_DETAILS.value).send_keys("This is test automation.")
                                time.sleep(1)
                                self.driver.find_element(*ElementLocators.POPUP_SUBMIT_BUTTON.value).click()
                                print("Popup form submitted successfully.")
                                
                                # Wait for popup to close
                                try:
                                    WebDriverWait(self.driver, 15).until(
                                        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".popup_wpr.popup_show"))
                                    )
                                    print("Popup closed.")
                                except:
                                    print("Popup did not close automatically, attempting to close manually...")
                                    try:
                                        self.driver.find_element(By.CSS_SELECTOR, "button.close_img_btn").click()
                                    except:
                                        pass

                                time.sleep(2)
                                popup_found = True
                                self.passed_urls.append(f"✅ Popup Form Submitted - {url}")
                                break
                            except Exception as e:
                                print(f"Attempt {attempt}: Popup not found or error filling popup: {e}")
                                time.sleep(10)
                        if not popup_found:
                            print("Popup did not appear after maximum wait time.")
                            self.failed_urls.append(f"❌ Popup Form Failed - {url}")

                        # Fill all required fields in service page form after popup
                        try:
                            name_field = self.driver.find_element(*ElementLocators.NAME_FIELD.value)
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", name_field)
                            time.sleep(1)
                            name_field.send_keys("Test Automation")
                            time.sleep(1)
                            email_field = self.driver.find_element(*ElementLocators.EMAIL_FIELD.value)
                            custom_email = self.generate_custom_email()
                            email_field.send_keys(custom_email)
                            print(f"Email Entered: {custom_email}")
                            time.sleep(1)
                            self.driver.find_element(*ElementLocators.PHONE_FIELD.value).send_keys("9909701409")
                            time.sleep(1)
                            self.driver.find_element(*ElementLocators.SERVICE_PROJECT_DETAIL.value).send_keys(
                                "This is a Service Page form automation test project detail."
                            )
                            time.sleep(1)
                            self.passed_urls.append(f"✅ {country_name} - Service Page Form - {url}")
                        except Exception as e:
                            print(f"Error filling service page form after popup: {e}")
                            self.failed_urls.append(f"❌ {country_name} - Service Page Form Failed - {url}")
                        
                        time.sleep(15)

                    elif page_type == "Hire Form":
                        self.close_hire_popup_if_present(timeout=15)
                        time.sleep(5)
                        self.driver.find_element(*ElementLocators.HIRE_PROJECT_DETAIL.value).send_keys(
                            "This is a Hire Page form automation test project detail."
                        )
                        time.sleep(2)

                    elif page_type == "Career Page Form":
                        # 🔹 Career form full filling logic
                        self.driver.find_element(*ElementLocators.JOB_NAME.value).send_keys("Test Candidate")
                        time.sleep(3)
                        email_field = self.driver.find_element(*ElementLocators.JOB_EMAIL.value)
                        custom_email = self.generate_custom_email()
                        email_field.send_keys(custom_email)
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_PHONE.value).send_keys("9909701409")
                        time.sleep(3)
                        Select(self.driver.find_element(*ElementLocators.JOB_GENDER.value)).select_by_index(1)
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_NOTICE_PERIOD.value).send_keys("30")
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_LOCATION.value).send_keys("Ahmedabad")
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_CURRENT_TITLE.value).send_keys("QA Engineer")
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_TOTAL_EXP.value).send_keys("2")
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_RELEVANT_EXP.value).send_keys("2")
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_CURRENT_EMPLOYER.value).send_keys("TechCorp Pvt Ltd")
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_CURRENT_SALARY.value).send_keys("4")
                        time.sleep(3)                    
                        self.driver.find_element(*ElementLocators.JOB_EXPECTED_SALARY.value).send_keys("6")
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_ADDITIONAL_INFO.value).send_keys("Ready to join immediately.")
                        # self.driver.find_element(*ElementLocators.JOB_RESUME_UPLOAD.value).click()
                        time.sleep(3)
                        resume_path = "/home/rutvik/Documents/Fake-Resume.pdf"
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_RESUME_UPLOAD.value).send_keys(resume_path)
                        time.sleep(3)
                        self.driver.find_element(*ElementLocators.JOB_SUBMIT.value).click()
                        time.sleep(5)

                    if page_type != "Career Page Form" and page_type != "Service Page Form":
                        submit_btn = self.driver.find_element(*ElementLocators.SUBMIT_BUTTON.value)
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                        time.sleep(2)
                        submit_btn.click()
                    time.sleep(10)

                    # Skip adding general entry for Service Page Form as it's already tracked separately
                    if page_type != "Service Page Form":
                        self.passed_urls.append(f"✅ {country_name} - {page_type} - {url}")

                except Exception as e:
                    error_msg = traceback.format_exc().splitlines()[-1]
                    print(f"Error: {e}")
                    traceback.print_exc()
                    self.failed_urls.append(f"❌ {country_name} - {page_type} - {url}")

    @classmethod
    def tearDownClass(cls):
        """Cleanup driver and send report"""
        with open(cls.counter_file, 'w') as f:
            f.write(str(cls.email_counter))
        cls.driver.quit()
        cls.send_email_report()

    @classmethod
    def send_email_report(cls):
        sender_email = os.getenv("SENDER_EMAIL")
        password = os.getenv("PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        cc_email = os.getenv("CC_EMAIL")
        subject = "MIS Automation Test Report - Contact Us & Book Free Consultation"
        email_body = f"""
        <h3>Test Report</h3>
        <p><b>Passed Tests:</b></p>
        <ul>
            {''.join(f"<li>{test}</li>" for test in cls.passed_urls)}
        </ul>

        <p><b>Failed Tests:</b></p>
        <ul>
            {''.join(f"<li>{test}</li>" for test in cls.failed_urls) if cls.failed_urls else "<li>No test failures 🎉</li>"}
        </ul>
        """

        smtp_send(
            sender_email=sender_email,
            receiver_email=receiver_email,
            cc_email=cc_email,
            subject=subject,
            password=password,
            email_body=email_body
        )
        print("Email Sent Successfully!")


if __name__ == "__main__":
    unittest.main()