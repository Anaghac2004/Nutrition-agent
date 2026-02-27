import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.base      import MIMEBase
from email                import encoders
from datetime             import datetime

class EmailSender:
    def __init__(self):
        self.sender   = os.environ.get("EMAIL_SENDER")
        self.password = os.environ.get("EMAIL_PASSWORD")
        self.receiver = os.environ.get("EMAIL_RECEIVER")

    def send(self, report_text, report_file, timestamp):
        if not all([self.sender, self.password, self.receiver]):
            print("[EMAIL] ⚠️ Email credentials not set. Skipping email.")
            return False

        print(f"[EMAIL] Sending daily report to {self.receiver}...")

        try:
            msg            = MIMEMultipart()
            msg['From']    = self.sender
            msg['To']      = self.receiver
            msg['Subject'] = f"🥗 Daily Nutrition Report — {timestamp[:10]}"

            # Build clean email body
            body = f"""Hello Anagha! 👋

Your Autonomous Diet & Nutrition Agent has completed today's analysis.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QUICK PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{report_text[report_text.find("🤖"):report_text.find("🥗")].strip()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📎 Full detailed report is attached to this email.

This report was generated automatically at {timestamp}.
Next report will arrive tomorrow at 9:00 AM UTC.

Stay healthy! 💪
— Your Autonomous Nutrition Agent 🤖
"""
            msg.attach(MIMEText(body, 'plain'))

            # Attach full report
            with open(report_file, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename=nutrition_report_{timestamp[:10]}.txt'
                )
                msg.attach(part)

            # Send via Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            server.quit()

            print(f"[EMAIL] ✅ Daily report sent to {self.receiver}")
            return True

        except Exception as e:
            print(f"[EMAIL] ❌ Failed: {e}")
            return False