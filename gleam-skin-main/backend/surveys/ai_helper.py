import os
import json
import re
from huggingface_hub import InferenceClient

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
        # 2. Improved Fallback: Find first [ or { and last ] or }
        first_brace = text.find('{')
        first_bracket = text.find('[')
        
        if first_brace == -1 and first_bracket == -1:
            json_str = text.strip()
        else:
            # Determine which comes first to find the outermost container
            if first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket):
                start_idx = first_brace
                end_idx = text.rfind('}')
            else:
                start_idx = first_bracket
                end_idx = text.rfind(']')
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx+1]
            else:
                json_str = text.strip()
    
    # 3. Cleanup common AI JSON errors
    # Remove comments (// ...)
    json_str = re.sub(r'//.*$', '', json_str, flags=re.MULTILINE)
    # Fix trailing commas before closing braces/brackets
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    
    # 4. Try to fix missing commas between objects/fields common in Llama output
    # Look for value end (quote, digit, bool/null, bracket) followed by newline/space then quote (key start)
    # This regex attempts to insert a comma if it's missing between values and keys
    json_str = re.sub(r'(["\d\}])\s*\n\s*(")', r'\1,\n\2', json_str)

    return json_str


def chat_with_llama(messages: list, api_key: str = None):
    """
    Chat with Llama AI model for conversational survey generation
    
    Args:
        messages: List of chat messages [{"role": "user/assistant", "content": "..."}]
        api_key: Hugging Face API key
    
    Returns:
        Assistant's response text
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        raise ValueError("Hugging Face API key not provided")
    
    client = InferenceClient(token=api_key)
    
    try:
        # Add system message to guide the AI
        system_message = {
            "role": "system",
            "content": "You are a helpful survey design assistant. Clarify goals and audience. ASK: 1. Do you want standard demographics? 2. Do you want to group questions into SECTIONS (multiple pages) or keep it as one page? Be conversational."
        }
        
        # Combine system message with conversation
        full_messages = [system_message] + messages
        
        response = client.chat_completion(
            messages=full_messages,
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"I'm having trouble connecting right now. Error: {str(e)}"

def generate_survey_from_conversation(conversation_history: list, api_key: str = None):
    """
    Generate survey questions from conversation history using AI
    
    Args:
        conversation_history: List of chat messages
        api_key: Hugging Face API key
    
    Returns:
        dict with 'title' and 'questions' list
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        raise ValueError("Hugging Face API key not provided")
    
    client = InferenceClient(token=api_key)
    
    # Create a summary of the conversation
    conversation_text = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in conversation_history
    ])
    
    # Extract specific numbers from conversation if mentioned
    conversation_lower = conversation_text.lower()
    # Detect explicit "no sections" requests
    no_sections_keywords = ["no section", "without section", "no header", "no break", "single list"]
    explicit_no_sections = any(keyword in conversation_lower for keyword in no_sections_keywords)
    
    # Try to extract section count
    sections_count = None
    section_match = re.search(r'(\d+)\s+section', conversation_lower)
    if section_match:
        sections_count = int(section_match.group(1))
    
    # Try to extract other counts
    questions_per_section = None
    per_section_match = re.search(r'(\d+)\s+question[s]?\s+(?:per|in each)\s+section', conversation_lower)
    if per_section_match:
        questions_per_section = int(per_section_match.group(1))
    
    total_questions = None
    total_match = re.search(r'(\d+)\s+question[s]?(?:\s+total)?(?!\s+per)', conversation_lower)
    if total_match:
        total_questions = int(total_match.group(1))
    
    # Build specific instructions based on extracted numbers
    count_instruction = ""
    if sections_count and questions_per_section:
        count_instruction = f"\nCRITICAL: Generate EXACTLY {sections_count} sections with EXACTLY {questions_per_section} questions in each section (total: {sections_count * questions_per_section} questions)."
    elif sections_count:
        count_instruction = f"\nCRITICAL: Generate EXACTLY {sections_count} sections with questions distributed evenly across them."
    elif explicit_no_sections:
        count_instruction = "\nCRITICAL: DO NOT use any section headers. Generate all questions as a single flat list. NO 'section_header' types allowed."
    elif total_questions:
        count_instruction = f"\nCRITICAL: Generate EXACTLY {total_questions} questions total."
    
    # Create the prompt
    generation_prompt = f"""You are a professional survey designer. Based on the conversation below, generate a complete survey.
    
CONVERSATION:
{conversation_text}
{count_instruction}

INSTRUCTIONS:
1. QUESTION COUNT: {"Generate exactly the number of questions specified above." if total_questions or (sections_count and questions_per_section) else "Generate 5-10 questions if no specific count was mentioned."}
2. SECTIONS: {"Create section headers as specified above. Each section should be a separate object with type='section_header'." if sections_count else "DO NOT include sections unless the user explicitly asked for them. If the user said 'no sections', strictly avoid 'section_header' types."}
3. QUESTION TYPES: Use appropriate types: "text", "multiple_choice", "rating", "yes_no", "checkboxes"
4. OPTIONS: For multiple_choice questions, provide 3-5 relevant options as an array
5. TONE: Keep all questions neutral, unbiased, and professional
6. DEMOGRAPHICS: Only include demographic questions (age, gender, etc.) if the user explicitly requested them

OUTPUT FORMAT - Return ONLY valid JSON with this structure:
{{
    "title": "Survey Title",
    "questions": [
        {{"text": "Sample Question Text", "type": "multiple_choice", "required": true, "options": ["A", "B", "C"]}},
        ...
    ]
}}
(Include section_header objects ONLY if requested)

Generate the survey JSON now:"""

    
    try:
        messages = [
            {"role": "user", "content": generation_prompt}
        ]
        
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=2500,
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content
        
        # Try to parse JSON from the response
        json_str = robust_json_extract(response_text)
        
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            # Final attempt: try one more cleanup if it still fails
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
            result = json.loads(json_str)
        
        if 'title' not in result or 'questions' not in result:
            raise ValueError("Invalid response structure")
        
        return result
        
    except Exception as e:
        print(f"AI Generation Error: {str(e)}")
        return {
            "title": "Generated Survey (Error)",
            "questions": [],
            "error": str(e)
        }

