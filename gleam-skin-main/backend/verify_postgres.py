import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gleam_backend.settings')
django.setup()

def verify_postgres():
    print(f"configured Engine: {django.conf.settings.DATABASES['default']['ENGINE']}")
    print(f"Database Name: {django.conf.settings.DATABASES['default']['NAME']}")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            row = cursor.fetchone()
            print(f"Database Version: {row[0]}")
            
            cursor.execute("SELECT count(*) FROM surveys_survey;")
            count = cursor.fetchone()[0]
            print(f"Survey Count in Postgres: {count}")
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    verify_postgres()
