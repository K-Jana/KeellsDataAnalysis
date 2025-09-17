import pandas as pd
import requests
import time

API_KEY = "API-KEY"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

def fetch_ratings_and_reviews(place_ids, store_info=None):
    """
    place_ids: list of place IDs (from CSV)
    store_info: optional list of tuples (store_id, branch) to attach to reviews
    Returns: DataFrame with ratings and reviews
    """
    reviews_data = []

    for idx, pid in enumerate(place_ids):
        if pd.isna(pid):
            continue

        params = {
            "place_id": pid,
            "fields": "rating,user_ratings_total,reviews",
            "key": API_KEY
        }
        response = requests.get(DETAILS_URL, params=params).json()
        result = response.get("result", {})

        avg_rating = result.get("rating")
        num_ratings = result.get("user_ratings_total")
        reviews = result.get("reviews", [])

        # Store summary row (no individual review)
        store_id = store_info[idx][0] if store_info else None
        branch = store_info[idx][1] if store_info else None
        reviews_data.append({
            "store_id": store_id,
            "branch": branch,
            "place_id": pid,
            "avg_rating": avg_rating,
            "num_ratings": num_ratings,
            "review_author": None,
            "review_rating": None,
            "review_text": None
        })

        # Individual reviews
        for r in reviews:
            reviews_data.append({
                "store_id": store_id,
                "branch": branch,
                "place_id": pid,
                "avg_rating": avg_rating,
                "num_ratings": num_ratings,
                "review_author": r.get("author_name"),
                "review_rating": r.get("rating"),
                "review_text": r.get("text")
            })

        time.sleep(0.2)  # avoid hitting API too fast

    return pd.DataFrame(reviews_data)


df = pd.read_csv("keells_stores.csv")

# Optional: pass store_id and branch for mapping reviews
store_info = list(zip(df["place_id"], df["location"]))

reviews_df = fetch_ratings_and_reviews(df["place_id"], store_info)

# Save reviews separately
reviews_df.to_csv("ratings.csv", index=False)
print("Ratings and reviews saved to ratings.csv")
