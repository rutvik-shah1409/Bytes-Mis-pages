import unittest
import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Env_sender import smtp_send

class Bytes(unittest.TestCase):

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
        cls.driver.set_window_size(1920, 1080)

        if os.path.exists(Bytes.counter_file):
            with open(Bytes.counter_file, 'r') as f:
                Bytes.email_counter = int(f.read().strip())
        else:
            Bytes.email_counter = 1

    def generate_custom_email(self, base_name='ilfas.mansuri', domain='bytestechnolab.com'):
        custom_email = f"{base_name}+{Bytes.email_counter}@{domain}"
        Bytes.email_counter += 1
        return custom_email

    def test_bytes_contact_us_form(self):
        starting_url = "https://www.nexstaralliance.com/"
        test_name = "Nexstar Contact Us"
        try:
            self.driver.get(starting_url)
            self.driver.execute_script("window.scrollBy(0, 4000);")
            self.driver.save_screenshot("headless_debug.png")  # Debug screenshot

            # Wait for the name field to be present
            name_elem = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "name"))
            )
            # Scroll the element into view and click using JS to avoid interception
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", name_elem)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, "name")))
            self.driver.execute_script("arguments[0].click();", name_elem)

            # Fill the form fields with explicit waits
            name_elem.send_keys("Test Bytes")

            custom_email = self.generate_custom_email()
            email_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_elem.send_keys(custom_email)

            tel_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "tel"))
            )
            tel_elem.send_keys("9687414356")

            select_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "select"))
            )
            select_elem.send_keys("Test")

            message_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "message"))
            )
            message_elem.send_keys("This is testing team of Bytes Technolab")

            # Wait for the submit button and click
            button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="nexstar_contact"]/input'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            self.driver.execute_script("arguments[0].click();", button)

            self.passed_urls.append(f"✅ {test_name} - {starting_url}")
        except Exception as e:
            print(f"Error during test: {traceback.format_exc()}")
            self.failed_urls.append(f"❌ {test_name} - {starting_url}")

    @classmethod
    def tearDownClass(cls):
        with open(Bytes.counter_file, 'w') as f:
            f.write(str(Bytes.email_counter))
        cls.driver.quit()
        cls.send_email_report()

    @classmethod
    def send_email_report(cls):
        sender_email = os.getenv("SENDER_EMAIL")
        password = os.getenv("PASSWORD")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        cc_email = os.getenv("CC_EMAIL")
        subject = "Nexstar Automation Test Report"

        email_body = f"""
        <h3>Test Report</h3>
        <p><b>Passed Tests:</b></p>
        <ul>
            {''.join(f"<li>{test}</li>" for test in cls.passed_urls)}
        </ul>
        <p><b>Failed Tests:</b></p>
        <ul>
            {''.join(f"<li>{test}</li>" for test in cls.failed_urls) if cls.failed_urls else "<li>No test failures</li>"}
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


















# import unittest
# import os
# import time
# import traceback
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from Env_sender import smtp_send

# class Bytes(unittest.TestCase):

#     counter_file = "email_counter.txt"
#     passed_urls = []
#     failed_urls = []

#     @classmethod
#     def setUpClass(cls):
#         options = webdriver.ChromeOptions()
#         # options.add_argument("--headless")
#         options.add_argument("--window-size=1920,1080")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         cls.driver.maximize_window()
        

#         if os.path.exists(Bytes.counter_file):
#             with open(Bytes.counter_file, 'r') as f:
#                 Bytes.email_counter = int(f.read().strip())
#         else:
#             Bytes.email_counter = 1

#     def generate_custom_email(self, base_name='ilfas.mansuri', domain='bytestechnolab.com'):
#         custom_email = f"{base_name}+{Bytes.email_counter}@{domain}"
#         Bytes.email_counter += 1
#         return custom_email

#     def test_bytes_contact_us_form(self):
#         starting_url = "https://www.nexstaralliance.com/"
#         test_name = "Nexstar Contact Us"
#         try:
#             self.driver.get(starting_url)
#             self.driver.execute_script("window.scrollBy(0, 4000);")
#             time.sleep(5)
#             self.driver.find_element(By.XPATH, '//*[@id="name"]').click()
#             time.sleep(5)
#             self.driver.find_element(By.ID, "name").send_keys("Test Bytes")
#             custom_email = self.generate_custom_email()
#             self.driver.find_element(By.ID, "email").send_keys(custom_email)
#             self.driver.find_element(By.ID, "tel").send_keys("9687414356")
#             self.driver.find_element(By.ID, "select").send_keys("Test")
#             self.driver.find_element(By.ID, "message").send_keys("This is testing team of Bytes Technolab")
#             time.sleep(10)
#             button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//*[@id="nexstar_contact"]/input'))
#             )
#             button.click()
#             time.sleep(10)
#             self.passed_urls.append(f"✅ {test_name} - {starting_url}")
#         except Exception as e:
#             print(f"Error during test: {traceback.format_exc()}")
#             self.failed_urls.append(f"❌ {test_name} - {starting_url}")

#     @classmethod
#     def tearDownClass(cls):
#         with open(Bytes.counter_file, 'w') as f:
#             f.write(str(Bytes.email_counter))
#         cls.driver.quit()
#         # cls.send_email_report()

#     # @classmethod
#     # def send_email_report(cls):
#     #     sender_email = os.getenv("SENDER_EMAIL")
#     #     password = os.getenv("PASSWORD")
#     #     receiver_email = os.getenv("RECEIVER_EMAIL")
#     #     cc_email = os.getenv("CC_EMAIL")
#     #     subject = "Nexstar Automation Test Report"

#     #     email_body = f"""
#     #     <h3>Test Report</h3>
#     #     <p><b>Passed Tests:</b></p>
#     #     <ul>
#     #         {''.join(f"<li>{test}</li>" for test in cls.passed_urls)}
#     #     </ul>
#     #     <p><b>Failed Tests:</b></p>
#     #     <ul>
#     #         {''.join(f"<li>{test}</li>" for test in cls.failed_urls) if cls.failed_urls else "<li>No test failures</li>"}
#     #     </ul>
#     #     """

#         # smtp_send(
#         #     sender_email=sender_email,
#         #     receiver_email=receiver_email,
#         #     cc_email=cc_email,
#         #     subject=subject,
#         #     password=password,
#         #     email_body=email_body
#         # )
#         # print("Email Sent Successfully!")

# if __name__ == "__main__":
#     unittest.main()
