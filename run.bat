set DJANGO_SETTINGS_MODULE=config.settings
daphne -b 127.0.0.1 -p 8000 config.asgi:application