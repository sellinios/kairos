#!/bin/bash

# Define directory paths
FRONTEND_DIR=~/kairos/frontend
MAIN_PROJECT_DIR=~/kairos

# Update and upgrade system packages
echo "Updating and upgrading system packages..."
sudo apt update && sudo apt upgrade -y
if [ $? -eq 0 ]; then
    echo "System packages updated and upgraded successfully."
else
    echo "Failed to update and upgrade system packages. Please check the error messages."
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "Frontend directory $FRONTEND_DIR does not exist. Exiting..."
    exit 1
fi

# Navigate to the frontend directory
cd "$FRONTEND_DIR" || exit

# Run npm build
echo "Running npm build..."
npm run build

# Check if npm build was successful
if [ $? -eq 0 ]; then
    echo "npm build successful. Preparing to manage Python dependencies..."

    # Check if main project directory exists
    if [ ! -d "$MAIN_PROJECT_DIR" ]; then
        echo "Main project directory $MAIN_PROJECT_DIR does not exist. Exiting..."
        exit 1
    fi

    # Navigate back to the main project directory to run Django commands and handle Python dependencies
    cd "$MAIN_PROJECT_DIR" || exit

    # Export current Python package dependencies
    pip freeze > requirements.txt
    echo "Python dependencies listed in requirements.txt."

    echo "Running manage.py collectstatic..."
    yes yes | python manage.py collectstatic  # Automatically answer 'yes' to the prompt

    # Check if Django collectstatic was successful
    if [ $? -eq 0 ]; then
        echo "Static files collected successfully. Restarting Gunicorn and Nginx..."

        sudo systemctl restart gunicorn
        if [ $? -eq 0 ]; then
            echo "Gunicorn restarted successfully."
        else
            echo "Failed to restart Gunicorn. Please check the error messages."
        fi

        sudo systemctl restart nginx
        if [ $? -eq 0 ]; then
            echo "Nginx restarted successfully."
        else
            echo "Failed to restart Nginx. Please check the error messages."
        fi
    else
        echo "Failed to collect static files. Please check the error messages."
    fi
else
    echo "Failed to build with npm. Please check the error messages."
fi
