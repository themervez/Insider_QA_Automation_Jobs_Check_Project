import os
from datetime import datetime

def save_error_screenshot(driver, test_class: str, test_method: str,
                          root: str = os.path.join("utils", "screenshots", "error_screenshots")) -> str:
    """Hata anında ekran görüntüsü alır ve şuraya kaydeder:
      utils/screenshots/error_screenshots/YYYY-MM-DD/Class.Method_YYYYmmdd_HHMMSS.png
    """
    # Gün bazlı klasör: utils/screenshots/error_screenshots/2025-02-28
    day_folder = datetime.now().strftime("%Y-%m-%d")
    target_dir = os.path.join(root, day_folder)
    os.makedirs(target_dir, exist_ok=True)

    # Dosya adı: Class.Method_YYYYmmdd_HHMMSS.png
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_class}.{test_method}_{ts}.png"

    path = os.path.join(target_dir, filename)
    driver.save_screenshot(path)
    return path