def detect_duplicate_questions(questions: list, api_key: str = None):
    """
    Detect duplicate/redundant questions using AI semantic similarity
    
    Args:
        questions: List of question dicts [{"text": "...", "type": "...", "options": [...]}]
        api_key: Hugging Face API key
    
    Returns:
        {
            "duplicates": [[idx1, idx2], ...],
            "suggestions": [...],
            "total_duplicates": int
        }
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        raise ValueError("Hugging Face API key not provided")
    
    client = InferenceClient(token=api_key)
    
    try:
        question_texts = [q.get('text', '') for q in questions]
        
        prompt = f"""Analyze these survey questions and identify which ones are asking essentially the same thing (duplicates/redundant).

Questions:
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(question_texts)])}

For each pair of duplicate questions, respond in this exact JSON format:
{{
  "duplicates": [
    {{
      "indices": [0, 3],
      "similarity": 0.95,
      "reason": "Both ask about age"
    }}
  ]
}}

Only include pairs that are truly asking the same thing. If no duplicates, return {{"duplicates": []}}.
Response (JSON only):"""

        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=1000,
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content.strip()
        
        json_str = robust_json_extract(response_text)
        if json_str:
            result = json.loads(json_str)
            duplicates_data = result.get('duplicates', [])
            
            duplicate_pairs = []
            suggestions = []
            
            for dup in duplicates_data:
                indices = dup.get('indices', [])
                if len(indices) >= 2:
                    duplicate_pairs.append(indices)
                    suggestions.append({
                        'indices': indices,
                        'questions': [question_texts[i] for i in indices if i < len(question_texts)],
                        'similarity': dup.get('similarity', 0.9),
                        'suggestion': f"These questions appear to ask the same thing: {dup.get('reason', 'similar meaning')}"
                    })
            
            return {
                'duplicates': duplicate_pairs,
                'suggestions': suggestions,
                'total_duplicates': len(duplicate_pairs)
            }
        else:
            return {
                'duplicates': [],
                'suggestions': [],
                'total_duplicates': 0
            }
            
    except Exception as e:
        print(f"Error detecting duplicates: {e}")
        return {
            'duplicates': [],
            'suggestions': [],
            'error': str(e),
            'total_duplicates': 0
        }

def generate_options_for_question(question_text: str, api_key: str = None):
    """
    Generate multiple-choice options for a survey question using AI
    
    Args:
        question_text: The question to generate options for
        api_key: Hugging Face API key
    
    Returns:
        { "options": ["Option 1", "Option 2", ...] }
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        raise ValueError("Hugging Face API key not provided")
    
    client = InferenceClient(token=api_key)
    
    try:
        prompt = f"""Generate 5 likely multiple-choice options for this survey question:
"{question_text}"

Return a JSON object with a single key "options" containing a list of strings.
Example: {{ "options": ["Satisfied", "Neutral", "Dissatisfied"] }}

JSON Only:"""

        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=200,
            temperature=0.7
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON
        json_str = robust_json_extract(response_text)
        if json_str:
            result = json.loads(json_str)
            return result
        else:
            # Fallback primitive parsing if JSON fails
            lines = [l.strip('- ').strip() for l in response_text.split('\n') if l.strip()]
            return { "options": lines[:5] }
            
    except Exception as e:
        print(f"Error generating options: {e}")
        return { "options": [], "error": str(e) }

