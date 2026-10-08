"""
ai_service.py – SkillPath AI Google Gemini Integration
=======================================================
This module handles all communication with the Google Gemini API.

How it works:
  1. Reads GEMINI_API_KEY (required) and GEMINI_MODEL (optional) from .env.
  2. Builds a detailed prompt from the student's profile.
  3. Calls the Gemini API using the official google-genai SDK and parses
     the JSON response.
  4. If the API is unavailable, the key is missing, or a quota/rate limit
     is hit, it returns graceful demo/fallback data so the app still works.

Gemini API docs: https://ai.google.dev/gemini-api/docs
Get a free API key: https://aistudio.google.com/app/apikey
"""

import os
import json
import re
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Default model — gemini-3.5-flash is fast, capable, and available on the free tier.
# You can override this by setting GEMINI_MODEL= in your .env file.
DEFAULT_MODEL = "gemini-3.5-flash"


def _get_api_key() -> str | None:
    """
    Read the Gemini API key from the environment.
    Returns None if the key is missing or empty.
    """
    key = os.getenv("GEMINI_API_KEY", "").strip()
    return key if key else None


def _get_model_name() -> str:
    """
    Return the Gemini model name to use.
    Falls back to DEFAULT_MODEL if GEMINI_MODEL is not set.
    """
    return os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def _build_prompt(profile: dict) -> str:
    """
    Build a detailed prompt for Gemini based on the student's profile.
    The prompt asks for a structured JSON response so we can parse it easily.
    """
    return f"""
You are SkillPath AI, an expert career mentor for college students.

A student has submitted their profile. Analyze it carefully and return a
personalized learning plan in valid JSON (no markdown, no extra text).

=== STUDENT PROFILE ===
Name            : {profile['name']}
Degree / Branch : {profile['degree']}
Current Skills  : {profile['current_skills'] or 'None listed'}
Target Career   : {profile['target_career']}
Experience Level: {profile['experience_level']}
Study Hours/Week: {profile['study_hours']} hours

=== INSTRUCTIONS ===
Return ONLY a valid JSON object with this exact structure:

{{
  "skills_to_learn": [
    "Skill 1 – one-line explanation",
    "Skill 2 – one-line explanation",
    "Skill 3 – one-line explanation",
    "Skill 4 – one-line explanation",
    "Skill 5 – one-line explanation"
  ],
  "roadmap": [
    {{
      "phase": "Phase 1 – <name>",
      "duration": "<timeframe>",
      "topics": ["Topic A", "Topic B", "Topic C"]
    }},
    {{
      "phase": "Phase 2 – <name>",
      "duration": "<timeframe>",
      "topics": ["Topic D", "Topic E", "Topic F"]
    }},
    {{
      "phase": "Phase 3 – <name>",
      "duration": "<timeframe>",
      "topics": ["Topic G", "Topic H", "Topic I"]
    }}
  ],
  "projects": [
    "Project 1 – brief description",
    "Project 2 – brief description",
    "Project 3 – brief description"
  ],
  "weekly_plan": [
    {{"day": "Monday",    "task": "<specific task>"}},
    {{"day": "Tuesday",   "task": "<specific task>"}},
    {{"day": "Wednesday", "task": "<specific task>"}},
    {{"day": "Thursday",  "task": "<specific task>"}},
    {{"day": "Friday",    "task": "<specific task>"}},
    {{"day": "Weekend",   "task": "<specific task>"}}
  ]
}}

Make the advice specific to the student's target career and current skills.
Tailor the weekly plan to fit {profile['study_hours']} study hours per week.
""".strip()


def _extract_json(text: str) -> dict:
    """
    Reliably extract and parse a single JSON object from Gemini's response text.
    Handles:
      - Direct clean JSON
      - Markdown code fences (```json ... ``` or ``` ... ```)
      - Leading commentary or intro text
      - Trailing commentary, extra data, notes, or explanations
    """
    text = text.strip()

    # 1. Direct parse if already a valid JSON string
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # 2. Extract content from markdown code fences if present
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence_match:
        fenced_content = fence_match.group(1).strip()
        try:
            data = json.loads(fenced_content)
            if isinstance(data, dict):
                return data
        except Exception:
            text = fenced_content

    # 3. Use JSONDecoder.raw_decode from the first '{'
    # This parses only the complete JSON object and ignores any trailing data
    decoder = json.JSONDecoder()
    start_pos = 0
    while True:
        idx = text.find("{", start_pos)
        if idx == -1:
            break
        try:
            obj, _ = decoder.raw_decode(text[idx:])
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
        start_pos = idx + 1

    # 4. Fallback to substring between first '{' and last '}'
    first_idx = text.find("{")
    last_idx = text.rfind("}")
    if first_idx != -1 and last_idx != -1 and last_idx > first_idx:
        candidate = text[first_idx : last_idx + 1]
        data = json.loads(candidate)
        if isinstance(data, dict):
            return data

    raise ValueError("No valid JSON object found in response")


