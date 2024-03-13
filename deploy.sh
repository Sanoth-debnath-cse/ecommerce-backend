 
#!/bin/bash
set -e

echo "Deployment started ..."

# Logging function
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Pull the latest version of the app
log "Pulling latest changes from Git..."
git pull origin main
log "Changes pulled successfully."

log "activate virtualnev"
source venv/bin/activate

log "Clearing cache..."
cd projectile
python manage.py clean_pyc
python manage.py clear_cache


log "Installing dependencies..."
pip install -r ../requirements/development.txt --no-input

# log "Collecting static files..."
# python manage.py collectstatic --noinput

log "Running database makemigrations."
python manage.py makemigrations

log "Running database migration..."
python manage.py migrate

log "virualenv deactivate"
deactivate

log "Reloading app..."
ps aux | grep gunicorn | grep ecommerce-backend | awk '{ print $2 }' | xargs kill -HUP


log "Deployment Finished !"