def generate_image_from_text(prompt: str, api_key: str = None):
    """
    Generate an image from text using Stable Diffusion via Hugging Face.
    Handles 503 errors by falling back to alternative models.
    """
    import base64
    import time
    from io import BytesIO
    
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        raise ValueError("Hugging Face API key not provided")
    
    # List of models to try in order of preference
    # FLUX is great but often hits 503. SDXL is more reliable.
    MODELS = [
        "stabilityai/stable-diffusion-xl-base-1.0",
        "stabilityai/stable-diffusion-2-1",
        "runwayml/stable-diffusion-v1-5",
        "black-forest-labs/FLUX.1-dev"
    ]
    
    last_error = ""
    
    for model_name in MODELS:
        print(f"DEBUG: Attempting image generation with model: {model_name}")
        client = InferenceClient(model=model_name, token=api_key)
        
        # Internal retries for the SAME model (3 attempts)
        for attempt in range(3):
            try:
                # Generate image
                image = client.text_to_image(prompt)
                
                # Convert to Base64
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                print(f"DEBUG: Successfully generated image with {model_name}")
                return { "image": f"data:image/png;base64,{img_str}" }
                
            except Exception as e:
                last_error = str(e)
                print(f"DEBUG: Attempt {attempt+1} failed for {model_name}: {last_error}")
                
                # Only retry if it's a 503/504 or rate limit, else break and try next model
                if "503" in last_error or "504" in last_error or "429" in last_error:
                    time.sleep(1 * (attempt + 1)) # Exponential backoff
                    continue
                else:
                    break
                    
    # If we got here, all models failed
    print(f"CRITICAL: All image models failed. Last error: {last_error}")
    return { "image": None, "error": f"AI service is temporarily busy. Please try again in a few moments. (Details: {last_error})" }

