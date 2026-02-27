import os
from groq import Groq

class LLMInterpreter:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("[LLM] ⚠️ GROQ_API_KEY not set. Using rule-based fallback.")
            self.client = None
        else:
            self.client = Groq(api_key=api_key)
            print("[LLM] ✅ Groq LLM connected.")

    def generate_daily_summary(self, test_results, top_healthy,
                                top_calorie, ranked, compared):
        if self.client is None:
            return self._rule_based_summary(test_results)

        sig_results = [r for r in test_results if r['significant']]

        # Build WHO comparison text
        who_lines = []
        for nutrient, info in compared.items():
            who_lines.append(
                f"  {nutrient}: {info['actual']} "
                f"(recommended {info['recommended']}) "
                f"— {info['percent']}% {info['status']}"
            )
        who_text = "\n".join(who_lines)

        prompt = f"""You are a professional nutritionist and personal diet coach.
Today's automated nutrition data analysis results:

SIGNIFICANT FINDINGS ({len(sig_results)} found):
{self._format_results(sig_results)}

TODAY'S NUTRIENT LEVELS vs WHO DAILY RECOMMENDATIONS:
{who_text}

TOP 5 HEALTHIEST FOODS TODAY:
{top_healthy[['food_name','calories','protein','fiber']].head().to_string()}

TOP 5 HIGHEST CALORIE FOODS TODAY:
{top_calorie[['food_name','calories','fat','sugar']].head().to_string()}

Write a friendly, practical DAILY DIET REPORT with:
1. 📊 TODAY'S NUTRITION SNAPSHOT (2-3 sentences)
2. ✅ WHAT TO EAT TODAY (3 specific food recommendations)
3. ❌ WHAT TO AVOID TODAY (2 specific foods to limit)
4. 💡 TODAY'S HEALTH TIP (1 actionable tip)
5. 🎯 DAILY HEALTH SCORE (X/10 with brief reason)

Be specific, friendly, and motivating. Under 200 words."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.4
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[LLM] API error: {e}. Using fallback.")
            return self._rule_based_summary(test_results)

    def _format_results(self, results):
        lines = []
        for r in results:
            lines.append(
                f"- {r['hypothesis']} "
                f"({r['test']}, {r['effect_name']}="
                f"{r['effect_size']} [{r['effect_label']}])"
            )
        return "\n".join(lines)

    def _rule_based_summary(self, results):
        sig   = [r for r in results if r['significant']]
        lines = [
            "DAILY NUTRITION REPORT",
            f"Significant findings: {len(sig)}/{len(results)}"
        ]
        for r in sig:
            lines.append(
                f"• {r['hypothesis']} "
                f"({r['effect_name']}={r['effect_size']} "
                f"[{r['effect_label']}])"
            )
        return "\n".join(lines)