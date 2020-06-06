#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/backend')

from app import app as application
