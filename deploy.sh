#!/bin/bash

echo "🚀 Starting deploy..."

# Pull latest code
echo "📥 Pulling latest code..."
git pull

# Activate venv
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install updated requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Collect static files
echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

# Restart Gunicorn
echo "🔁 Restarting Gunicorn..."
systemctl restart gunicorn

echo "✅ Deploy complete!"
