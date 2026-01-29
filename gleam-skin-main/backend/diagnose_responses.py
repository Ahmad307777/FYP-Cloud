import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gleam_backend.settings')
django.setup()

from surveys.models import Survey, SurveyResponse

def diagnose():
    surveys = Survey.objects.all()
    print(f"Total Surveys: {surveys.count()}")
    for s in surveys:
        responses = SurveyResponse.objects.filter(survey=s)
        high_quality = responses.filter(quality_score__gte=60)
        print(f"Survey ID: {s.id}, Title: '{s.title}', Total Responses: {responses.count()}, High Quality (>=60): {high_quality.count()}")
        
        if responses.exists():
            first = responses.first()
            print(f"  Example Response Quality Score: {first.quality_score}, Is Flagged: {first.is_flagged}")
            print(f"  Response Data Keys: {list(first.responses.keys()) if first.responses else 'Empty'}")
            print(f"  Survey Questions (Full):")
            for q in s.questions:
                print(f"    - ID: {q.get('id')}, Text: {q.get('text')[:30]}...")

if __name__ == "__main__":
    diagnose()
