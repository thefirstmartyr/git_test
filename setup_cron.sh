#!/bin/bash
# Setup script for daily world news digest cron job
# Usage: bash setup_cron.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/world_news_digest.py"
LOG_FILE="$SCRIPT_DIR/news_digest.log"

echo "🔧 Setting up World News Digest Cron Job"
echo "========================================"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: world_news_digest.py not found"
    exit 1
fi

# Make script executable
chmod +x "$PYTHON_SCRIPT"

# Get configuration
echo ""
echo "Configuration Required:"
echo ""

read -p "📰 NewsAPI Key (get free from https://newsapi.org): " NEWS_API_KEY
if [ -z "$NEWS_API_KEY" ]; then
    echo "❌ NewsAPI key is required"
    exit 1
fi

read -p "📧 Gmail address to send from: " SENDER_EMAIL
if [ -z "$SENDER_EMAIL" ]; then
    echo "❌ Sender email is required"
    exit 1
fi

read -sp "🔐 Gmail App Password (not regular password): " SENDER_PASSWORD
echo ""
if [ -z "$SENDER_PASSWORD" ]; then
    echo "❌ Gmail password is required"
    exit 1
fi

# Create environment file
ENV_FILE="$SCRIPT_DIR/.env"
cat > "$ENV_FILE" << EOF
export NEWS_API_KEY="$NEWS_API_KEY"
export SENDER_EMAIL="$SENDER_EMAIL"
export SENDER_PASSWORD="$SENDER_PASSWORD"
EOF

chmod 600 "$ENV_FILE"
echo ""
echo "✓ Configuration saved to .env (permissions: 600)"

# Install cron job
echo ""
echo "Installing cron job..."

# Create cron wrapper script
CRON_WRAPPER="$SCRIPT_DIR/run_news_digest.sh"
cat > "$CRON_WRAPPER" << 'EOF'
#!/bin/bash
# Wrapper for cron execution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"
python3 "$SCRIPT_DIR/world_news_digest.py" >> "$SCRIPT_DIR/news_digest.log" 2>&1
EOF

chmod +x "$CRON_WRAPPER"

# Create cron job (5 AM AST = 9 AM UTC during standard time, 8 AM UTC during daylight time)
# Using 8 AM UTC to cover both cases
CRON_CMD="0 8 * * * $CRON_WRAPPER"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$CRON_WRAPPER"; then
    echo "⚠️  Cron job already exists, skipping installation"
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✓ Cron job installed"
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Details:"
echo "  Script: $PYTHON_SCRIPT"
echo "  Wrapper: $CRON_WRAPPER"
echo "  Config: $ENV_FILE"
echo "  Log file: $LOG_FILE"
echo "  Schedule: Daily at 5 AM AST (8 AM UTC)"
echo "  Recipient: soshinycf@gmail.com"
echo ""
echo "To verify installation, run: crontab -l"
echo "To view logs, run: tail -f $LOG_FILE"
echo "To remove, run: crontab -e and delete the line with 'run_news_digest.sh'"