def _get_demo_results(profile: dict) -> dict:
    """
    Fallback demo data returned when the API is unavailable or the key
    is missing. This keeps the app functional for demonstration.
    """
    career = profile.get("target_career", "your target career")
    hours = profile.get("study_hours", "5")
    return {
        "skills_to_learn": [
            f"Core technical skills for {career} (demo — add your GEMINI_API_KEY for real results)",
            "Data structures & algorithms – foundation for any tech role",
            "Version control with Git – essential for all developers",
            "Problem-solving & communication – top soft skills employers want",
            "Portfolio building – create projects that showcase your abilities",
        ],
        "roadmap": [
            {
                "phase": "Phase 1 – Foundation",
                "duration": "Month 1–2",
                "topics": ["Core Concepts", "Basic Tools", "Fundamentals"],
            },
            {
                "phase": "Phase 2 – Intermediate",
                "duration": "Month 3–4",
                "topics": ["Applied Skills", "Mini Projects", "Portfolio Building"],
            },
            {
                "phase": "Phase 3 – Advanced",
                "duration": "Month 5–6",
                "topics": ["Real-world Projects", "Interview Prep", "Networking"],
            },
        ],
        "projects": [
            f"Demo Project 1 – Build a beginner project related to {career}",
            "Demo Project 2 – Create a portfolio website showcasing your work",
            "Demo Project 3 – Contribute to an open-source project on GitHub",
        ],
        "weekly_plan": [
            {"day": "Monday",    "task": f"Study core concepts ({hours} hrs/week split across days)"},
            {"day": "Wednesday", "task": "Hands-on coding practice & exercises"},
            {"day": "Friday",    "task": "Review week's learning & fix doubts"},
            {"day": "Weekend",   "task": "Work on your portfolio project"},
        ],
        "_is_demo": True,  # Internal flag — tells the dashboard to show Demo Mode banner
    }


def get_ai_results(profile: dict) -> dict:
    """
    Main function called by app.py.

    Tries to get a real AI response from Google Gemini.
    Falls back to demo data gracefully if anything goes wrong.

    Args:
        profile (dict): The student's profile from the form.

    Returns:
        dict: Structured results with skills, roadmap, projects, weekly plan.
    """
    # Import here so the module still loads even if google-genai is not installed
    try:
        from google import genai
        from google.genai import errors as genai_errors, types as genai_types
    except ImportError:
        print("[SkillPath AI] google-genai package not installed. Run: pip install google-genai")
        return _get_demo_results(profile)

    api_key = _get_api_key()

    # --- No API key configured → return demo data ---
    if api_key is None:
        print("[SkillPath AI] GEMINI_API_KEY not set in .env. Using demo data.")
        return _get_demo_results(profile)

    model_name = _get_model_name()

    try:
        # Create the Gemini client
        client = genai.Client(api_key=api_key)

        prompt = _build_prompt(profile)

        # Call the Gemini API with structured JSON output requested
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        raw_text = response.text.strip()

        # Reliably extract the JSON object, ignoring any extra text or fences
        ai_data = _extract_json(raw_text)

        # Mark as a live AI response (not demo)
        ai_data["_is_demo"] = False
        print(f"[SkillPath AI] Successfully got response from Gemini ({model_name}).")
        return ai_data

    except genai_errors.ClientError as e:
        # Covers 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
        status = getattr(e, "status_code", "unknown")
        if status == 401 or "API_KEY_INVALID" in str(e):
            print("[SkillPath AI] Invalid Gemini API key. Check GEMINI_API_KEY in .env.")
        elif status == 403:
            print("[SkillPath AI] Gemini API access denied (quota or billing issue).")
        else:
            print(f"[SkillPath AI] Gemini API client error ({status}): {e}")
        return _get_demo_results(profile)

    except genai_errors.ServerError as e:
        print(f"[SkillPath AI] Gemini API server error: {e}")
        return _get_demo_results(profile)

    except (json.JSONDecodeError, ValueError) as e:
        print(f"[SkillPath AI] Could not parse Gemini response as JSON: {e}")
        return _get_demo_results(profile)

    except Exception as e:
        print(f"[SkillPath AI] Unexpected error: {e}")
        return _get_demo_results(profile)
