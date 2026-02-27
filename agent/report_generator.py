import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, df, test_results, llm_summary,
                 top_healthy, top_calorie, ranked,
                 compared, timestamp):
        self.df           = df
        self.test_results = test_results
        self.llm_summary  = llm_summary
        self.top_healthy  = top_healthy
        self.top_calorie  = top_calorie
        self.ranked       = ranked
        self.compared     = compared
        self.timestamp    = timestamp

    def generate(self):
        sig   = [r for r in self.test_results if r['significant']]
        lines = []

        lines.append("=" * 70)
        lines.append("   AUTONOMOUS DIET & NUTRITION AGENT — DAILY REPORT")
        lines.append(f"   Date       : {self.timestamp}")
        lines.append(f"   Data Source: USDA FoodData Central API")
        lines.append(f"   Mode       : Fully Automatic — No Human Intervention")
        lines.append("=" * 70)

        # Summary
        lines.append(f"\n📊 TODAY'S DATA SUMMARY")
        lines.append(f"   Total Food Items Analyzed : {len(self.df)}")
        lines.append(f"   Food Categories           : "
                     f"{self.df['category'].nunique()}")
        lines.append(f"   Hypothesis Tests Run      : "
                     f"{len(self.test_results)}")
        lines.append(f"   Significant Findings      : {len(sig)}")

        # WHO Comparison
        lines.append(f"\n🎯 NUTRIENT LEVELS vs WHO DAILY RECOMMENDATIONS")
        lines.append("-" * 70)
        for nutrient, info in self.compared.items():
            lines.append(
                f"   {nutrient:12} : {info['actual']:>8} "
                f"(recommended: {info['recommended']:>5}) "
                f"— {info['percent']:>6}%  {info['status']}"
            )

        # AI Summary
        lines.append(f"\n🤖 AI NUTRITIONIST DAILY ADVICE")
        lines.append("-" * 70)
        lines.append(self.llm_summary)

        # Healthiest foods
        lines.append(f"\n🥗 TODAY'S TOP 10 HEALTHIEST FOODS")
        lines.append("-" * 70)
        lines.append(self.top_healthy.to_string(index=False))

        # Highest calorie foods
        lines.append(f"\n⚠️ TODAY'S TOP 10 HIGHEST CALORIE FOODS")
        lines.append("-" * 70)
        lines.append(self.top_calorie.to_string(index=False))

        # Category ranking
        lines.append(f"\n📈 FOOD CATEGORY RANKING (by avg calories)")
        lines.append("-" * 70)
        lines.append(self.ranked.to_string())

        # Hypothesis results
        lines.append(f"\n🔬 HYPOTHESIS TESTING RESULTS")
        lines.append("-" * 70)
        for i, r in enumerate(self.test_results, 1):
            status = "✅ SIGNIFICANT" if r['significant'] else "❌ NOT SIGNIFICANT"
            lines.append(f"\n  #{i} [{status}]")
            lines.append(f"      Hypothesis : {r['hypothesis']}")
            lines.append(f"      Test       : {r['test']}")
            lines.append(f"      Statistic  : {r['statistic']}")
            lines.append(f"      p-value    : {r['p_value']:.4e}")
            lines.append(
                f"      Effect Size: {r['effect_name']}="
                f"{r['effect_size']} [{r['effect_label']}]"
            )

        lines.append("\n" + "=" * 70)
        lines.append("  [AGENT] Daily analysis complete. Zero manual intervention.")
        lines.append(f"  [AGENT] Next auto-run: Tomorrow 9:00 AM UTC")
        lines.append("=" * 70)

        report = "\n".join(lines)

        # Save to reports folder
        os.makedirs("reports", exist_ok=True)
        safe_time = self.timestamp.replace(' ', '_').replace(':', '-')
        filename  = f"reports/nutrition_report_{safe_time}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"[REPORT] 📄 Saved: {filename}")
        print(report)
        return report, filename