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
from Env_sender import smtp_send
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

URLS = [
    ("Bytes Contact Us", "https://www.bytestechnolab.com/contact-us/", ContactUsLocators),
    ("Bytes Contact Us UK", "https://www.bytestechnolab.com/uk/contact-us/", ContactUsLocators),
    ("Bytes Let's Talk", "https://www.bytestechnolab.com/", LetsTalkLocators),
    ("Bytes Let's Talk UK", "https://www.bytestechnolab.com/uk/", LetsTalkLocators),
    ("Bytes OurService", "https://www.bytestechnolab.com/our-services", OurServiceLocators)
]

class BytesTests(unittest.TestCase):
    load_dotenv()
    counter_file = "email_counter.txt"
    passed_urls = []
    failed_urls = []

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.wait = WebDriverWait(cls.driver, 20)

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

                    # Fill text fields
                    self.fill_input(locators.FULL_NAME.value, "Test Bytes")
                    time.sleep(5)  # Wait for the page to load
                    self.fill_input(locators.EMAIL_ID.value, "ilfas.mansuri@bytestechnolab.com")
                    time.sleep(5)  # Wait for the email field to be ready
                    self.fill_input(locators.CONTACT_NUMBER.value, "9687414356")
                    time.sleep(5)  # Wait for the contact number field to be ready
                    self.fill_input(locators.COMPANY_URL.value, "Test Bytes Technolab")
                    time.sleep(5)  # Wait for the company URL field to be ready
                    # Handle dropdowns
                    dropdown_fields = ['SERVICE_LABEL', 'BUDGET_LABEL', 'REQUIREMENT_LABEL', 'START_LABEL']
                    for field in dropdown_fields:
                        if hasattr(locators, field):
                            dropdown_locator = getattr(locators, field).value
                            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_locator))
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                            Select(dropdown).select_by_index(1)
                    time.sleep(5)  # Wait for dropdown selection to be processed
                    self.fill_input(locators.PROJECT_DESCRIPTION.value, "Automation testing form submission")
                    time.sleep(5)  # Wait for the project description field to be ready
                    # Submit
                    submit_button = self.wait.until(EC.element_to_be_clickable(locators.SUBMIT_BUTTON.value))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    self.driver.execute_script("arguments[0].click();", submit_button)
                    time.sleep(10)  # Wait for the form submission to complete
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
        cls.send_email_report()

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
        <ul>{''.join(f"<li>{url}</li>" for url in cls.failed_urls) if cls.failed_urls else '<li>No test failures</li>'}</ul>
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
