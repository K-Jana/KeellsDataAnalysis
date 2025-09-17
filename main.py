from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

API_KEY = 'API-KEY'
BASE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

csv_file = 'keells_stores.csv'
df = pd.read_csv('keells_stores.csv')
print(df.head())

location_column = "address"

place_ids = []
latitudes = []
longitudes = []

for loc in df[location_column]:
    params = {
        "input": f"Keells {loc}",
        "inputtype": "textquery",
        "fields": "place_id,geometry",
        "key": API_KEY
    }
    response = requests.get(BASE_URL, params=params).json()

    if response.get("candidates"):
        candidate = response["candidates"][0]
        place_ids.append(candidate.get("place_id"))
        latitudes.append(candidate["geometry"]["location"]["lat"])
        longitudes.append(candidate["geometry"]["location"]["lng"])
    else:
        place_ids.append(None)
        latitudes.append(None)
        longitudes.append(None)
    
    time.sleep(0.1)  # avoid hitting rate limits

# Insert new columns AFTER the first 4 columns
df.insert(4, "place_id", place_ids)
df.insert(5, "latitude", latitudes)
df.insert(6, "longitude", longitudes)

# Save back to same file (or new file if you prefer safety)
df.to_csv("keells_stores.csv", index=False)

print("Place IDs and coordinates added to keells_stores.csv")
