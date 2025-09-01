import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from utils.logger import get_logger


class BaseTest(unittest.TestCase):
    base_url = 'https://useinsider.com/'

    def setUp(self):
        self.log = get_logger()
        """Chrome oturumunu başlat, sayfayı aç, implicit wait"""
        chrome_options = Options()
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument("--disable-application-cache")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(10)
        self.cookie_reject_if_visible()
        self.log.info("Setup tamamlandı, ana sayfa açıldı.")

    def tearDown(self):
        """Oturumu kapat"""
        self.driver.quit()

    def cookie_reject_if_visible(self):
        """Visible ise çerez/consent banner'ını reddet"""
        try:
            for el in self.driver.find_elements(By.ID, "wt-cli-reject-btn"):
                if el.is_displayed():
                    el.click(); time.sleep(1); return
            xpath = "//a[contains(., 'Decline') or contains(., 'Reddet') or contains(., 'Reject')]"
            for el in self.driver.find_elements(By.XPATH, xpath):
                if el.is_displayed():
                    el.click(); time.sleep(1); return
        except Exception:
            pass

    """Logging (test flow için)"""
    def step(self, message: str):
        self.log.info(f"STEP: {message}")
