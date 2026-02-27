import pandas as pd
import numpy as np
from config import DAILY_RECOMMENDED

class DataAnalyzer:
    def __init__(self, df):
        self.df      = df.copy()
        self.summary = {}

    def clean(self):
        print("[ANALYZER] Cleaning nutrition data...")
        self.df.dropna(inplace=True)
        self.df = self.df[self.df['calories'] > 0]
        self.df = self.df[self.df['calories'] < 2000]
        print(f"[ANALYZER] Clean dataset: {len(self.df)} food items")
        return self.df

    def compute_summary(self):
        print("[ANALYZER] Computing daily nutritional summary per category...")
        nutrients    = ['calories', 'protein', 'carbs', 'fat',
                        'fiber', 'sugar', 'sodium']
        self.summary = self.df.groupby('category')[nutrients].agg(
            ['mean', 'median', 'std']
        ).round(2)
        print("[ANALYZER] ✅ Summary computed.")
        return self.summary

    def rank_categories(self):
        print("[ANALYZER] Ranking food categories by nutritional profile...")
        ranked = self.df.groupby('category').agg(
            avg_calories = ('calories', 'mean'),
            avg_protein  = ('protein',  'mean'),
            avg_fiber    = ('fiber',    'mean'),
            avg_sugar    = ('sugar',    'mean'),
            avg_fat      = ('fat',      'mean'),
            food_count   = ('food_name','count')
        ).round(2).sort_values('avg_calories', ascending=False)
        return ranked

    def get_healthiest_foods(self, top_n=10):
        df = self.df.copy()
        df['health_score'] = (
            df['protein'] * 2.0 +
            df['fiber']   * 3.0 -
            df['sugar']   * 1.5 -
            df['fat']     * 0.5
        )
        return df.nlargest(top_n, 'health_score')[
            ['food_name', 'category', 'calories',
             'protein', 'fiber', 'sugar', 'health_score']
        ]

    def get_highest_calorie_foods(self, top_n=10):
        return self.df.nlargest(top_n, 'calories')[
            ['food_name', 'category', 'calories', 'fat', 'sugar']
        ]

    def compare_with_daily_recommended(self):
        print("[ANALYZER] Comparing food averages with WHO daily recommendations...")
        avg      = self.df[list(DAILY_RECOMMENDED.keys())].mean().round(2)
        compared = {}
        for nutrient, recommended in DAILY_RECOMMENDED.items():
            actual  = avg.get(nutrient, 0)
            percent = round((actual / recommended) * 100, 1)
            status  = "✅ OK" if percent <= 100 else "⚠️ HIGH"
            compared[nutrient] = {
                'actual'       : actual,
                'recommended'  : recommended,
                'percent'      : percent,
                'status'       : status
            }
        return compared