from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

# İlan detay doğrulamaları: Title ve Apply CTA(Call To Action)
class JobDetailsPage(BasePage):
    JOB_TITLE = (By.CSS_SELECTOR, "h1, h2")  # Tema farkı için h1/h2
    APPLY_CTA = (
        By.XPATH,
        "//*[self::a or self::button]"
        "[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'apply for this role') "
        " or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'apply for this job') "
        " or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'apply now')]"
    )

    qa_title = "Quality Assurance"

    def get_job_title(self, timeout=15):
        """Görünür başlık metnini döndür"""
        self.log.info("İlan başlığı bekleniyor...")
        title = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.JOB_TITLE)
        ).text
        self.log.info(f"Bulunan başlık: {title!r}")
        return title

    def wait_apply_cta_visible(self, timeout=15) -> bool:
        """Apply CTA görünene kadar bekle"""
        self.log.info("Apply CTA bekleniyor...")
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.APPLY_CTA)
        )
        self.log.info("Apply CTA göründü.")
        return True
