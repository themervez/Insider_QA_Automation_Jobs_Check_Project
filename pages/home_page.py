from selenium.webdriver.common.by import By
from pages.base_page import BasePage

#Anasayfa aksiyonları
class HomePage(BasePage):
    COMPANY_MENU = (By.XPATH, "//a[contains(@class,'dropdown-toggle') and normalize-space(text())='Company']")
    CAREERS_LINK = (By.XPATH, "//a[contains(@href,'/careers/') and contains(@class,'dropdown-sub') and normalize-space(text())='Careers']")

    def open_company_menu(self):
        """Company menüsünü aç (hover; fallback click)"""
        self.log.info("Company menüsü açılıyor (hover -> click fallback).")
        try:
            self.hover_element(*self.COMPANY_MENU)
        except Exception:
            self.click_element(*self.COMPANY_MENU)

    def go_to_careers(self):
        """Careers’a git"""
        self.log.info("Careers linkine tıklanıyor.")
        self.wait_clickable(self.CAREERS_LINK)
        self.click_element(*self.CAREERS_LINK)
