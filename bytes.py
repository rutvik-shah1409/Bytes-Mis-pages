import unittest
import os
import traceback
import time
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from env_sender import smtp_send
from dotenv import load_dotenv

class ContactUsLocators(Enum):
    FULL_NAME = (By.ID, "full_name")
    EMAIL_ID = (By.ID, "email_id")
    CONTACT_NUMBER = (By.ID, "contact_number")
    COMPANY_URL = (By.ID, "company_url")
    SERVICE_LABEL = (By.ID, "service_label")
    BUDGET_LABEL = (By.ID, "budget_label")
    REQUIREMENT_LABEL = (By.ID, "requirement_label")
    START_LABEL = (By.ID, "start_label")
    PROJECT_DESCRIPTION = (By.ID, "project_description")
    SUBMIT_BUTTON = (By.XPATH, "//*[@id='v3_insert']")

class LetsTalkLocators(Enum):
    FULL_NAME = (By.ID, "fullName_lets_talk_home")
    EMAIL_ID = (By.ID, "email_lets_talk_home")
    CONTACT_NUMBER = (By.ID, "contact_number")
    COMPANY_URL = (By.ID, "company_url_2")
    SERVICE_LABEL = (By.ID, "single_service_home")
    PROJECT_DESCRIPTION = (By.ID, "project_description_2")
    SUBMIT_BUTTON = (By.CLASS_NAME, "primary_btn")

class OurServiceLocators(Enum):
    FULL_NAME = (By.ID, "full_name")
    EMAIL_ID = (By.ID, "email_id")
    CONTACT_NUMBER = (By.ID, "contact_number")
    COMPANY_URL = (By.ID, "company_url")
    SERVICE_LABEL = (By.ID, "single_service")
    PROJECT_DESCRIPTION = (By.ID, "project_description")
    SUBMIT_BUTTON = (By.CLASS_NAME, "primary_btn")

class HireDeveloversLocators(Enum):
    FULL_NAME = (By.ID, "full_name")
    EMAIL_ID = (By.ID, "email_id")
    CONTACT_NUMBER = (By.ID, "contact_number")
    COMPANY_URL = (By.ID, "company_url")
    SERVICE_LABEL = (By.ID, "service_label")
    BUDGET_LABEL = (By.ID, "budget_label")
    REQUIREMENT_LABEL = (By.ID, "requirement_label")
    START_LABEL = (By.ID, "start_label")
    PROJECT_DESCRIPTION = (By.ID, "project_description")
    SUBMIT_BUTTON = (By.CLASS_NAME, "primary_btn")

class CareerFormLocators(Enum):
    FULL_NAME = (By.NAME, "fname")
    EMAIL_ID = (By.ID, "email_id")
    CONTACT_NUMBER = (By.NAME, "contact_number")
    TOTAL_EXP = (By.NAME, "total-experience")
    RELEVANT_EXP = (By.NAME, "relevant-experience")
    CURRENT_CTC = (By.NAME, "Current-CTC")
    EXPECTED_CTC = (By.NAME, "Expected-CTC")
    CURRENT_LOCATOIN = (By.NAME, "Current-Location")
    NOTICE_PERIOD = (By.NAME, "notice-period")
    RESUME_UPLOAD = (By.ID, "resume")
    SUBMIT_BUTTON = (By.ID, "applynow")

URLS = [
    ("Bytes Contact Us", "https://www.bytestechnolab.com/contact-us/", ContactUsLocators),
    ("Bytes Contact Us UK", "https://www.bytestechnolab.com/uk/contact-us/", ContactUsLocators),
    ("Bytes Contact Us AU", "https://www.bytestechnolab.com/au/contact-us/", ContactUsLocators),
    ("Bytes Contact Us SA", "https://www.bytestechnolab.com/sa/contact-us/", ContactUsLocators),
    ("Bytes Let's Talk", "https://www.bytestechnolab.com/", LetsTalkLocators),
    ("Bytes Let's Talk UK", "https://www.bytestechnolab.com/uk/", LetsTalkLocators),
    ("Bytes Let's Talk AU", "https://www.bytestechnolab.com/au/", LetsTalkLocators),
    ("Bytes Let's Talk SA", "https://www.bytestechnolab.com/sa/", LetsTalkLocators),
    ("Bytes OurService", "https://www.bytestechnolab.com/our-services", OurServiceLocators),
    ("Bytes Hire Develovers", "https://www.bytestechnolab.com/hire-developers", HireDeveloversLocators),
    ("Bytes Hire Develovers UK", "https://www.bytestechnolab.com/uk/hire-developers", HireDeveloversLocators),
    ("Bytes Hire Develovers AU", "https://www.bytestechnolab.com/au/hire-developers", HireDeveloversLocators),
    ("Bytes Hire Develovers SA", "https://www.bytestechnolab.com/sa/hire-developers", HireDeveloversLocators),
    ("Bytes Career Form", "https://www.bytestechnolab.com/opportunities/bytes-qa-testing-opening/", CareerFormLocators)
]

