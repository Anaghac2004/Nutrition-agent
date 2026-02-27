import requests
import pandas as pd
import os
from datetime import datetime

class DataCollector:
    def __init__(self):
        self.api_key   = os.environ.get("USDA_API_KEY")
        self.base_url  = "https://api.nal.usda.gov/fdc/v1"
        self.df        = None
        self.timestamp = None

    def fetch(self):
        print("[DATA COLLECTOR] Fetching today's nutrition data from USDA...")

        if not self.api_key:
            raise ValueError(
                "[DATA COLLECTOR] ❌ USDA_API_KEY not set in environment."
            )

        all_foods = []

        categories = [
            "Fruits and Fruit Juices",
            "Vegetables and Vegetable Products",
            "Dairy and Egg Products",
            "Poultry Products",
            "Beef Products",
            "Baked Products",
            "Sweets",
            "Fast Foods",
            "Beverages",
            "Snacks",
            "Breakfast Cereals",
            "Legumes and Legume Products"
        ]

        for category in categories:
            print(f"   [FETCHING] {category}...")
            try:
                url    = f"{self.base_url}/foods/search"
                params = {
                    "api_key"    : self.api_key,
                    "query"      : category,
                    "pageSize"   : 25,
                    "pageNumber" : 1
                }
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data  = response.json()
                foods = data.get("foods", [])

                for food in foods:
                    nutrients = {}
                    for n in food.get("foodNutrients", []):
                        name  = n.get("nutrientName", "")
                        value = n.get("value", 0)
                        if "Energy"       in name: nutrients["calories"]  = value
                        if "Protein"      in name: nutrients["protein"]   = value
                        if "Carbohydrate" in name: nutrients["carbs"]     = value
                        if "Total lipid"  in name: nutrients["fat"]       = value
                        if "Fiber"        in name: nutrients["fiber"]     = value
                        if "Sugars"       in name: nutrients["sugar"]     = value
                        if "Sodium"       in name: nutrients["sodium"]    = value
                        if "Calcium"      in name: nutrients["calcium"]   = value
                        if "Iron"         in name: nutrients["iron"]      = value
                        if "Vitamin C"    in name: nutrients["vitamin_c"] = value

                    all_foods.append({
                        "food_name" : food.get("description", "Unknown"),
                        "category"  : category,
                        "calories"  : nutrients.get("calories",  0),
                        "protein"   : nutrients.get("protein",   0),
                        "carbs"     : nutrients.get("carbs",     0),
                        "fat"       : nutrients.get("fat",       0),
                        "fiber"     : nutrients.get("fiber",     0),
                        "sugar"     : nutrients.get("sugar",     0),
                        "sodium"    : nutrients.get("sodium",    0),
                        "calcium"   : nutrients.get("calcium",   0),
                        "iron"      : nutrients.get("iron",      0),
                        "vitamin_c" : nutrients.get("vitamin_c", 0)
                    })

            except Exception as e:
                print(f"   [WARNING] Failed to fetch {category}: {e}")
                continue

        self.df        = pd.DataFrame(all_foods)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[DATA COLLECTOR] ✅ Fetched {len(self.df)} food items "
              f"at {self.timestamp}")
        return self.df