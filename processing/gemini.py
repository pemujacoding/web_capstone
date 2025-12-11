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
            if "quota" in err or "resource_exhausted" in err or "429" in str(e):
                print(f"[ERROR] Gemini quota exceeded: {e}")
                return None  # Quota error → handle sebagai gagal biasa, bukan raise
            elif "503" in err or "overloaded" in err or "UNAVAILABLE" in err:
                wait = 2 * (attempt + 1)
                print(f"[Gemini] Overloaded. Retry {attempt+1}/{retries} in {wait}s...")
                time.sleep(wait)
                continue

            else:
                print(f"[ERROR] Unexpected Gemini error: {e}")
                raise  # Hanya raise kalau bukan quota/overloaded

    raise RuntimeError("Gemini failed after retries.")


PRIMARY_MODEL = "models/gemini-flash-latest"
FALLBACK_MODEL = "models/gemini-2.0-flash"

def gemini_analyze(all_result_stt):

    # serialize data
    video_data = [
        {"id": idx + 1, "question": item["Question"], "answer": item["Answer"]}
        for idx, item in enumerate(all_result_stt)
    ]

    total_items = len(video_data)

    # generate dynamic score template for Gemini
    dynamic_score_template = ",\n        ".join(
        [f'{{"id": {i+1}, "score": x, "reason": str}}' for i in range(total_items)]
    )

    # Dynamic prompt for Gemini
    prompt = f"""
        You are a strict, experienced technical interviewer for senior-level positions.

        There are {total_items} interview question(s) with candidate answers.

        Data:
        {json.dumps(video_data, indent=2)}

        RUBRIC (0–4) - Be very strict:
        - Score 4: Exceptional – Perfect depth, flawless explanation, shows deep expertise (rare, <10% cases).
        - Score 3: Good – Solid understanding, clear, minor gaps acceptable.
        - Score 2: Fair – Basic answer, lacks depth or clarity.
        - Score 1: Poor – Vague, incomplete, or partially incorrect.
        - Score 0: Fail – Irrelevant, wrong, or no meaningful answer.

        Examples:
        Q: Explain how backpropagation works.
        A: "It's when the model learns from mistakes."
        → Score 2 (too general)

        Q: Describe CNN architecture.
        A: "It's layers like conv, pooling, fully connected."
        → Score 3 (correct but lacks detail)

        Q: Explain attention mechanism in detail with equations.
        A: Full correct explanation with scaled dot-product, multi-head, etc.
        → Score 4 (only if truly excellent)

        IMPORTANT RULES:
        - Most candidates get 2–3. Only give 4 if truly outstanding.
        - Do NOT give all 4s unless the candidate is exceptional in every answer.
        - Be critical and objective.
        - For `reason`: 15–25 words, justify why this score (not higher/lower).

        Your task:
        1. Score EACH question using that rubric.
        2. Produce JSON output ONLY in this exact format:

        {{
            "minScore": 0,
            "maxScore": 4,
            "scores": [
                {dynamic_score_template}
            ],
            "communication_score": 0,
            "english_fluency_score": 0,
            "content_quality_score": 0
        }}

        RULES:
        - Output must be PURE JSON only.
        - `score` must ONLY be a number 0–4 (no extra text).
        - Do NOT add or remove fields. Match the format exactly.
        - communication_score MUST be an integer between 0 and 100.
        - english_fluency_score MUST be an integer between 0 and 100.
        - content_quality_score MUST be an integer between 0 and 100.
        - Do NOT write "0-100" in the output. Only output real integers.
        - Do not  use ```json ... ``` blocks.
        - Do NOT explain anything. Output ONLY the JSON.
        - For `reason`, provide a brief explanation (max 20 words) justifying the score.
    """
    try:
        response = safe_generate(PRIMARY_MODEL, prompt)
    except Exception:
        print("[Gemini] Primary model failed. Trying fallback...")
        response = safe_generate(FALLBACK_MODEL, prompt)

    return response.text
