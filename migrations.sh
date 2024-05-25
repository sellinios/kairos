#!/bin/bash

# List of apps
apps=("api" "articles" "geography" "weather")

# Step 1: Backup your database
echo "Backing up database..."
# Replace with your actual backup command
pg_dump mydatabase > backup.sql

# Step 2: Fake apply existing migrations
echo "Faking existing migrations..."
python manage.py migrate --fake

# Step 3: Remove existing migrations
echo "Removing existing migrations..."
for app in "${apps[@]}"
do
  migrations_dir="$app/migrations"
  if [ -d "$migrations_dir" ]; then
    find "$migrations_dir" -type f ! -name "__init__.py" -delete
    touch "$migrations_dir/__init__.py"
  else
    echo "Migrations directory for app $app does not exist."
  fi
done

# Step 4: Create new initial migrations
echo "Creating new initial migrations..."
python manage.py makemigrations "${apps[@]}"

# Step 5: Apply new migrations
echo "Applying new migrations..."
python manage.py migrate

echo "Migration cleanup and consolidation complete."
