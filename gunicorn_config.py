import os

workers = int(os.environ.get('GUNICORN_PROCESS', '1'))
threads= int(os.environ.get('GUNICORN_THREADS', '1'))
bind = os.environ.get('GUNICONR_BIND', '0.0.0.0:8080')
forwarded_allow_ips ='*'
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}

