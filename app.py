"""
SkillPath AI – Personalized Career & Skill Mentor
Backend: Flask web server

This is the main entry point for the application.
It handles two routes:
  - "/" (Home): Shows the student profile form.
  - "/dashboard": Receives form data, calls the AI service, and shows results.

AI integration: xAI / Grok via ai_service.py
"""

from flask import Flask, render_template, request
from ai_service import get_ai_results

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
    Dashboard page — receives form data, calls the AI service,
    and renders the personalized results.
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

    # --- AI RESULTS ---
    # Calls xAI/Grok API. Falls back to demo data if unavailable.
    ai_results = get_ai_results(student_profile)

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
