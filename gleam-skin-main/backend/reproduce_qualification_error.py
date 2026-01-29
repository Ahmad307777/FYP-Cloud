
import json
import re

def robust_json_extract(text: str) -> str:
    """
    Current implementation in ai_helper.py (simplified/relevant part)
    """
    if not text:
        return ""
    
    # 1. Try Markdown code block extraction
    json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        # 2. Fallback: Find the first { and last }
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_str = text[start_idx:end_idx+1]
        else:
            json_str = text.strip()
    
    return json_str

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

print("AI Response Summary (first 50 chars):", ai_response.strip()[:50], "...")

extracted = robust_json_extract(ai_response)
print("\nExtracted String:")
print(f"---START---\n{extracted}\n---END---")

try:
    data = json.loads(extracted)
    print("\nSUCCESS: JSON parsed correctly!")
except json.JSONDecodeError as e:
    print(f"\nFAILURE: JSONDecodeError: {e}")

# Proposed FIX
def improved_robust_json_extract(text: str) -> str:
    if not text:
        return ""
    
    # 1. Try Markdown code block extraction
    json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()
    
    # 2. Improved Fallback: Find first [ or { and last ] or }
    first_brace = text.find('{')
    first_bracket = text.find('[')
    
    if first_brace == -1 and first_bracket == -1:
        return text.strip()
    
    if first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket):
        # Starts with an object
        start_idx = first_brace
        end_idx = text.rfind('}')
    else:
        # Starts with a list
        start_idx = first_bracket
        end_idx = text.rfind(']')
        
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        return text[start_idx:end_idx+1]
    
    return text.strip()

print("\n--- Testing Improved Version ---")
extracted_improved = improved_robust_json_extract(ai_response)
print("Extracted (Improved):")
print(f"---START---\n{extracted_improved}\n---END---")

try:
    data = json.loads(extracted_improved)
    print("\nSUCCESS: Improved version parsed correctly!")
except json.JSONDecodeError as e:
    print(f"\nFAILURE: Improved version also failed: {e}")
