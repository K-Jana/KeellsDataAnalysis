from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.keellssuper.com/store-locator")

# Wait until at least one store appears
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "store-card"))
)

stores = []

for sc in driver.find_elements(By.CLASS_NAME, "store-card"):
    spans = sc.find_elements(By.CLASS_NAME, "mb-2")
    
    store_data = {"location": "", "address": "", "tel": "", "mobile": ""}

    if len(spans) >= 4:
        # Location
        store_data["location"] = spans[0].text.strip()
        # Address
        store_data["address"] = spans[1].text.strip()
        # Tel
        store_data["tel"] = spans[2].text.replace("Tel:", "").replace("Tel", "").strip()
        # Mobile
        store_data["mobile"] = spans[3].text.replace("Mob:", "").replace("Mobile:", "").strip()
    
    stores.append(store_data)

with open("keells_stores.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["location", "address", "tel", "mobile"])
    writer.writeheader()
    writer.writerows(stores)

print(f"Scraped {len(stores)} stores. Saved to keells_stores.csv")

driver.quit()
