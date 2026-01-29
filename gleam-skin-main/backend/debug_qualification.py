
import os
import sys
import django
from mongoengine import connect

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gleam_backend.settings')
django.setup()

from surveys.models import Survey, QualificationTest
from surveys.serializers import QualificationTestSerializer

def debug_association():
    print("--- Debugging Qualification Test Association ---")
    
    # 1. Create Survey
    try:
        survey = Survey(
            user_id="test_user",
            title="Debug Survey for Qual",
            require_qualification=True
        ).save()
        print(f"[SUCCESS] Created Survey: {survey.id}")
    except Exception as e:
        print(f"[FAIL] Creating Survey: {e}")
        return

    # 2. Create Qualification Test linked to Survey
    try:
        input_data = {
            'survey_id': str(survey.id),
            'topic': 'Debug Topic',
            'questions': [
                {'question': 'Is this working?', 'options': ['Yes', 'No'], 'correctAnswer': 0}
            ]
        }
        
        # Use Serializer to create meant to mimic the viewset
        serializer = QualificationTestSerializer(data=input_data)
        if serializer.is_valid():
            q_test = serializer.save()
            print(f"[SUCCESS] Created QualificationTest: {q_test.id}")
        else:
            print(f"[FAIL] Serializer Invalid: {serializer.errors}")
            return
            
    except Exception as e:
        print(f"[FAIL] Creating QualTest: {e}")
        return

    # 3. Query it back using the same logic as ViewSet
    try:
        # Mimic get_queryset logic
        found_survey = Survey.objects.get(id=str(survey.id))
        queryset = QualificationTest.objects.filter(survey=found_survey)
        
        print(f"Found {queryset.count()} tests for this survey.")
        
        if queryset.count() > 0:
            retrieved_test = queryset.first()
            print(f"Retrieved Questions: {retrieved_test.questions}")
            
            # Serialize
            serialized = QualificationTestSerializer(retrieved_test).data
            print(f"Serialized Data: {serialized}")
            
            if not serialized.get('questions'):
                print("[ERROR] Questions missing in serialized data!")
            else:
                print("[SUCCESS] Questions present in serialized data.")
        else:
            print("[ERROR] Could not find the test by survey reference.")
            
    except Exception as e:
        print(f"[FAIL] Querying: {e}")

    # Cleanup
    survey.delete() # Should cascade delete the test
    print("Cleanup done.")

if __name__ == "__main__":
    debug_association()
