"""
ai_service.py – SkillPath AI xAI/Grok Integration
====================================================
This module handles all communication with the xAI (Grok) API.

How it works:
  1. Reads XAI_API_KEY from the .env file (never hard-coded).
  2. Builds a detailed prompt from the student's profile.
  3. Calls the xAI API (OpenAI-compatible) and parses the JSON response.
  4. If the API is unavailable or the key has no credits, returns
     graceful demo/fallback data so the app still works.

xAI API docs: https://docs.x.ai/api
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, PermissionDeniedError, RateLimitError, APIConnectionError

# Load environment variables from the .env file
load_dotenv()


def _get_client():
    """
    Create and return an OpenAI-compatible client pointed at the xAI API.
    Returns None if the API key is missing.
    """
    api_key = os.getenv("XAI_API_KEY", "").strip()
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",  # xAI's OpenAI-compatible endpoint
    )


def _build_prompt(profile: dict) -> str:
    """
    Build a detailed prompt for Grok based on the student's profile.
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


def _get_demo_results(profile: dict) -> dict:
    """
    Fallback demo data returned when the API is unavailable or the key
    has no credits. This keeps the app functional for demonstration.
    """
    career = profile.get("target_career", "your target career")
    hours = profile.get("study_hours", "5")
    return {
        "skills_to_learn": [
            f"Core technical skills for {career} (demo — add your XAI_API_KEY for real results)",
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
        "_is_demo": True,  # Internal flag — used to show a banner in the UI
    }


def get_ai_results(profile: dict) -> dict:
    """
    Main function called by app.py.

    Tries to get a real AI response from xAI/Grok.
    Falls back to demo data if anything goes wrong.

    Args:
        profile (dict): The student's profile from the form.

    Returns:
        dict: Structured results with skills, roadmap, projects, weekly plan.
    """
    client = _get_client()

    # --- No API key configured → return demo data ---
    if client is None:
        print("[SkillPath AI] XAI_API_KEY not set. Using demo data.")
        return _get_demo_results(profile)

    try:
        prompt = _build_prompt(profile)

        response = client.chat.completions.create(
            model="grok-3-mini",        # xAI's fast, cost-efficient model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SkillPath AI, a helpful career mentor. "
                        "Always respond with valid JSON only. No extra text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,            # Slightly creative but focused
            max_tokens=1500,
        )

        raw_text = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model adds them (defensive parsing)
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        ai_data = json.loads(raw_text)

        # Mark as a live AI response (not demo)
        ai_data["_is_demo"] = False
        print("[SkillPath AI] Successfully got response from Grok.")
        return ai_data

    except (AuthenticationError,) as e:
        print(f"[SkillPath AI] API key invalid or unauthorized: {e}")
        return _get_demo_results(profile)

    except (PermissionDeniedError,) as e:
        print(
            "[SkillPath AI] API key has no credits. "
            "Purchase credits at https://console.x.ai then restart the app."
        )
        return _get_demo_results(profile)

    except (RateLimitError,) as e:
        print(f"[SkillPath AI] Rate limit or quota exceeded: {e}")
        return _get_demo_results(profile)

    except (APIConnectionError,) as e:
        print(f"[SkillPath AI] Could not connect to xAI API: {e}")
        return _get_demo_results(profile)

    except json.JSONDecodeError as e:
        print(f"[SkillPath AI] Could not parse AI response as JSON: {e}")
        return _get_demo_results(profile)

    except Exception as e:
        print(f"[SkillPath AI] Unexpected error: {e}")
        return _get_demo_results(profile)
