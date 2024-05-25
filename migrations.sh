#!/bin/bash

# List of custom apps and built-in apps
custom_apps=("api" "articles" "geography" "weather")
builtin_apps=("admin" "auth" "contenttypes" "sessions")

# Step 1: Backup your database
echo "Backing up database..."
# Replace with your actual backup command
pg_dump mydatabase > backup.sql
echo "Database backup completed."

# Step 2: Fake apply existing migrations for all apps
echo "Faking existing migrations for all apps..."
python manage.py migrate --fake
echo "Existing migrations faked."

# Step 3: Remove existing migrations for custom apps
echo "Removing existing migrations for custom apps..."
for app in "${custom_apps[@]}"
do
  migrations_dir="$app/migrations"
  if [ -d "$migrations_dir" ]; then
    find "$migrations_dir" -type f ! -name "__init__.py" -delete
    touch "$migrations_dir/__init__.py"
    echo "Cleaned migrations for $app."
  else
    echo "Migrations directory for app $app does not exist."
  fi
done

# Step 4: Create new initial migrations for custom apps
echo "Creating new initial migrations for custom apps..."
python manage.py makemigrations "${custom_apps[@]}"
echo "New initial migrations created."

# Step 5: Apply new migrations for all apps
echo "Applying new migrations for all apps..."
python manage.py migrate
echo "New migrations applied."

# Ensure built-in apps migrations are correctly applied (if not already)
echo "Ensuring built-in apps migrations are applied..."
for app in "${builtin_apps[@]}"
do
  python manage.py migrate $app
  echo "Migrations applied for $app."
done

echo "Migration cleanup and consolidation complete."
