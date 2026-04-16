"""Basic example: env-driven settings with validation."""
import os

def load_settings():
    app = os.getenv('APP_NAME', 'backend-service')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('PORT', '8000'))
    if not 1 <= port <= 65535:
        raise ValueError('invalid port')
    return {'app_name': app, 'debug': debug, 'port': port}

os.environ.setdefault('APP_NAME', 'module13-demo')
os.environ.setdefault('DEBUG', 'true')
os.environ.setdefault('PORT', '9000')
print(load_settings())
