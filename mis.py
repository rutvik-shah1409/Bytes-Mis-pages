import unittest
import os
import time
import traceback
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Env_sender import smtp_send

class ElementLocators(Enum):
    # Form fields
    NAME_FIELD = (By.ID, "SingleLine1")
    EMAIL_FIELD = (By.ID, "Email")
    PHONE_FIELD = (By.ID, "mobile_label")
    COMPANY_FIELD = (By.NAME, "SingleLine")
    MESSAGE_FIELD = (By.NAME, "MultiLine")

    # Dropdowns
    SERVICE_DROPDOWN = (By.ID, "service_label")
    BUDGET_DROPDOWN = (By.ID, "budget_label")
    START_DROPDOWN = (By.ID, "start_label")
    REQUIREMENT_DROPDOWN = (By.NAME, "Dropdown3")
    # Buttons
    SUBMIT_BUTTON = (By.XPATH, '//*[@id="btn-validate"]')

# URLs for both pages
URLS = {
    "book_consultation": [
        ("India", "https://magnetoitsolutions.com/book-a-free-consultation/?qa=test"),
        ("Canada", "https://magnetoitsolutions.com/canada/book-a-free-consultation/?qa=test"),
        ("United Kingdom", "https://magnetoitsolutions.com/uk/book-a-free-consultation/?qa=test"),
        ("Australia", "https://magnetoitsolutions.com/au/book-a-free-consultation/?qa=test"),
        ("Kuwait", "https://magnetoitsolutions.com/kuwait/book-a-free-consultation/?qa=test"),
        ("Saudi Arabia", "https://magnetoitsolutions.com/sa/book-a-free-consultation/?qa=test"),
        ("South Africa", "https://magnetoitsolutions.com/za/book-a-free-consultation/?qa=test"),
        ("UAE", "https://magnetoitsolutions.com/dubai/book-a-free-consultation/?qa=test"),
    ],
    "contact_us": [
        ("India", "https://magnetoitsolutions.com/contact/?qa=test"),
        ("Canada", "https://magnetoitsolutions.com/canada/contact/?qa=test"),
        ("United Kingdom", "https://magnetoitsolutions.com/uk/contact/?qa=test"),
        ("Australia", "https://magnetoitsolutions.com/au/contact/?qa=test"),
        ("Kuwait", "https://magnetoitsolutions.com/kuwait/contact/?qa=test"),
        ("Saudi Arabia", "https://magnetoitsolutions.com/sa/contact/?qa=test"),
        ("South Africa", "https://magnetoitsolutions.com/za/contact/?qa=test"),
        ("UAE", "https://magnetoitsolutions.com/dubai/contact/?qa=test"),
    ]
}

class UnifiedAutomation(unittest.TestCase):
    counter_file = "email_counter.txt"
    passed_urls = []
    failed_urls = []

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode for CI/CD
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.maximize_window()
        

        if os.path.exists(cls.counter_file):
            with open(cls.counter_file, 'r') as f:
                cls.email_counter = int(f.read().strip())
        else:
            cls.email_counter = 1

    def generate_custom_email(self, base_name="ilfas.mansuri", domain="bytestechnolab.com"):
        custom_email = f"{base_name}+{self.email_counter}@{domain}"
        self.email_counter += 1
        return custom_email

    def test_book_consultation(self):
        """Test Book Free Consultation Page"""
        self.run_tests(URLS["book_consultation"], "Book Free Consultation")

    def test_contact_us(self):
        """Test Contact Us Page"""
        self.run_tests(URLS["contact_us"], "Contact Us")

    def run_tests(self, url_list, page_type):
        for country_name, url in url_list:
            with self.subTest(country=country_name, page=page_type):
                try:
                    print(f"Testing {page_type} for {country_name} at {url}")
                    self.driver.get(url)
                    time.sleep(5)

                    # Fill out the form
                    self.driver.find_element(*ElementLocators.NAME_FIELD.value).send_keys("Test Automation")
                    time.sleep(2)

                    email_field = self.driver.find_element(*ElementLocators.EMAIL_FIELD.value)
                    custom_email = self.generate_custom_email()
                    email_field.send_keys(custom_email)
                    print(f"Email Entered: {custom_email}")
                    time.sleep(2)
                    self.driver.find_element(*ElementLocators.PHONE_FIELD.value).send_keys("9909701409")
                    time.sleep(2)

                    self.driver.find_element(*ElementLocators.COMPANY_FIELD.value).send_keys("Test Company")
                    time.sleep(2)
                    
                    Select(self.driver.find_element(*ElementLocators.SERVICE_DROPDOWN.value)).select_by_index(2)
                    time.sleep(2)

                    Select(self.driver.find_element(*ElementLocators.BUDGET_DROPDOWN.value)).select_by_index(2)
                    time.sleep(2)

                    Select(self.driver.find_element(*ElementLocators.START_DROPDOWN.value)).select_by_index(1)
                    time.sleep(2)

                    Select(self.driver.find_element(*ElementLocators.REQUIREMENT_DROPDOWN.value)).select_by_index(2)
                    time.sleep(2)

                    self.driver.find_element(*ElementLocators.MESSAGE_FIELD.value).send_keys(
                        "This is a test automation script running."
                    )
                    self.driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(10)

                    self.driver.find_element(*ElementLocators.SUBMIT_BUTTON.value).click()
                    time.sleep(10)

                    self.passed_urls.append(f"✅ {country_name} - {page_type} - {url}")

                except Exception as e:
                    error_msg = traceback.format_exc().splitlines()[-1]
                    self.failed_urls.append(f"❌ {country_name} - {page_type} - {url}")

    @classmethod
    def tearDownClass(cls):
        with open(cls.counter_file, 'w') as f:
            f.write(str(cls.email_counter))
        cls.driver.quit()
    #     cls.send_email_report()

    # @classmethod
    # def send_email_report(cls):
    #     sender_email = os.getenv("SENDER_EMAIL")
    #     password = os.getenv("PASSWORD")
    #     receiver_email = os.getenv("RECEIVER_EMAIL")
    #     cc_email = os.getenv("CC_EMAIL")
    #     subject = "MIS Automation Test Report - Contact Us & Book Free Consultation"
    #     email_body = f"""
        
    #     <h3>Test Report</h3>
    #     <p><b>Passed Tests:</b></p>
    #     <ul>
    #         {''.join(f"<li>{test}</li>" for test in cls.passed_urls)}
    #     </ul>

    #     <p><b>Failed Tests:</b></p>
    #     <ul>
    #         {''.join(f"<li>{test}</li>" for test in cls.failed_urls)if cls.failed_urls else "<li>No test failures 🎉</li>"}
    #     </ul>
    #     """

    #     smtp_send(
    #         sender_email=sender_email,
    #         receiver_email=receiver_email,
    #         cc_email=cc_email,
    #         subject=subject,
    #         password=password,
    #         email_body=email_body
    #     )
    #     print("Email Sent Successfully!")

if __name__ == "__main__":
    unittest.main()
