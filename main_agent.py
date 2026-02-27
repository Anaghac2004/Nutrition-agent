import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# ── Load .env file ───────────────────────────────────────────────────
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

from data_collector   import DataCollector
from data_analyzer    import DataAnalyzer
from hypothesis_tester import HypothesisTester
from llm_interpreter  import LLMInterpreter
from report_generator import ReportGenerator
from email_sender     import EmailSender


class AutonomousNutritionAgent:
    def __init__(self):
        self.collector = DataCollector()
        self.llm       = LLMInterpreter()
        self.email     = EmailSender()
        self.run_time  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run(self):
        print("\n" + "=" * 70)
        print("     AUTONOMOUS DIET & NUTRITION AGENT — STARTING")
        print(f"     Date      : {self.run_time}")
        print(f"     Mode      : Fully Automatic — No Human Intervention")
        print("=" * 70)

        # Phase 1 — Fetch fresh nutrition data from USDA API
        df = self.collector.fetch()

        # Phase 2 — Clean and analyze
        analyzer     = DataAnalyzer(df)
        df           = analyzer.clean()
        analyzer.compute_summary()
        ranked       = analyzer.rank_categories()
        top_healthy  = analyzer.get_healthiest_foods(top_n=10)
        top_calorie  = analyzer.get_highest_calorie_foods(top_n=10)
        compared     = analyzer.compare_with_daily_recommended()

        # Phase 3 — Run hypothesis tests autonomously
        tester  = HypothesisTester(df)
        results = tester.run_all_tests()

        # Phase 4 — Generate LLM daily advice
        print("\n[AGENT] Generating AI nutritionist daily advice...")
        llm_summary = self.llm.generate_daily_summary(
            results, top_healthy, top_calorie, ranked, compared
        )

        # Phase 5 — Generate and save report
        reporter = ReportGenerator(
            df, results, llm_summary,
            top_healthy, top_calorie,
            ranked, compared, self.run_time
        )
        report_text, report_file = reporter.generate()

        # Phase 6 — Send email automatically
        self.email.send(report_text, report_file, self.run_time)

        print(f"\n[AGENT] ✅ Daily analysis complete!")
        print(f"[AGENT] Report : {report_file}")
        print(f"[AGENT] Email  : Sent to {os.environ.get('EMAIL_RECEIVER')}")
        print(f"[AGENT] Next   : Tomorrow 9:00 AM UTC automatically")


if __name__ == "__main__":
    agent = AutonomousNutritionAgent()
    agent.run()