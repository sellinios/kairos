  GNU nano 7.2                                                                                                                                           setup.sh                                                                                                                                                     
#!/bin/bash

# Define database names and user
DB_NAME_PRIMARY="aethradb"
DB_NAME_BACKUP="lagerthadb"
DB_USER="sellinios"
REPO_URL="https://github.com/sellinios/aethra.git"
PROJECT_DIR="aethra"

# Function to terminate connections to a database
terminate_db_connections() {
    local dbname=$1
    psql -U $DB_USER -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${dbname}' AND pid <> pg_backend_pid();"
}

# Function to create a database with PostGIS extension
create_db_with_postgis() {
    local dbname=$1
    psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS ${dbname};"
    psql -U $DB_USER -d postgres -c "CREATE DATABASE ${dbname};"
    psql -U $DB_USER -d ${dbname} -c "CREATE EXTENSION IF NOT EXISTS postgis;"
}

# Terminate connections to the databases
terminate_db_connections $DB_NAME_PRIMARY
terminate_db_connections $DB_NAME_BACKUP

# Create primary and backup databases with PostGIS extension
create_db_with_postgis $DB_NAME_PRIMARY
create_db_with_postgis $DB_NAME_BACKUP

# Clone the repository
if [ -d "$PROJECT_DIR" ]; then
    rm -rf "$PROJECT_DIR"
fi
git clone $REPO_URL

# Change to the project directory
cd $PROJECT_DIR

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

echo "Setup completed successfully."