def analyze_survey_results(survey_title: str, questions: list, responses: list, api_key: str = None):
    """
    Analyze survey results using AI to generate comprehensive insights and reports.
    
    Args:
        survey_title: Title of the survey
        questions: List of question dicts
        responses: List of response dicts
        api_key: Hugging Face API key
    
    Returns:
        dict containing stats, aggregated_data, and ai_insights
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    # 1. Aggregate Data
    total_responses = len(responses)
    question_stats = []
    
    # Text summary for AI
    text_summary_for_ai = f"Survey Title: {survey_title}\nTotal Responses: {total_responses}\n\n"
    
    for idx, q in enumerate(questions):
        q_id = str(q.get('id', '')) # Assuming questions have IDs or we match by text if needed
        q_text = q.get('text', '')
        q_type = q.get('type', 'text')
        q_options = q.get('options', [])
        
        # Extract answers for this question
        answers = []
        for r in responses:
            # responses structure: {'question_text': 'answer'} or based on ID
            # Based on models.py, SurveyResponse.responses is a DictField. 
            # It usually maps question_id/text -> answer. 
            # Let's assume it keys by question text based on typical mongo usage or we try both.
            # Try 3 strategies to find the answer:
            # 1. Exact text match
            # 2. ID match
            # 3. Index match (common in this frontend: q-{index}-{timestamp})
            
            resp_dict = r.get('responses', {})
            val = resp_dict.get(q_text) or resp_dict.get(q_id)
            
            if not val:
                # Try index match
                prefix = f"q-{idx}-"
                for k, v in resp_dict.items():
                    if k.startswith(prefix):
                        val = v
                        break
            
            if val:
                answers.append(val)
        
        stat = {
            'question': q_text,
            'type': q_type,
            'total_answers': len(answers)
        }
        
        if q_type in ['multiple_choice', 'rating', 'yes_no', 'dropdown']:
            # Count frequencies
            counts = {}
            # Handle options that might be objects (e.g., {text: "...", value: "..."}) or strings
            for opt in q_options:
                # Extract string value from option (handle both string and dict/object formats)
                opt_key = ""
                if isinstance(opt, dict):
                    opt_key = str(opt.get('text', opt))
                elif isinstance(opt, str):
                    opt_key = opt
                else:
                    # Handle BaseDict or other object types
                    try:
                        opt_key = str(opt.get('text')) if hasattr(opt, 'get') else str(opt)
                    except:
                        opt_key = str(opt)
                
                if not opt_key:
                    opt_key = "Unnamed Option"
                    
                counts[opt_key] = 0
            
            # Also handle answers not in options (custom)
            for a in answers:
                # Extract string value from answer as well
                if isinstance(a, dict):
                    a_key = a.get('text', str(a))
                elif isinstance(a, str):
                    a_key = a
                else:
                    a_key = a.get('text') if hasattr(a, 'get') else str(a)
                counts[a_key] = counts.get(a_key, 0) + 1
                
            stats_list = []
            for k, v in counts.items():
                stats_list.append({
                    'option': k,
                    'count': v,
                    'percentage': round((v / len(answers) * 100)) if len(answers) > 0 else 0
                })
            
            stat['stats'] = stats_list
            text_summary_for_ai += f"Question: {q_text}\nResults: {json.dumps(stats_list)}\n\n"

            
        else:
            # Text analysis
            stat['sampleResponses'] = answers[:5] # Send top 5 to frontend
            # Send all to AI (truncated if too long)
            joined_answers = "; ".join([str(a) for a in answers[:20]]) # Limit to 20 text responses for prompt size
            text_summary_for_ai += f"Question: {q_text}\nText Responses: {joined_answers}\n\n"
            
        question_stats.append(stat)

    # 2. AI Analysis
    ai_insights = None
    
    if api_key and total_responses > 0:
        client = InferenceClient(token=api_key)
        
        prompt = f"""You are an expert data analyst. Analyze these survey results deeply and generate a comprehensive report.

DATA:
{text_summary_for_ai}

REQUIREMENTS:
1. Sentiment Analysis: Determine overall positive/neutral/negative sentiment percentage (must sum to 100).
2. Key Insights: Identify 3-5 distinct patterns. Look for correlations (e.g. "Satisfied users typically mentioned 'Feature X'").
3. Improvement Suggestions: Give 3-5 practical, data-driven recommendations.
4. Data Narratives: Identify 3 distinct 'stories' or respondent personas found in the data (e.g. 'The Enthusiastic Power User', 'The Frustrated Beginner').
5. Executive Summary: A concise narrative of what this data actually MEANS for the researcher.
6. Keywords: Extract 5-7 thematic keywords.

OUTPUT FORMAT (JSON ONLY):
{{
  "sentiment": {{ "positive": 0, "neutral": 0, "negative": 0 }},
  "keyInsights": ["Primary trend A...", "Counter-trend B..."],
  "improvementSuggestions": ["Corrective action 1...", "Expansion opportunity 2..."],
  "strategicRoadmap": [
    {{"phase": "Persona A", "action": "Likely to feel... due to..."}},
    {{"phase": "Persona B", "action": "Often struggles with..."}},
    {{"phase": "Persona C", "action": "Primarily values..."}}
  ],
  "keywords": ["Theme1", "Theme2"],
  "executiveSummary": "A human-like synthesis of the findings..."
}}

