import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


# Careers sayfası: blokları gösterme ve doğrulama"""
class CareersPage(BasePage):
    LOCATIONS_BLOCK = (By.XPATH, "//h3[contains(@class,'category-title-media') and contains(text(),'Our Locations')]")
    LIFE_AT_INSIDER_BLOCK = (By.XPATH, "//h2[contains(@class,'elementor-heading-title') and contains(text(),'Life at Insider')]")
    TEAM_TITLES = (By.XPATH, "//div[contains(@class,'job-title')]//h3")
    SEE_ALL_TEAMS = (
        By.XPATH,
        "//*[self::a or self::button]"
        "[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'see all teams')]"
    )
    our_locations_block = "Our Locations"
    life_at_insider_block = "Life at Insider"

    def is_locations_block_present(self):
        """Our Locations title'ı döndür"""
        txt = self.get_text(self.LOCATIONS_BLOCK)
        self.log.info("'Our Locations' başlığı bulundu.")
        return txt

    def is_teams_block_present(self) -> bool:
        """En az bir teams title'ı var mı"""
        count = len(self.driver.find_elements(*self.TEAM_TITLES))
        self.log.info(f"Teams bölüm başlık sayısı: {count}")
        return count > 0

    def is_life_block_present(self):
        """Life at Insider title'ı döndür"""
        txt = self.get_text(self.LIFE_AT_INSIDER_BLOCK)
        self.log.info("'Life at Insider' başlığı bulundu.")
        return txt

    # --- Title'ı tam Tepeye hizalama ve bekleme---
    def _show_at_top(self, locator, pause=2.0):
        el = self.wait_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'start'});", el)
        try:
            ActionChains(self.driver).move_to_element(el).pause(0.2).perform()
        except Exception:
            pass
        time.sleep(pause)

    def reveal_sections_top_to_bottom(self, pause_each=2.0, bottom_pause=1.0):
        """Our Locations -> See all teams (varsa) -> Life at Insider -> sayfa sonu"""
        self.log.info("Careers sayfası bölümleri sırayla kullanıcıya gösteriliyor.")
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.6)

        self._show_at_top(self.LOCATIONS_BLOCK, pause=pause_each)

        # See all teams var ise onu tepeye sabitle; yoksa ilk team başlığına in
        sat = self.driver.find_elements(*self.SEE_ALL_TEAMS)
        if sat:
            self._show_at_top(self.SEE_ALL_TEAMS, pause=pause_each)
        else:
            teams = self.driver.find_elements(*self.TEAM_TITLES)
            if teams:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'start'});", teams[0])
                time.sleep(pause_each)

        self._show_at_top(self.LIFE_AT_INSIDER_BLOCK, pause=pause_each)

        #Sayfanın sonuna adım adım in (lazy load içerikler/animasyonlar tetiklenir)
        last_h = -1
        for _ in range(14):
            h = self.driver.execute_script("return document.body.scrollHeight;")
            if h == last_h:
                break
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(bottom_pause)
            last_h = h
        self.log.info("Careers sayfası sonuna kadar scroll tamamlandı.")
