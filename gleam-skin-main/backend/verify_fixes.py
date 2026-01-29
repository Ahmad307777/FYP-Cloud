
import os
import sys
import json
from unittest.mock import MagicMock, patch

# Add backend to path so we can import surveys.ai_helper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from surveys.ai_helper import robust_json_extract, analyze_survey_quality
    print("SUCCESS: Imported ai_helper")
except ImportError as e:
    print(f"ERROR: Could not import ai_helper: {e}")
    sys.exit(1)

def test_robust_json_extract():
    print("\n--- Testing robust_json_extract ---")
    malformed_json = """
    {
        "title": "Test Survey"
        "questions": []
    }
    """
    try:
        result = robust_json_extract(malformed_json)
        parsed = json.loads(result)
        print("PASS: Handled missing comma")
    except json.JSONDecodeError as e:
        print(f"FAIL: Failed to parse fixed JSON: {e}")
        print(f"Result was: {result}")

def test_analyze_survey_quality():
    print("\n--- Testing analyze_survey_quality (Mocked AI) ---")
    
    questions = [
        {"text": "Q1", "type": "text"},
        {"text": "Header", "type": "section_header"}, # Index 1
        {"text": "Q3", "type": "text"}
    ]
    
    # Mock the AI response to return an issue for the header (Index 1) to see if it gets filtered
    mock_response_json = json.dumps({
        "issues": [
            {"index": 0, "type": "leading", "reason": "bad"},
            {"index": 1, "type": "leading", "reason": "should be ignored"}, # Should be filtered
            {"index": 2, "type": "leading", "reason": "ok"}
        ]
    })
    
    # Mock InferenceClient
    with patch('surveys.ai_helper.InferenceClient') as MockClient:
        instance = MockClient.return_value
        instance.chat_completion.return_value.choices = [
            MagicMock(message=MagicMock(content=mock_response_json))
        ]
        
        # Call the function (api_key needed usually, but mocked client ignores it unless init checks)
        # The function checks os.getenv if key not passed.
        # We'll pass a dummy key
        result = analyze_survey_quality(questions, api_key="dummy_key")
        
        issues = result.get('issues', [])
        print(f"Returned Issues: {len(issues)}")
        
        indices = [i['index'] for i in issues]
        print(f"Returned Indices: {indices}")
        
        if 1 in indices:
            print("FAIL: Section header (Index 1) was NOT filtered out.")
        else:
            print("PASS: Section header was filtered out.")
            
        if 0 in indices and 2 in indices:
            print("PASS: Valid questions were preserved.")
        else:
            print("FAIL: Valid questions were lost.")

if __name__ == "__main__":
    test_robust_json_extract()
    test_analyze_survey_quality()
