#  Jobs Check Automation Project

End-to-end test automation project using **Python**, **Selenium**
and **Page Object Model (POM)**

---

## 📂 Proje Yapısı

```
QA_Jobs_Check_Project/
├── pages/
│   ├── base_page.py         # Base POM sınıfı (click, wait, hover, get_text vb.)
│   ├── home_page.py         # Ana sayfa (Company → Careers navigasyonu)
│   ├── careers_page.py      # Careers sayfası ('Our Locations', 'Teams', 'Life at Insider' blokları görünürlüğü kontrol)
│   ├── qa_jobs_page.py      # QA Open Positions (filtreleme, listeleme, View Role)
│   └── job_details_page.py  # İş detayları (başlık ve Apply CTA doğrulama)
│
├── tests/
│   ├── base_test.py         # WebDriver setup/teardown, cookie yönetimi, step loglama
│   └── test_qa_jobs.py      # End-to-End smoke test
│
├── utils/
│   ├── logger.py            # Projenin genelinde kullanılan logging helper
│   ├── screenshot.py        # Hatalarda ekran görüntüsü kaydı
│   └── screenshots/
│       └── error_screenshots/
│           └── YYYY-MM-DD/  # Tarihe göre gruplanan hata ekran görüntüleri
│
└── README.md                # Proje açıklaması
```

---

## 🧩 Özellikler

- 💠 **Page Object Model (POM)** ile modüler yapı
- ⏱️ **Explicit Wait** kullanımı (WebDriverWait + EC)
- 📋 **Logging helper** ile test adımları terminalde izlenebilir
- 🧠 **Smart Scroll**: Lazy-load tamamlanana kadar sayfayı scroll eder
- 📸 **Hatalarda otomatik screenshot alımı** (tarih bazlı klasörlere)
- 🍪 **Cookie banner reddetme** (Türkçe ve İngilizce destekli)
- ⚙️ Kolayca **CI/CD** sistemlerine entegre edilebilir.

---

## 🔍 Test Senaryosu (E2E Akış)

1. Anasayfa açılır ve doğrulanır  
2. Company → Careers navigasyonu yapılır  
3. Careers sayfasındaki bloklar doğrulanır:
   - Our Locations
   - Teams
   - Life at Insider
4. QA Open Positions sayfasında:
   - Location = Istanbul
   - Department = Quality Assurance
5. Lazy-load scroll yapılır, ilanlar listelenir  
6. İlk iş ilanı “View Role” ile açılır  
7. İlan detayında:
   - Pozisyon başlığı doğrulanır
   - "Apply" butonu kontrol edilir

---

## 🖼️ Screenshot Yönetimi

- Hatalı testlerde `utils/screenshots/error_screenshots/YYYY-MM-DD/` içine kaydedilir.
- Dosya adı formatı:  
  `ClassName.MethodName_YYYYmmdd_HHMMSS.png`

---
