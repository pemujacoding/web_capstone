import json
import os
import time

# all_result_stt contoh
# all_result_stt = [
#     {"Question": "...", "Answer": "..."},
#     ...
# ]

# Tambahkan id otomatis

from google import genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

try :
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
        print(f"Error creating Gemini client: {e}")

def safe_generate(model, prompt, retries=5):
    for attempt in range(retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=prompt
            )
        except Exception as e:
            err = str(e)

            # Kalau overload / 503 → retry
            if "UNAVAILABLE" in err or "overloaded" in err or "503" in err:
                wait = 2 * (attempt + 1)
                print(f"[Gemini] Overloaded. Retry {attempt+1}/{retries} in {wait}s...")
                time.sleep(wait)
                continue

            # Kalau error bukan overload → lempar ulang
            raise

    raise RuntimeError("Gemini failed after retries.")


PRIMARY_MODEL = "models/gemini-flash-latest"
FALLBACK_MODEL = "models/gemini-2.5-flash"

def gemini_analyze(all_result_stt):

    # serialize data
    video_data = [
        {"id": idx + 1, "question": item["Question"], "answer": item["Answer"]}
        for idx, item in enumerate(all_result_stt)
    ]

    # Prompt untuk Gemini
    prompt = f"""
    You are an interview assessment engine.

    There are interview videos. Each contains:
    1) The question spoken by the interviewer
    2) The candidate's answer

    Here is the extracted STT content for each video (already cleaned):

    {json.dumps(video_data, indent=2)}

    You must evaluate the candidate based on the official rubric below:

    RUBRIC SCORING (0–4):
    Score 4 = Comprehensive, very clear, technically strong
    Score 3 = Specific explanation with basic understanding
    Score 2 = General response with limited details
    Score 1 = Minimal or vague response
    Score 0 = Unanswered or irrelevant

    Your task:
    1. Score each question using that rubric.
    2. Produce JSON output ONLY in this format:

    {{
    "minScore": 0,
    "maxScore": 4,
    "scores": [
        {{"id": 1, "score": x}},
        {{"id": 2, "score": x}},
        {{"id": 3, "score": x}},
        {{"id": 4, "score": x}},
        {{"id": 5, "score": x}}
    ],
    "communication_score": 0-100,
    "english_fluency_score": 0-100,
    "content_quality_score": 0-100
    }}

    Rules:
    - Output must be PURE JSON with no explanation.
    - The `score` must be only the rubric (0–4). No reasoning.
    """

    try:
        response = safe_generate(PRIMARY_MODEL, prompt)
    except Exception:
        print("[Gemini] Primary model failed. Trying fallback...")
        response = safe_generate(FALLBACK_MODEL, prompt)
    
    return response.text
