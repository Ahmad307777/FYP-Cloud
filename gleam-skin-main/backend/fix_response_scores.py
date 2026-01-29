import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gleam_backend.settings')
django.setup()

from surveys.models import SurveyResponse
from surveys.ai_helper import analyze_response_quality

def fix_responses():
    responses = SurveyResponse.objects.filter(quality_score=0)
    print(f"Found {responses.count()} responses with score 0. Reprocessing...")
    
    for r in responses:
        try:
            if r.survey:
                questions = r.survey.questions
                # Re-run audit with new logic
                audit_result = analyze_response_quality(questions, r.responses)
                
                old_score = r.quality_score
                r.quality_score = audit_result.get('score', 100)
                r.quality_analysis = audit_result
                r.is_flagged = r.quality_score < 60
                r.save()
                
                print(f"Response ID: {r.id}, Old Score: {old_score}, New Score: {r.quality_score}, Flagged: {r.is_flagged}")
        except Exception as e:
            print(f"Error reprocessing response {r.id}: {e}")

if __name__ == "__main__":
    fix_responses()
