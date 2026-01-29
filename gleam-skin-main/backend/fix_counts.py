
import os
import sys
import django

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'survonica_backend.settings')
django.setup()

from surveys.models import Survey, SurveyResponse

def sync_counts():
    print("Starting sync of survey response counts...")
    surveys = Survey.objects.all()
    count = 0
    for survey in surveys:
        # Count actual responses
        actual_count = SurveyResponse.objects(survey=survey).count()
        
        # Update if different
        if survey.response_counter != actual_count:
            print(f"Updating {survey.title}: {survey.response_counter} -> {actual_count}")
            survey.response_counter = actual_count
            survey.save()
            count += 1
            
    print(f"Sync complete. Updated {count} surveys.")

if __name__ == '__main__':
    sync_counts()
