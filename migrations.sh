#!/bin/bash

# List of custom apps and built-in apps
custom_apps=("api" "articles" "geography" "weather" "gfs_management")
builtin_apps=("admin" "auth" "contenttypes" "sessions")

# Step 1: Remove existing migrations for custom apps
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

# Step 2: Create new initial migrations in the correct order
echo "Creating new initial migrations for geography..."
python manage.py makemigrations geography
if [ $? -ne 0 ]; then
  echo "Failed to create migrations for geography."
  exit 1
fi

echo "Creating new initial migrations for gfs_management..."
python manage.py makemigrations gfs_management
if [ $? -ne 0 ]; then
  echo "Failed to create migrations for gfs_management."
  exit 1
fi

echo "Creating new initial migrations for other apps..."
python manage.py makemigrations articles weather
if [ $? -ne 0 ]; then
  echo "Failed to create migrations for articles and weather."
  exit 1
fi

# Step 3: Apply the migrations
echo "Applying migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
  echo "Failed to apply migrations."
  exit 1
fi

echo "Migrations applied successfully."
