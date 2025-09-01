import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

# QA Open Positions: filtrele, listele, ilk görünür "View Role"u aç
class QAJobsPage(BasePage):
    LOCATION_SELECT = (By.ID, "filter-by-location")
    DEPARTMENT_SELECT = (By.ID, "filter-by-department")
    JOB_CARD = (By.CSS_SELECTOR, "div.position-list-item")

    VIEW_ROLE_IN_CARD = (
        By.XPATH,
        ".//*[self::a or self::button]"
        "[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'view role')]"
    )
    VIEW_ROLE_ANYWHERE = (
        By.XPATH,
        "//*[self::a or self::button]"
        "[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'view role')]"
    )
    QA_department_url = "https://useinsider.com/careers/open-positions/?department=qualityassurance"

    # --- Filtreleme metotları---
    def select_location_istanbul(self):
        """Istanbul lokasyonunu seç"""
        self.log.info("Lokasyon: Istanbul seçiliyor.")
        sel = Select(self.find(*self.LOCATION_SELECT))
        try:
            sel.select_by_visible_text("Istanbul, Turkey")
        except Exception:
            sel.select_by_visible_text("Istanbul, Turkiye")
        time.sleep(0.4)

    def select_department_qa(self):
        """Quality Assurance departmanını seç"""
        self.log.info("Departman: Quality Assurance seçiliyor.")
        Select(self.find(*self.DEPARTMENT_SELECT)).select_by_visible_text("Quality Assurance")
        time.sleep(0.4)

    # --- Liste / scroll metotları ---
    def list_jobs(self):
        """Kartların yüklenmesini bekle ve listeyi döndür"""
        self.log.info("İlan kartları bekleniyor...")
        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(self.JOB_CARD))
        cards = self.driver.find_elements(*self.JOB_CARD)
        self.log.info(f"Toplam {len(cards)} ilan kartı bulundu.")
        return cards

    def scroll_to_bottom_until_stable(self, max_rounds=20, pause=0.8):
        """Sayfa sonuna kaydır ve içerik yüklemesi durana kadar devam et"""
        self.log.info("Lazy-load için sayfa sonuna doğru scroll başlatıldı.")
        prev_count = len(self.driver.find_elements(*self.JOB_CARD))
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        stable = 0
        for _ in range(max_rounds):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
            curr_count = len(self.driver.find_elements(*self.JOB_CARD))
            curr_height = self.driver.execute_script("return document.body.scrollHeight")
            if curr_count == prev_count and curr_height == prev_height:
                stable += 1
            else:
                stable = 0
            prev_count, prev_height = curr_count, curr_height
            if stable >= 2:
                break
        self.log.info(f"Scroll tamamlandı. Son ilan sayısı: {prev_count}")

    # --- Hover + tıkla ---
    def _hover_card(self, card):
        # Kartı orta hizaya getir ve hover et
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
        self.driver.execute_script("window.scrollBy(0, -150);")
        time.sleep(0.2)
        ActionChains(self.driver).move_to_element(card).pause(0.2).perform()

    def _force_click(self, el):
        """Normal → action → JS click sırasıyla dene"""
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        self.driver.execute_script("window.scrollBy(0, -150);")
        time.sleep(0.2)
        try:
            el.click(); return
        except Exception:
            pass
        try:
            ActionChains(self.driver).move_to_element(el).pause(0.1).click().perform(); return
        except Exception:
            pass
        self.driver.execute_script("arguments[0].click();", el)

    def open_first_job_via_view_role(self):
        """İlk kartı hover et; görünür 'View Role' varsa tıkla. Değilse sırayla dene; global fallback."""
        # İlk görünür "View Role" butonunu aç; yeni sekme açılırsa ona geç
        self.log.info("İlk görünür 'View Role' tıklanacak.")
        cards = self.list_jobs()
        if not cards:
            raise AssertionError("Listelenecek iş ilanı bulunamadı.")

        # İlk kart
        self._hover_card(cards[0])
        time.sleep(3.0)  # Filtre sonrası liste DOM güncellenene kadar bekle
        btns = [b for b in cards[0].find_elements(*self.VIEW_ROLE_IN_CARD) if b.is_displayed()]
        if btns:
            self._force_click(btns[0])
        else:
            """Diğer kartları sırayla dene"""
            clicked = False
            for c in cards:
                self._hover_card(c)
                vis = [b for b in c.find_elements(*self.VIEW_ROLE_IN_CARD) if b.is_displayed()]
                if vis:
                    self._force_click(vis[0])
                    clicked = True
                    break
            if not clicked:
                # Global fallback
                WebDriverWait(self.driver, 8).until(EC.presence_of_all_elements_located(self.VIEW_ROLE_ANYWHERE))
                global_vis = [b for b in self.driver.find_elements(*self.VIEW_ROLE_ANYWHERE) if b.is_displayed()]
                if not global_vis:
                    raise AssertionError("'View Role' butonu görünür değil.")
                self._force_click(global_vis[0])

        """Yeni sekmede açıldıysa ona geç"""
        try:
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])
        except Exception:
            pass
        self.log.info("İlan detay sekmesine geçildi.")
