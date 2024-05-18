#!/bin/bash
# Navigate to the frontend directory
# shellcheck disable=SC2164
cd ~/kairos/frontend

# Run npm build
echo "Running npm build..."
npm run build

# Check if npm build was successful
# shellcheck disable=SC2181
if [ $? -eq 0 ]; then
    echo "npm build successful. Preparing to manage Python dependencies..."

    # Navigate back to the main project directory to run Django commands and handle Python dependencies
    cd ~/kairos

    # Export current Python package dependencies
    pip freeze > requirements.txt
    echo "Python dependencies listed in requirements.txt."

    echo "Running manage.py collectstatic..."
    yes yes | python manage.py collectstatic  # Automatically answer 'yes' to the prompt

    # Check if Django collectstatic was successful
    # shellcheck disable=SC2181
    if [ $? -eq 0 ]; then
        echo "Static files collected successfully. Restarting Nginx..."
        sudo systemctl restart nginx
        # shellcheck disable=SC2181
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
