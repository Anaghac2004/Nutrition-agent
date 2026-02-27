import pandas as pd
import numpy as np
from scipy.stats import f_oneway, pearsonr

class HypothesisTester:
    def __init__(self, df):
        self.df      = df
        self.results = []

    def run_all_tests(self):
        print("\n[HYPOTHESIS TESTER] Running daily hypothesis tests...")

        self._anova_test('category', 'calories',
            "Does food category significantly affect calorie content?")
        self._anova_test('category', 'protein',
            "Does food category significantly affect protein content?")
        self._anova_test('category', 'sugar',
            "Does food category significantly affect sugar content?")
        self._anova_test('category', 'fiber',
            "Does food category significantly affect fiber content?")
        self._anova_test('category', 'sodium',
            "Does food category significantly affect sodium content?")
        self._correlation_test('fat', 'calories',
            "Does fat content strongly correlate with calories?")
        self._correlation_test('protein', 'calories',
            "Does protein content correlate with calories?")
        self._correlation_test('sugar', 'calories',
            "Does sugar content correlate with calories?")
        self._correlation_test('carbs', 'calories',
            "Does carbohydrate content correlate with calories?")
        self._correlation_test('fiber', 'sugar',
            "Does fiber content inversely correlate with sugar?")

        print(f"[HYPOTHESIS TESTER] ✅ {len(self.results)} tests completed.")
        return self.results

    def _anova_test(self, group_col, value_col, hypothesis):
        try:
            groups = [
                self.df[self.df[group_col] == g][value_col].dropna()
                for g in self.df[group_col].unique()
            ]
            groups = [g for g in groups if len(g) > 1]
            if len(groups) < 2:
                return

            f, p   = f_oneway(*groups)
            eta2   = self._eta_squared(group_col, value_col)
            sig    = p < 0.005
            effect = self._effect_label_anova(eta2)

            result = {
                'hypothesis'  : hypothesis,
                'test'        : 'ANOVA',
                'statistic'   : round(f, 4),
                'p_value'     : float(p),
                'effect_size' : eta2,
                'effect_name' : 'Eta Squared',
                'effect_label': effect,
                'significant' : sig,
                'var1'        : group_col,
                'var2'        : value_col
            }
            self.results.append(result)
            status = "✅" if sig else "❌"
            print(f"   {status} {hypothesis}")
            print(f"      F={round(f,4)}, p={p:.4e}, "
                  f"Eta²={eta2} [{effect}]")

        except Exception as e:
            print(f"   [ERROR] {hypothesis}: {e}")

    def _correlation_test(self, col1, col2, hypothesis):
        try:
            data     = self.df[[col1, col2]].dropna()
            r, p     = pearsonr(data[col1], data[col2])
            sig      = p < 0.005
            strength = self._effect_label_correlation(abs(r))
            direction = "positive" if r > 0 else "negative"

            result = {
                'hypothesis'  : hypothesis,
                'test'        : 'Pearson Correlation',
                'statistic'   : round(r, 4),
                'p_value'     : float(p),
                'effect_size' : round(abs(r), 4),
                'effect_name' : 'Pearson r',
                'effect_label': strength,
                'significant' : sig,
                'var1'        : col1,
                'var2'        : col2
            }
            self.results.append(result)
            status = "✅" if sig else "❌"
            print(f"   {status} {hypothesis}")
            print(f"      r={round(r,4)} ({direction}), "
                  f"p={p:.4e} [{strength}]")

        except Exception as e:
            print(f"   [ERROR] {hypothesis}: {e}")

    def _eta_squared(self, group_col, value_col):
        try:
            grand_mean = self.df[value_col].mean()
            groups     = [
                self.df[self.df[group_col] == g][value_col].dropna()
                for g in self.df[group_col].unique()
            ]
            ss_between = sum(
                len(g) * (g.mean() - grand_mean) ** 2
                for g in groups
            )
            ss_total = sum(
                (x - grand_mean) ** 2
                for g in groups for x in g
            )
            return round(
                ss_between / ss_total if ss_total > 0 else 0.0, 4
            )
        except:
            return 0.0

    def _effect_label_anova(self, eta2):
        if eta2 >= 0.14:   return "Large Effect"
        elif eta2 >= 0.06: return "Medium Effect"
        elif eta2 >= 0.01: return "Small Effect"
        return "Negligible"

    def _effect_label_correlation(self, r):
        if r >= 0.5:   return "Strong"
        elif r >= 0.3: return "Moderate"
        elif r >= 0.1: return "Weak"
        return "Negligible"