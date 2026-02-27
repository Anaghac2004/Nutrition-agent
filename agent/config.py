import os

# ── API Settings ─────────────────────────────────────────────────────
USDA_BASE_URL        = "https://api.nal.usda.gov/fdc/v1"

# ── Analysis Settings ────────────────────────────────────────────────
SIGNIFICANCE_LEVEL   = 0.05
BONFERRONI_N         = 10
BONFERRONI_THRESHOLD = SIGNIFICANCE_LEVEL / BONFERRONI_N

# ── Food categories to fetch daily ───────────────────────────────────
FOOD_CATEGORIES = [
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

# ── Daily recommended values (WHO standards) ─────────────────────────
DAILY_RECOMMENDED = {
    'calories'  : 2000,
    'protein'   : 50,
    'carbs'     : 275,
    'fat'       : 78,
    'fiber'     : 28,
    'sugar'     : 50,
    'sodium'    : 2300,
    'calcium'   : 1300,
    'iron'      : 18,
    'vitamin_c' : 90
}

# ── Report Settings ──────────────────────────────────────────────────
MAX_INSIGHTS         = 10
REPORT_MODE          = "daily"