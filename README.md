# Project Setup and Maintenance Guide

This document serves as a quick reference for setting up and maintaining the Django and React weather application.

## Development Environment

### Activate Virtual Environment
To activate the virtual environment and access the project-specific Python packages:
source venv/bin/activate
pip freeze > requirements.txt


### Collect Static Files
Collect all static files required by Django:
python manage.py collectstatic


## Deployment

### Restart Nginx
To apply changes made to the Nginx configuration:
sudo systemctl restart nginx

### Restart Gunicorn
sudo systemctl restart gunicorn

### Edit Nginx Configuration
To edit the Nginx site configuration:
sudo nano /etc/nginx/sites-available/kairos


### Edit Gunicorn Service Configuration
To edit the Gunicorn system service configuration:
sudo nano /etc/systemd/system/gunicorn.service


## SSL Certificate Setup

### Obtain or Renew SSL Certificates with Certbot
To set up or renew SSL certificates for the domain with Let's Encrypt:
sudo certbot --nginx -d kairos.gr -d www.kairos.gr


## Additional Information

- Remember to keep your environment variables updated and secure.
- Ensure proper permissions are set for scripts and execution.
- Regularly update your application dependencies to maintain security and functionality.
nano README.md

