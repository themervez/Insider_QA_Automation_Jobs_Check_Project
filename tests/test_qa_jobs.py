import time
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_jobs_page import QAJobsPage
from pages.job_details_page import JobDetailsPage
from tests.base_test import BaseTest
from utils.screenshot import save_error_screenshot

# E2E smoke test: QA ilanlarını bul, ilkini aç, detayda başlık + Apply CTA kontrol et.
class TestInsiderQAJobs(BaseTest):
    def test_qa_job_flow(self):
        try:
            # 1) Anasayfa
            self.step("Anasayfayı doğrula") # Test Flow'da her adımı loglamak için
            # Test süreci terminal/rapor çıktısında okunur ve takip edilebilir,
            # Test dokümantasyonu işlevini kolaylaştırmak için
            home = HomePage(self.driver)
            self.cookie_reject_if_visible()
            self.assertEqual(self.base_url, home.get_current_url(), "Anasayfa açılamadı")

            # 2) Company -> Careers
            self.step("Company -> Careers navigasyonu")
            home.open_company_menu()
            self.cookie_reject_if_visible()
            home.go_to_careers()

            # 3) Careers bloklarını doğrula + göster
            self.step("Careers bloklarını doğrula ve kullanıcıya göster")
            careers = CareersPage(self.driver)
            self.cookie_reject_if_visible()
            self.assertIn(careers.our_locations_block, careers.is_locations_block_present(), "Locations bloğu yok")
            self.assertTrue(careers.is_teams_block_present(), "Teams bloğu yok")
            self.assertIn(careers.life_at_insider_block, careers.is_life_block_present(), "Life at Insider bloğu yok")
            careers.reveal_sections_top_to_bottom(pause_each=2.0, bottom_pause=1.0)

            # 4) QA Open Positions: filtreleme, listeleme
            self.step("QA Open Positions sayfasına git ve filtrele")
            self.driver.get(QAJobsPage.QA_department_url)
            qa = QAJobsPage(self.driver)
            self.cookie_reject_if_visible()
            qa.select_location_istanbul()
            qa.select_department_qa()
            qa.scroll_to_bottom_until_stable() # Lazy-load tamamlanana kadar kaydır
            time.sleep(0.5)

            jobs = qa.list_jobs()
            self.assertGreater(len(jobs), 0, "Hiç QA ilanı yok")

            # 5) İlk ilanı hover + 'View Role' ile aç
            self.step("İlk ilanda 'View Role' ile detay aç")
            qa.open_first_job_via_view_role()
            self.cookie_reject_if_visible()  # Lever tarafında da banner olabiliyor

            # 6) Detay sayfası: başlık + Apply CTA (Call To Action)
            self.step("Detay sayfasında başlık ve Apply CTA doğrula")
            details = JobDetailsPage(self.driver)
            self.assertIn(details.qa_title, details.get_job_title(), "Pozisyon başlığı beklenen gibi değil")
            self.assertTrue(details.wait_apply_cta_visible(), "'APPLY' CTA(Call To Action) görünmedi (Lever)")
            time.sleep(0.5)

        except Exception:
            """Hata/Assertion durumunda ekran görüntüsü almak için:"""
            path = save_error_screenshot(self.driver, self.__class__.__name__, self._testMethodName)
            print(f"[ERROR] Screenshot kaydedildi: {path}")
            raise