class BytesTests(unittest.TestCase):
    load_dotenv()
    counter_file = "email_counter.txt"
    passed_urls = []
    failed_urls = []

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.wait = WebDriverWait(cls.driver, 30)

        if os.path.exists(cls.counter_file):
            with open(cls.counter_file, 'r') as f:
                cls.email_counter = int(f.read().strip())
        else:
            cls.email_counter = 1

    def fill_input(self, locator, value):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.wait.until(EC.visibility_of(element))
            element.clear()
            element.send_keys(value)    
        except Exception as e:
            raise Exception(f"Error in fill_input({locator}): {str(e)}")

    def test_website_forms(self):
        for test_name, url, locators in URLS:
            with self.subTest(test_name=test_name, url=url):
                try:
                    print(f"\n🔍 Testing: {test_name} - {url}")
                    self.driver.get(url)

                    if locators == CareerFormLocators:
                    # Career Form handling
                        self.fill_input(locators.FULL_NAME.value, "Ilfas Mansuri")
                        time.sleep(5)
                        self.fill_input(locators.EMAIL_ID.value, "ilfas.mansuri@bytestechnolab.com")
                        time.sleep(5)
                        self.fill_input(locators.CONTACT_NUMBER.value, "9876543210")
                        time.sleep(5)
                        self.fill_input(locators.TOTAL_EXP.value, "3")
                        time.sleep(5)
                        self.fill_input(locators.RELEVANT_EXP.value, "2")
                        time.sleep(5)
                        self.fill_input(locators.CURRENT_CTC.value, "500000")
                        time.sleep(5)
                        self.fill_input(locators.EXPECTED_CTC.value, "700000")
                        time.sleep(5)
                        self.fill_input(locators.CURRENT_LOCATOIN.value, "Ahmedabad")
                        time.sleep(5)
                        self.fill_input(locators.NOTICE_PERIOD.value, "30 Days")
                        time.sleep(5)
                        # File upload (resume)
                        resume_path = os.path.abspath("/home/rutvik/Documents/Fake-Resume.pdf")
                        self.wait.until(EC.presence_of_element_located(locators.RESUME_UPLOAD.value)).send_keys(resume_path)
                        time.sleep(5)
                        # Submit
                        submit_button = self.wait.until(EC.element_to_be_clickable(locators.SUBMIT_BUTTON.value))
                        # self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                        # self.driver.execute_script("arguments[0].click();", submit_button)

                    else:
                    # Default handling for Contact Us, Let's Talk, Our Services, Hire Developers
                        self.fill_input(locators.FULL_NAME.value, "Test Bytes")
                        time.sleep(2)
                        self.fill_input(locators.EMAIL_ID.value, "ilfas.mansuri@bytestechnolab.com")
                        time.sleep(2)
                        self.fill_input(locators.CONTACT_NUMBER.value, "9687414356")
                        time.sleep(2)

                        if hasattr(locators, "COMPANY_URL"):
                            self.fill_input(locators.COMPANY_URL.value, "Test Bytes Technolab")

                    # Handle dropdowns
                    dropdown_fields = ['SERVICE_LABEL', 'BUDGET_LABEL', 'REQUIREMENT_LABEL', 'START_LABEL']
                    for field in dropdown_fields:
                        if hasattr(locators, field):
                            dropdown_locator = getattr(locators, field).value
                            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_locator))
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                            Select(dropdown).select_by_index(1)

                    if hasattr(locators, "PROJECT_DESCRIPTION"):
                        self.fill_input(locators.PROJECT_DESCRIPTION.value, "Automation testing form submission")

                    # Submit
                    submit_button = self.wait.until(EC.element_to_be_clickable(locators.SUBMIT_BUTTON.value))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    self.driver.execute_script("arguments[0].click();", submit_button)

                    time.sleep(10)  # Wait for submission
                    self.email_counter += 1
                    print(f"✅ Passed: {test_name}")
                    self.passed_urls.append(f"✅ {test_name} - {url}")

                except Exception as e:
                    print(f"❌ Failed: {test_name}\n{traceback.format_exc()}")
                    screenshot = f"screenshot_{test_name.replace(' ', '_')}.png"
                    self.driver.save_screenshot(screenshot)
                    self.failed_urls.append(f"❌{test_name} - {url} - {str(e)}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        with open(cls.counter_file, 'w') as f:
            f.write(str(cls.email_counter))

        # Uncomment to send email report
        # cls.send_email_report()

    @classmethod
    def send_email_report(cls):
        sender_email = os.getenv("SENDER_EMAIL")
        password = os.getenv("PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        cc_email = os.getenv("CC_EMAIL")
        subject = "Bytes Automation Test Report - Contact Us , Let's Talk & Our Service"

        email_body = f"""
        <h3>Automation Report</h3>
        <p><b>Passed:</b></p>
        <ul>{''.join(f"<li>{url}</li>" for url in cls.passed_urls)}</ul>
        <p><b>Failed:</b></p>
        <ul>{''.join(f"<li>{url}</li>" for url in cls.failed_urls) if cls.failed_urls else '<li>No test failures 🎉</li>'}</ul>
        """

        smtp_send(
            sender_email=sender_email,
            receiver_email=receiver_email,
            cc_email=cc_email,
            subject=subject,
            password=password,
            email_body=email_body
        )
        print("📧 Email sent.")

if __name__ == "__main__":
    unittest.main()
