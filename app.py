"""
SkillPath AI – Personalized Career & Skill Mentor
Backend: Flask web server

This is the main entry point for the application.
It handles two routes:
  - "/" (Home): Shows the student profile form.
  - "/dashboard": Receives form data and shows the results dashboard.

AI integration will be added in the next stage.
"""

from flask import Flask, render_template, request, session
import json

# Create the Flask app
app = Flask(__name__)

# Secret key needed to use Flask sessions (stores data between pages)
app.secret_key = "skillpath-ai-secret-key-change-this-later"


@app.route("/", methods=["GET"])
def index():
    """
    Home page — shows the student profile form.
    """
    return render_template("index.html")


@app.route("/dashboard", methods=["POST"])
def dashboard():
    """
    Dashboard page — receives form data and displays the results.
    In this version, the AI results are shown as placeholders.
    Real AI output will be added in the next stage.
    """
    # Collect form data submitted by the student
    student_profile = {
        "name": request.form.get("name", "").strip(),
        "degree": request.form.get("degree", "").strip(),
        "current_skills": request.form.get("current_skills", "").strip(),
        "target_career": request.form.get("target_career", "").strip(),
        "experience_level": request.form.get("experience_level", "Beginner"),
        "study_hours": request.form.get("study_hours", "5"),
    }

    # Split the comma-separated skills into a clean list
    skills_list = [
        skill.strip()
        for skill in student_profile["current_skills"].split(",")
        if skill.strip()
    ]
    student_profile["skills_list"] = skills_list

    # --- PLACEHOLDER DATA ---
    # In the next stage, this will be replaced by a real AI agent response.
    ai_results = {
        "skills_to_learn": [
            "Placeholder: AI will suggest skills based on your profile",
            "Example: Python, Data Analysis, Machine Learning",
            "Example: Communication, Problem Solving",
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
            "Placeholder Project 1 – AI will suggest projects for your career",
            "Placeholder Project 2 – Hands-on practice idea",
            "Placeholder Project 3 – Portfolio-worthy project",
        ],
        "weekly_plan": [
            {
                "day": "Monday",
                "task": "AI will generate your personalized schedule",
            },
            {"day": "Wednesday", "task": "Hands-on practice & exercises"},
            {"day": "Friday", "task": "Review & mini project work"},
            {"day": "Weekend", "task": "Build projects & revise concepts"},
        ],
    }

    return render_template(
        "dashboard.html",
        profile=student_profile,
        results=ai_results,
    )


# Run the app locally
if __name__ == "__main__":
    print("=" * 50)
    print("  SkillPath AI is running!")
    print("  Open your browser and go to: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True)
