#!/usr/bin/env python3
"""
Daily World News Digest - Fetches and emails top world news headlines
Runs daily at 5 AM AST via cron job
"""

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
import sys

# Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")  # Get from environment variable
EMAIL_ADDRESS = "soshinycf@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")  # Gmail address for sending
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")  # App-specific password

def fetch_world_news():
    """Fetch top world news headlines from the past day"""
    if not NEWS_API_KEY:
        return None, "ERROR: NEWS_API_KEY not set"

    try:
        # Calculate yesterday's date
        yesterday = datetime.utcnow() - timedelta(days=1)
        from_date = yesterday.strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "world news",
            "sortBy": "popularity",
            "language": "en",
            "from": from_date,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        # Get top 10 most impactful headlines
        headlines = []
        for article in articles[:10]:
            headline = {
                "title": article.get("title", ""),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", "")
            }
            headlines.append(headline)

        return headlines, None

    except requests.exceptions.RequestException as e:
        return None, f"Error fetching news: {str(e)}"

def format_email_body(headlines):
    """Format headlines into email body"""
    if not headlines:
        return "No headlines available today."

    body = f"📰 World News Digest - {datetime.now().strftime('%B %d, %Y')}\n"
    body += "=" * 60 + "\n\n"

    for i, article in enumerate(headlines, 1):
        body += f"{i}. {article['title']}\n"
        body += f"   Source: {article['source']}\n"
        body += f"   {article['url']}\n\n"

    body += "=" * 60 + "\n"
    body += "Generated at 5 AM AST daily\n"
    return body

def send_email(headlines):
    """Send email with news digest"""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("ERROR: SENDER_EMAIL and SENDER_PASSWORD environment variables not set")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"🌍 World News Digest - {datetime.now().strftime('%B %d, %Y')}"

        body = format_email_body(headlines)
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"✓ Email sent to {EMAIL_ADDRESS}")
        return True

    except smtplib.SMTPException as e:
        print(f"ERROR: Failed to send email: {str(e)}")
        return False

def main():
    """Main function"""
    print("Fetching world news...")
    headlines, error = fetch_world_news()

    if error:
        print(error)
        sys.exit(1)

    if headlines:
        print(f"Found {len(headlines)} headlines")
        if send_email(headlines):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("No headlines found")
        sys.exit(1)

if __name__ == "__main__":
    main()
