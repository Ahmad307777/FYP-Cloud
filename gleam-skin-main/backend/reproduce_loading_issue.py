import os
import django
from django.conf import settings
import sys

# Add the current directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gleam_backend.settings')
django.setup()

from surveys.models import Survey
from surveys.serializers import SurveyListSerializer
from rest_framework.renderers import JSONRenderer

try:
    print("Fetching all surveys...")
    surveys = Survey.objects.all()
    count = surveys.count()
    print(f"Found {count} surveys.")
    
    if count > 0:
        print("Attempting to serialize first survey...")
        first_survey = surveys.first()
        print(f"First survey ID: {first_survey.id}")
        print(f"First survey title: {first_survey.title}")
        # Check raw attribute access
        try:
             print(f"First survey response_counter (raw): {getattr(first_survey, 'response_counter', 'MISSING')}")
        except Exception as e:
             print(f"Error accessing response_counter: {e}")

        serializer = SurveyListSerializer(first_survey)
        data = serializer.data
        print("Serialization successful for single item:")
        print(data)

        print("Attempting to serialize all surveys...")
        serializer = SurveyListSerializer(surveys, many=True)
        # Force evaluation
        try:
            json_data = JSONRenderer().render(serializer.data)
            print("Serialization successful for all items.")
        except Exception as e:
            print(f"Serialization failed for list: {e}")
            raise e
    else:
        print("No surveys found. This might be why it's 'not loading' if the user expects some.")

except Exception as e:
    print("ERROR OCCURRED:")
    print(e)
    import traceback
    traceback.print_exc()
