
import sys
import os
import json

# Add backend to path to import ai_helper
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.surveys.ai_helper import robust_json_extract

# Simulated AI response for qualification test
ai_response = """
Certainly! Here is the qualification test JSON:
[
    {
        "question": "What is 2+2?",
        "options": ["3", "4", "5", "6"],
        "correctAnswer": 1
    },
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "correctAnswer": 1
    }
]
I hope this helps!
"""

print("Testing actual robust_json_extract from ai_helper...")
extracted = robust_json_extract(ai_response)
print("\nExtracted String:")
print(f"---START---\n{extracted}\n---END---")

try:
    data = json.loads(extracted)
    print("\nSUCCESS: JSON parsed correctly from ai_helper!")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError as e:
    print(f"\nFAILURE: JSONDecodeError: {e}")
