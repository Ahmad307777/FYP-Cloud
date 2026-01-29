import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gleam_backend.settings')
django.setup()

from django.contrib import admin
from surveys.models import Survey

def check_admin():
    print("Checking Django Admin Registry...")
    registry = admin.site._registry
    print(f"Registered Models: {[m.__name__ for m in registry.keys()]}")
    
    if Survey in registry:
        print("SUCCESS: Survey model IS registered in Admin.")
    else:
        print("FAILURE: Survey model is NOT registered.")

if __name__ == "__main__":
    check_admin()
