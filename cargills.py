import requests
import pandas as pd
import time


API_KEY = "API-KEY"
BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

districts = [
    "Colombo", "Gampaha", "Kalutara",
    "Kandy", "Matale", "Nuwara Eliya",
    "Galle", "Matara", "Hambantota",
    "Jaffna", "Kilinochchi", "Mannar", "Vavuniya", "Mullaitivu",
    "Batticaloa", "Ampara", "Trincomalee",
    "Kurunegala", "Puttalam",
    "Anuradhapura", "Polonnaruwa",
    "Badulla", "Monaragala",
    "Ratnapura", "Kegalle"
]

def get_cargills_by_district(district):
    query = f"Cargills Food City {district} Sri Lanka"
    params = {"query": query, "key": API_KEY}
    results = []
    
    while True:
        response = requests.get(BASE_URL, params=params).json()
        results.extend(response.get("results", []))
        
        next_page_token = response.get("next_page_token")
        if not next_page_token:
            break
        time.sleep(2)  # Google requires a delay before using next_page_token
        params = {"pagetoken": next_page_token, "key": API_KEY}
    
    return results

all_places = []

for district in districts:
    print(f"Fetching outlets for {district}...")
    district_results = get_cargills_by_district(district)
    
    for r in district_results:
        all_places.append({
            "district": district,
            "place_id": r.get("place_id"),
            "name": r.get("name"),
            "address": r.get("formatted_address"),
            "lat": r["geometry"]["location"]["lat"],
            "lng": r["geometry"]["location"]["lng"],
            "rating": r.get("rating"),
            "num_ratings": r.get("user_ratings_total")
        })
    
    time.sleep(1)  

df = pd.DataFrame(all_places)
df.to_csv("cargills_stores.csv", index=False)
print(f"Saved {len(df)} outlets to cargills_stores.csv")
