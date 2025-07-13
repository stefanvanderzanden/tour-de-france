#!/bin/sh
set -e

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "✅ Migrations completed."
