#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import io
import re
import time
from sysValues import SysValues

class OCR():
    
    domainUrl = ''
    driver = None
    
    def __init__(self, url, tesseractPath=SysValues.TESSERACT.value):
        # Set the path to the Tesseract executable (update this with your path)
        pytesseract.pytesseract.tesseract_cmd = tesseractPath
        self.domainUrl = url

        # Set the desired window size (virtual screen resolution)
        window_size = (1920, 1080)  # Adjust the dimensions as needed

        # Create a headless Chrome browser
        chrome_options = Options()
        chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--disable-gpu')

        service = Service(SysValues.CHROME_DRIVER.value)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        # Navigate to the webpage
        self.driver.get(url)
        
    def get_lines(self):
        try:
            # Handle cookie consent (customize this based on the structure of the webpage)
            # For example, clicking on an element with a specific class or ID
            cookie_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cc-btn.cc-allow-all.Alles.annehmen')))
            cookie_button.click()

            # Wait for specific elements to be present before executing the script
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.wisyr_kurstitel'))
            WebDriverWait(self.driver, 10).until(element_present)

            element_present = EC.presence_of_element_located((By.ID, 'wisyr_tabnav_tabpane0'))
            WebDriverWait(self.driver, 10).until(element_present)

            # Execute JavaScript to replace the body content with the specific div
            self.driver.execute_script("""
                var body = document.body;
                var specificDiv1 = document.querySelector('.wisyr_kurstitel');
                var specificDiv2 = document.getElementById('wisyr_tabnav_tabpane0');
                
                if (specificDiv1 && specificDiv2) {
                    body.innerHTML = '';  // Clear existing content (optional)
                    body.appendChild(specificDiv1.cloneNode(true));
                    body.appendChild(specificDiv2.cloneNode(true));
                }
            """)

            time.sleep(10)

            # Execute JavaScript to check if the page is scrollable
            # is_scrollable = self.driver.execute_script("return document.documentElement.scrollHeight > document.documentElement.clientHeight;")

            # if is_scrollable:
            #     print("The page is scrollable.")
            # else:
            #     print("The page is not scrollable.")

            # Take a screenshot of the specified section
            screenshot = self.driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(screenshot))

            # Perform OCR on the captured image
            text = pytesseract.image_to_string(img, lang='deu')

            # Split lines based on a threshold for consecutive newline characters
            #lines = re.split('\n\s*\n|\r\n\s*\r\n|\r\s*\r', text)
            lines = re.split('\n', text)
        
            # Iterate over the extracted lines
            linesList = []
            value = ""
            for line in lines:
                if(len(line) >= 20):
                    linesList.append(value)
                    value = ""
                    linesList.append(line)
                else:
                    value = value + " " + line
            
            if(value != ""):
                linesList.append(value)

            self.driver.quit()
            return linesList
        except Exception as ex:
            print(ex)
            return []
            
        finally:
            # Close the browser
            self.driver.quit()