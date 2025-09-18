import requests
import pandas as pd
import time

API_KEY = "AIzaSyA0JnfxLt5GAbIHoV9dDmszfBbnJsrc1y8"  
CENTERS_CSV = "sri_lanka_30km_centers.csv"  
OUTPUT_CSV = "cargills_outlets.csv"

SEARCH_KEYWORD = "Cargills Food City"
RADIUS = 30000  # 30 km in meters

centers_df = pd.read_csv(CENTERS_CSV)

all_results = []

def fetch_places(lat, lng, keyword, radius=30000):
    """Fetch all results (with pagination) for one center point"""
    results = []
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword,
        "key": API_KEY
    }
    
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "results" in data:
            results.extend(data["results"])
        
        # Pagination
        if "next_page_token" in data:
            time.sleep(2)  # required delay before using next_page_token
            params = {
                "pagetoken": data["next_page_token"],
                "key": API_KEY
            }
        else:
            break
    
    return results

# === MAIN LOOP ===
for i, row in centers_df.iterrows():
    lat, lng = row["lat"], row["lng"]
    print(f"Searching center {i+1}/{len(centers_df)} at {lat},{lng} ...")
    
    try:
        results = fetch_places(lat, lng, SEARCH_KEYWORD, RADIUS)
        for r in results:
            all_results.append({
                "place_id": r.get("place_id"),
                "name": r.get("name"),
                "lat": r["geometry"]["location"].get("lat"),
                "lng": r["geometry"]["location"].get("lng"),
                "address": r.get("vicinity"),
                "rating": r.get("rating"),
                "user_ratings_total": r.get("user_ratings_total"),
                "types": ",".join(r.get("types", []))
            })
    except Exception as e:
        print(f"Error at {lat},{lng}: {e}")
    
    time.sleep(0.5)  # avoid hammering API too fast

df = pd.DataFrame(all_results)
df = df.drop_duplicates(subset=["place_id"])

print(f"Collected {len(df)} unique outlets.")
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved results to {OUTPUT_CSV}")
