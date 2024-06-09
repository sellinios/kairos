#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define database names and user
DB_NAME_PRIMARY="aethradb"
DB_NAME_BACKUP="lagerthadb"
DB_USER="sellinios"
REPO_URL="https://github.com/sellinios/aethra.git"
PROJECT_DIR="aethra"

# Function to terminate connections to a database
terminate_db_connections() {
    local dbname=$1
    echo "Terminating connections to database: $dbname"
    psql -U $DB_USER -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${dbname}' AND pid <> pg_backend_pid();"
}

# Function to create a database with PostGIS extension
create_db_with_postgis() {
    local dbname=$1
    echo "Creating database: $dbname with PostGIS extension"
    psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS ${dbname};"
    psql -U $DB_USER -d postgres -c "CREATE DATABASE ${dbname};"
    psql -U $DB_USER -d ${dbname} -c "CREATE EXTENSION IF NOT EXISTS postgis;"
}

# Check if necessary commands are available
if ! command -v psql &> /dev/null; then
    echo "psql command not found. Please ensure PostgreSQL is installed and psql is available in PATH."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "git command not found. Please ensure Git is installed and available in PATH."
    exit 1
fi

# Terminate connections to the databases
terminate_db_connections $DB_NAME_PRIMARY
terminate_db_connections $DB_NAME_BACKUP

# Create primary and backup databases with PostGIS extension
create_db_with_postgis $DB_NAME_PRIMARY
create_db_with_postgis $DB_NAME_BACKUP

# Clone the repository
if [ -d "$PROJECT_DIR" ]; then
    echo "Removing existing project directory: $PROJECT_DIR"
    rm -rf "$PROJECT_DIR"
fi

echo "Cloning repository: $REPO_URL"
git clone $REPO_URL

# Change to the project directory
cd $PROJECT_DIR

# Set up Python virtual environment
echo "Setting up Python virtual environment"
python3 -m venv venv

# Check if the virtual environment was created successfully
if [ ! -d "venv" ]; then
    echo "Failed to create virtual environment"
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies"
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations"
python manage.py makemigrations
python manage.py migrate

# Configure Git user details (optional, if required)
echo "Configuring Git user details"
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Add virtual environment activation to .bashrc or .zshrc
echo "Adding virtual environment activation to shell startup file"

if [ -f ~/.bashrc ]; then
    SHELL_RC=~/.bashrc
elif [ -f ~/.zshrc ]; then
    SHELL_RC=~/.zshrc
else
    echo "No suitable shell startup file found (.bashrc or .zshrc)"
    exit 1
fi

ACTIVATION_STRING="source $(pwd)/venv/bin/activate"

# Check if the activation string is already in the file
if ! grep -Fxq "$ACTIVATION_STRING" $SHELL_RC; then
    echo "$ACTIVATION_STRING" >> $SHELL_RC
    echo "Added virtual environment activation to $SHELL_RC"
