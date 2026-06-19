# 🌍 Daily World News Digest

Automated daily world news digest sent to your email at **5 AM AST**.

## Quick Start

### 1. Get a Free NewsAPI Key
- Visit [https://newsapi.org](https://newsapi.org)
- Sign up (free account)
- Copy your API key

### 2. Get Gmail App Password
- Enable 2-factor authentication on your Gmail account
- Go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Generate an app-specific password for "Mail"
- Copy the 16-character password

### 3. Run Setup Script
```bash
bash setup_cron.sh
```

Follow the prompts to enter:
- NewsAPI Key
- Gmail address (sender)
- Gmail App Password

### 4. Verify Installation
```bash
# Check if cron job is installed
crontab -l

# Monitor logs
tail -f news_digest.log
```

## Files

- **world_news_digest.py** - Main script that fetches and emails headlines
- **setup_cron.sh** - Setup wizard for cron configuration
- **run_news_digest.sh** - Wrapper script executed by cron (created during setup)
- **.env** - Environment configuration (created during setup, keep private)
- **news_digest.log** - Execution logs

## Schedule

- **Time**: 5 AM AST (9 AM UTC)
- **Frequency**: Every day
- **Recipient**: soshinycf@gmail.com
- **Headlines**: Top 10 world news stories from previous day

## Troubleshooting

### Check logs
```bash
tail -20 news_digest.log
```

### Test the script manually
```bash
source .env
python3 world_news_digest.py
```

### Remove cron job
```bash
crontab -e
# Delete the line containing 'run_news_digest.sh'
```

### Gmail app password issues
- Make sure you're using the 16-character app password, not your regular password
- 2FA must be enabled on your Gmail account
- Generate a new password if it's not working

## Notes

- Keep `.env` file private (contains credentials)
- The script uses UTC time (8 AM UTC ≈ 5 AM AST)
- Logs are appended daily to `news_digest.log`
- Failed deliveries are logged but don't stop the system
