from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from utils.logger import get_logger


class BasePage(object):
    #Tüm sayfalar için ortak yardımcılar (POM)
    def __init__(self, driver):
        # WebDriver referansı ve varsayılan explicit wait
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.log = get_logger()  # <— tüm page objelerinde hazır

    def find(self, *locator):
        """Tek bir elementi bul"""
        return self.driver.find_element(*locator)

    def click_element(self, *locator):
        """Verilen elementi tıkla (doğrudan)"""
        self.driver.find_element(*locator).click()

    def hover_element(self, *locator):
        """Verilen elementin üzerine gel (hover)"""
        el = self.find(*locator)
        ActionChains(self.driver).move_to_element(el).perform()

    def get_current_url(self):
        """ evcut sayfa URL'ini döndür"""
        return self.driver.current_url

    def wait_clickable(self, locator, message=''):
        """Tıklanabilir olana kadar bekle"""
        return self.wait.until(ec.element_to_be_clickable(locator), message)

    def wait_visible(self, locator, message=''):
        """Görünür olana kadar bekle"""
        return self.wait.until(ec.visibility_of_element_located(locator), message)

    def get_text(self, locator):
        """Title/label gibi metin alanları için görünürlüğe göre text al"""
        return self.wait_visible(locator).text
