"""
LinkedIn Scraper implementation.
"""
from typing import Dict, Optional
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

class LinkedInScraper:
    def __init__(self, headless: bool = True):
        """Initialize the LinkedIn scraper.
        
        Args:
            headless (bool): Whether to run the browser in headless mode
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self, email: Optional[str] = None, password: Optional[str] = None) -> bool:
        """Login to LinkedIn.
        
        Args:
            email (str, optional): LinkedIn email. Defaults to env var LINKEDIN_EMAIL
            password (str, optional): LinkedIn password. Defaults to env var LINKEDIN_PASSWORD
            
        Returns:
            bool: True if login successful, False otherwise
        """
        email = email or os.getenv('LINKEDIN_EMAIL')
        password = password or os.getenv('LINKEDIN_PASSWORD')
        
        if not email or not password:
            raise ValueError("Email and password must be provided")
            
        try:
            self.driver.get('https://www.linkedin.com/login')
            
            # Wait for and fill email field
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)
            
            # Fill password field
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for successful login
            time.sleep(3)  # Allow time for login to complete
            
            return "feed" in self.driver.current_url.lower()
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
            
    def get_profile_info(self, profile_url: str) -> Dict:
        """Scrape basic information from a LinkedIn profile.
        
        Args:
            profile_url (str): URL of the LinkedIn profile to scrape
            
        Returns:
            Dict: Dictionary containing profile information
        """
        try:
            self.driver.get(profile_url)
            time.sleep(2)  # Allow time for page to load
            
            # Extract basic information
            name = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
            ).text
            
            headline = self.driver.find_element(
                By.CSS_SELECTOR, 
                "div.text-body-medium"
            ).text
            
            location = self.driver.find_element(
                By.CSS_SELECTOR,
                "span.text-body-small"
            ).text
            
            return {
                "name": name,
                "headline": headline,
                "location": location,
                "profile_url": profile_url
            }
            
        except Exception as e:
            print(f"Failed to get profile info: {str(e)}")
            return {}
            
    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()