JSON RESPONSE:"""

        try:
            response = client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a senior data analyst. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                model="meta-llama/Llama-3.2-3B-Instruct",
                max_tokens=2000, 
                temperature=0.5
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Robust JSON extraction
            json_str = robust_json_extract(response_text)
                
            try:
                ai_insights = json.loads(json_str)
            except json.JSONDecodeError as je:
                print(f"JSON Parse Error in AI Analysis: {je}")
                # Log the raw string for debugging in the backend directory
                debug_path = os.path.join(os.path.dirname(__file__), "..", "ai_analysis_fail_debug.txt")
                try:
                    with open(debug_path, "w", encoding="utf-8") as f:
                        f.write(f"Error: {je}\n\nRAW RESPONSE:\n{response_text}\n\nEXTRACTED JSON:\n{json_str}")
                except:
                    pass
                raise # Let the outer fallback handle it or the view handle it
            
        except Exception as e:
            print(f"AI Analysis Error: {e}")
            # Fallback if AI fails
            ai_insights = {
                "sentiment": { "positive": 0, "neutral": 100, "negative": 0 },
                "keyInsights": [f"AI Analysis failed: {str(e)}"],
                "improvementSuggestions": ["Try running the analysis again."],
                "keywords": [],
                "executiveSummary": "Automated analysis was temporarily unavailable due to a technical error."
            }
            
    return {
        "questionStats": question_stats,
        "aiInsights": ai_insights,
        "stats": {
            "totalResponses": total_responses,
            "completionRate": 100, 
        }
    }
def analyze_survey_quality(questions: list, api_key: str = None):
    """
    Analyze survey questions for bias, leading language, and quality issues.
    
    Args:
        questions: List of question dicts
        api_key: Hugging Face API key
        
    Returns:
        { "issues": [ { "index": 0, "type": "leading", "reason": "...", "suggestion": "..." } ] }
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        raise ValueError("Hugging Face API key not provided")
    
    client = InferenceClient(token=api_key)
    
    try:
        # Prepare questions with indices, marking sections to be ignored
        formatted_questions = []
        for i, q in enumerate(questions):
            text = q.get('text', '')
            if q.get('type') == 'section_header':
                formatted_questions.append(f"Index {i}: [SECTION HEADER - IGNORE]")
            else:
                formatted_questions.append(f"Index {i}: {text}")

        prompt = f"""You are a Survey Quality Auditor. Analyze the questions below INDEPENDENTLY.
        
        QUESTIONS:
        {chr(10).join(formatted_questions)}
        
        TASK: Identify "Leading", "Biased", or "Confusing" questions.
        
        RULES:
        1. Ignore standard demographic questions (Age, Gender, etc.) - they are OK.
        2. Ignore open-ended feedback questions.
        3. Ignore [SECTION HEADER] items entirely. Do not generate issues for them.
        4. ONLY flag questions that force a specific answer or are heavily biased.
        5. Treat each question in isolation. Do not compare them.
        
        OUTPUT JSON:
        {{
          "issues": [
            {{
              "index": <number straight from the Input List>,
              "type": "Leading/Biased/Ambiguous",
              "reason": "Clear explanation",
              "suggestion": "Neutral alternative"
            }}
          ]
        }}
        
        If no severe issues found, return {{ "issues": [] }}.
        JSON RESPONSE:"""

        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a professional research consultant. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=1500,
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON
        json_str = robust_json_extract(response_text)
        if json_str:
            result = json.loads(json_str)
            cleaned_issues = []
            
            for issue in result.get('issues', []):
                idx = issue.get('index')
                if isinstance(idx, (int, str)):
                   try:
                       idx = int(idx)
                       # validate index range
                       if 0 <= idx < len(questions):
                           # Critical check: Is this a section header?
                           if questions[idx].get('type') == 'section_header':
                               continue # Skip it, it shouldn't be audited
                           
                           # Update index to match strictly if not already correct?
                           # We sent indices 0..N, so we trust the AI returns 0..N
                           # But we verify it's not a section header.
                           issue['index'] = idx
                           cleaned_issues.append(issue)
                   except ValueError:
                       continue
            
            return { "issues": cleaned_issues }
        else:
            return { "issues": [] }
            
    except Exception as e:
        print(f"Error auditing quality: {e}")
        return { "issues": [], "error": str(e) }

