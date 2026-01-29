import requests
import json

def test_audit_quality():
    url = "http://localhost:8000/api/ai/audit-quality/"
    
    # Test questions: one neutral, one biased/leading
    questions = [
        {"text": "What is your favorite color?", "type": "text"},
        {"text": "Don't you think our customer service is the best in the world?", "type": "text"},
        {"text": "How many times a day do you use our amazing product?", "type": "text"}
    ]
    
    print(f"Testing quality audit with {len(questions)} questions...")
    
    try:
        response = requests.post(url, json={"questions": questions})
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\nAI Audit Results:")
            print(json.dumps(result, indent=2))
            
            issues = result.get('issues', [])
            if len(issues) > 0:
                print(f"\n✅ Success: Found {len(issues)} quality issues.")
            else:
                print("\n❌ Failure: Should have found issues in leading questions.")
        else:
            print(f"\n❌ Error: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Request failed: {e}")

if __name__ == "__main__":
    test_audit_quality()
