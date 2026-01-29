
import os
import sys
import django
from dotenv import load_dotenv

# Setup Django standalone
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv('backend/.env')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gleam_backend.settings")
django.setup()

from surveys.ai_helper import analyze_response_quality

def test_quality_audit():
    print("Testing AI Quality Auditor with Mixtral...")
    
    # 1. Test Good Response
    good_questions = [
        {'id': '1', 'text': 'How satisfied are you?', 'type': 'rating'},
        {'id': '2', 'text': 'What did you like most?', 'type': 'text'}
    ]
    good_responses = {
        'How satisfied are you?': '5',
        'What did you like most?': 'The user interface was very clean and intuitive.'
    }
    
    print("\n--- Analyzing Good Response ---")
    result_good = analyze_response_quality(good_questions, good_responses)
    print(f"Score: {result_good.get('score')}")
    print(f"Flags: {result_good.get('flags')}")
    print(f"Analysis: {result_good.get('analysis')}")
    
    # 2. Test Bad (Gibberish) Response
    bad_questions = [
        {'id': '1', 'text': 'Describe your experience', 'type': 'text'},
        {'id': '2', 'text': 'Any suggestions?', 'type': 'text'}
    ]
    bad_responses = {
        'Describe your experience': 'asdf asdf asdf jkl',
        'Any suggestions?': 'no text just random'
    }
    
    print("\n--- Analyzing Bad Response ---")
    result_bad = analyze_response_quality(bad_questions, bad_responses)
    print(f"Score: {result_bad.get('score')}")
    print(f"Flags: {result_bad.get('flags')}")
    print(f"Analysis: {result_bad.get('analysis')}")

if __name__ == "__main__":
    test_quality_audit()
