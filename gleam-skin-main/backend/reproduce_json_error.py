
import json
import re

def robust_json_extract(text: str) -> str:
    """
    Extracts and cleans JSON from a string, handling markdown blocks and common syntax errors.
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
    
    # 3. Cleanup common AI JSON errors
    # Remove comments (// ...)
    json_str = re.sub(r'//.*$', '', json_str, flags=re.MULTILINE)
    # Fix trailing commas before closing braces/brackets
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    
    return json_str

# Proposed Improvement
def improved_robust_json_extract(text: str) -> str:
    original = robust_json_extract(text)
    
    # 4. Try to fix missing commas between objects/fields
    # Pass 1: Missing comma between "..." "..." or digit "..." or boolean "..."
    # This is risky but often needed for Llama models that forget commas
    # Regex: Look for value end (quote, digit, true/false/null, bracket) followed by newline/space then quote (key start)
    
    # Insert comma between "End of Value" and "Start of Key" if missing
    # value ends: " or digit or e/l (true/null)
    # key starts: "
    
    fixed = re.sub(r'(["\d\}])\s*\n\s*(")', r'\1,\n\2', original)
    
    return fixed

# Test Cases
malformed_json_1 = """
{
    "title": "Test Survey"
    "questions": []
}
""" # Missing comma after title line

malformed_json_2 = """
{
    "key1": "value1",
    "key2": "value2"
    "key3": "value3"
}
"""

print("--- Test 1 ---")
try:
    print(json.loads(robust_json_extract(malformed_json_1)))
except Exception as e:
    print(f"Original failed as expected: {e}")

try:
    print(json.loads(improved_robust_json_extract(malformed_json_1)))
    print("Improved Succeeded!")
except Exception as e:
    print(f"Improved failed: {e}")

print("\n--- Test 2 ---")
try:
    print(json.loads(improved_robust_json_extract(malformed_json_2)))
    print("Improved Succeeded!")
except Exception as e:
    print(f"Improved failed: {e}")
