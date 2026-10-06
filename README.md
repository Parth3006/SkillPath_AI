# SkillPath AI – Personalized Career & Skill Mentor

> A beginner-friendly web app that helps college students identify skill gaps and create a personalized learning roadmap for their target career.

---

## 📌 What is SkillPath AI?

SkillPath AI is a student-focused tool where you enter your:
- Current skills
- Target career/job role
- Degree & experience level
- Weekly study availability

…and get back a **personalized learning roadmap**, list of **skills to learn**, **recommended projects**, and a **weekly study plan**.

> **Note:** In this first version (v1), the AI integration is not yet added. The dashboard shows placeholder data. AI-powered results will be added in the next stage.

---

## 🗂️ Project Structure

```
SkillPath_AI/
├── app.py                  ← Flask backend (main server file)
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
│
├── templates/
│   ├── index.html          ← Home page (student profile form)
│   └── dashboard.html      ← Results dashboard
│
└── static/
    ├── css/
    │   └── style.css       ← All styles for the app
    └── js/
        └── main.js         ← Frontend interactivity (vanilla JS)
```

---

## 🚀 How to Run (Windows)

Follow these steps to run the project on your local machine.

### Step 1: Make sure Python is installed

Open a terminal (Command Prompt or PowerShell) and type:
```bash
python --version
```
You should see something like `Python 3.10.x`. If not, download Python from [python.org](https://python.org).

---

### Step 2: Navigate to the project folder

```bash
cd "C:\Users\YOUR_NAME\OneDrive\Desktop\SkillPath_AI"
```
*(Replace `YOUR_NAME` with your actual Windows username)*

---

### Step 3: Create a virtual environment (recommended)

A virtual environment keeps your project's dependencies separate from the rest of your system.

```bash
python -m venv venv
```

Then activate it:
```bash
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal prompt.

---

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask (the only library needed for now).

---

### Step 5: Run the app

```bash
python app.py
```

You should see:
```
==================================================
  SkillPath AI is running!
  Open your browser and go to: http://127.0.0.1:5000
==================================================
```

---

### Step 6: Open in your browser

Go to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Fill in your profile and click **"Generate My Roadmap"** to see the dashboard!

---

## 🛠️ How It Works (For Beginners)

| File | What it does |
|------|-------------|
| `app.py` | The Python brain. Runs the web server, handles form submissions, passes data to HTML pages. |
| `templates/index.html` | The home page. Contains the student profile form. |
| `templates/dashboard.html` | The results page. Shows skills, roadmap, projects, and weekly plan. |
| `static/css/style.css` | Makes the app look nice (colors, layout, cards). |
| `static/js/main.js` | Adds interactivity: live skill tags, loading button, card animations. |

### Request Flow

```
User fills form → Submits to /dashboard (POST) → Flask reads the data
→ Flask prepares placeholder results → Sends data to dashboard.html
→ HTML displays the results to the user
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask   | 3.0.3   | Web framework (routing, templates, forms) |

That's it! No database, no authentication, no complex setup.

---

## 🔮 What's Coming Next (Stage 2)

In the next stage, we will add:
- 🤖 **AI/LLM Integration** – Connect to an AI model (like Google Gemini or OpenAI) to generate real, personalized results
- 📊 Real skill gap analysis based on your profile
- 🗺️ AI-generated step-by-step learning roadmap
- 🛠️ Personalized project recommendations
- 📅 Dynamic weekly study plan

---

## 💡 Tips for Students

- **Use `debug=True`** (already set) while developing — Flask will auto-reload when you save files.
- **CSS variables** in `style.css` (at the top under `:root`) let you change the color theme easily.
- **Comments are everywhere** in the code to help you understand each part.
- To stop the server, press `Ctrl + C` in the terminal.

---

## 👨‍💻 Built With

- **Python** + **Flask** – Backend
- **HTML5** + **CSS3** + **Vanilla JavaScript** – Frontend
- No external JS libraries (no jQuery, no Bootstrap — keeping it simple!)

---

*SkillPath AI – Built for students, by students 💙*