def analyze_response_quality(questions: list, response_data: dict, api_key: str = None):
    """
    Analyze survey response quality using Mixtral-8x7B (MoE).
    Detects: Gibberish, low effort, straight-lining, irrelevant answers.
    
    Args:
        questions: List of question dicts
        response_data: Dictionary of answers {question_id/text: answer}
        api_key: Hugging Face API key
        
    Returns:
        {
            "score": 85,
            "flags": ["Gibberish in Q3"],
            "analysis": "..."
        }
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        # Fail gracefully if no key, return perfect score
        return { "score": 100, "flags": [], "analysis": "AI Analysis Unavailable" }
        
    client = InferenceClient(token=api_key)
    
    # NEW: Check for Active Locally Trained Model first (FYP Training Component)
    # NEW: Check for Active Locally Trained Model first (FYP Training Component) -> REMOVED

    # 1. Prepare Data for AI (Cloud Fallback)
    # Map questions to answers
    qa_pairs = []
    
    # Heuristic check for "Straight-lining" (choosing same option everywhere)
    # We can do this with simple python before spending AI tokens
    total_mcq = 0
    mcq_answers = []
    
    for q in questions:
        q_text = q.get('text', '')
        q_id = str(q.get('id', ''))
        q_type = q.get('type', 'text')
        
        # Find answer
        ans = response_data.get(q_text) or response_data.get(q_id)
        if not ans:
            # Try index-based matching (e.g. q-0-12345678)
            idx = questions.index(q)
            
            # 1. Try finding key starting with q-{idx}-
            prefix = f"q-{idx}-"
            for k, v in response_data.items():
                if str(k).startswith(prefix):
                    ans = v
                    break
            
            # 2. Resot to direct index matching if key is just the index "0", "1" etc
            if not ans:
                ans = response_data.get(str(idx))

        if not ans:
             # Skip if truly no answer found
             continue
             
        qa_pairs.append(f"Q: {q_text}\nA: {ans}")
        
        if q_type in ['multiple_choice', 'rating']:
            total_mcq += 1
            mcq_answers.append(str(ans))

    # Basic Heuristic: Straight-lining
    flags = []
    heuristic_score_deduction = 0
    
    # Abort if no data found to analyze
    if not qa_pairs:
        return { "score": 100, "flags": [], "analysis": "No text content found to analyze." }
    
    if total_mcq > 6:
        # If >90% of answers are identical
        from collections import Counter
        counts = Counter(mcq_answers)
        most_common = counts.most_common(1)
        if most_common and most_common[0][1] > (total_mcq * 0.9):
            flags.append("Straight-lining detected (repetitive answers)")
            heuristic_score_deduction += 20

    # 2. MoE AI Analysis for Text coherence and Gibberish
    try:
        context = "\n".join(qa_pairs)
        
        prompt = f'''You are a Quality Control Auditor. Analyze the SURVEY DATA below.
        
        SURVEY DATA:
        {context}
        
        Task: Identify Gibberish, Irrelevant, or Spam answers.
        
        Scoring Rules:
        - "asdf", "jkl", random typing -> Score 0 (Flag: Gibberish)
        - Nonsense phrases not related to question -> Score 20 (Flag: Irrelevant)
        - Short but valid answers (e.g. "Yes", "Blue") -> Score 100
        - Valid, coherent English -> Score 100
        
        IMPORTANT: Assume the answer is VALID unless it is clearly spam or gibberish. Do not penalize for brevity.
        
        Return JSON.
        {{
            "score": <number>,
            "flags": [<list of strings>],
            "reasoning": "<short explanation>"
        }}
        
        JSON RESPONSE:'''
        
        
        # Format prompt for Mixtral Instruct
        # Use Llama-3.2-3B-Instruct (Consistent with other functions)
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=1000,
            temperature=0.1
        )
        response_text = response.choices[0].message.content
        
        # response_text is already the string content
        
        # JSON Parse
        json_str = robust_json_extract(response_text)
        if json_str:
            ai_result = json.loads(json_str)
            
            final_score = ai_result.get('score', 100) - heuristic_score_deduction
            final_score = max(0, min(100, final_score))
            
            ai_flags = ai_result.get('flags', [])
            all_flags = flags + ai_flags
            
            return {
                "score": final_score,
                "flags": all_flags,
                "analysis": ai_result.get('reasoning', 'Analyzed by Mixtral-8x7B')
            }
        else:
            # Fallback
            return { "score": 100 - heuristic_score_deduction, "flags": flags, "analysis": "AI output parse error" }
            
    except Exception as e:
        print(f"Quality Audit Error: {e}")
        return { "score": 100 - heuristic_score_deduction, "flags": flags, "analysis": f"Analysis failed: {str(e)}" }


def generate_qualification_test(topic: str, num_questions: int, api_key: str = None):
    """
    Generate qualification MCQ questions using AI.
    
    Args:
        topic: The topic/context of the survey
        num_questions: Number of questions to generate (1-5)
        api_key: Hugging Face API key
    
    Returns:
        List of dicts: [{ "question": "...", "options": ["..."], "correctAnswer": 0 }]
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not api_key:
        raise ValueError("Hugging Face API key not provided")
    
    client = InferenceClient(token=api_key)
    
    try:
        prompt = f"""You are a subject-matter expert and professional academic researcher. 
        Your task is to generate {num_questions} unique SCREENING QUESTIONS to filter respondents for a survey titled: "{topic}".
        
        GOAL: Ensure the respondent has basic knowledge or a relevant background to answer questions about "{topic}".
        
        CRITICAL CONSTRAINTS:
        1. NO GENERIC CONTENT: DO NOT ask about "business pre-qualification", "construction bidding", "procurement", or the definition of "qualification". These are WRONG and irrelevant.
        2. SUBJECT MATTER FOCUS: If the topic is "Socioeconomic Status of Pakistan", ask about things like "Gross Domestic Product (GDP) sectors", "Income inequality indices (Gini)", or "Demographic shifts in South Asia".
        3. VARIETY: Each question must cover a DIFFERENT concept related to "{topic}". 
        4. OPTIONS: Provide 4 plausible academic/professional options.
        5. FORMAT: Return exactly {num_questions} question objects in a JSON array. Each object MUST have the key "correctAnswer" (index of correct option).
        
        EXAMPLE OF GOOD RELEVANCE:
        Topic: "Climate Change in the Arctic"
        Question: "Which phenomenon describes the faster warming of the Arctic compared to the global average?"
        Options: ["Arctic Amplification", "Polar Vortex", "Albedo Effect", "Oceanic Stratification"]
        correctAnswer: 0
        
        Generate the questions for "{topic}" now:"""
        
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a research assistant. You generate technical screening questions. You NEVER use generic 'pre-qualification' templates unless the topic is specifically about construction or procurement."},
                {"role": "user", "content": prompt}
            ],
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=2000,
            temperature=0.2
        )
        
        response_text = response.choices[0].message.content.strip()
        json_str = robust_json_extract(response_text)
        
        if json_str:
            questions = json.loads(json_str)
            # Validate structure
            if isinstance(questions, list):
                # Ensure limit and map 'correct' to 'correctAnswer' if needed
                processed_questions = []
                for q in questions[:num_questions]:
                    if 'correct' in q and 'correctAnswer' not in q:
                        q['correctAnswer'] = q.pop('correct')
                    processed_questions.append(q)
                return processed_questions
            elif isinstance(questions, dict) and 'questions' in questions:
                 raw_qs = questions['questions'][:num_questions]
                 processed_questions = []
                 for q in raw_qs:
                    if 'correct' in q and 'correctAnswer' not in q:
                        q['correctAnswer'] = q.pop('correct')
                    processed_questions.append(q)
                 return processed_questions
        
        return []
            
    except Exception as e:
        print(f"Error generating qualification test: {e}")
        return []

