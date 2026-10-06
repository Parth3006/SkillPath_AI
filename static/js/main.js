/**
 * SkillPath AI – Main JavaScript
 *
 * Handles:
 *  1. Live skill tag preview as the user types in the "Current Skills" field.
 *  2. Study hours hint that updates based on the number entered.
 *  3. Loading state on form submit to give user feedback.
 *
 * No external libraries used — plain vanilla JavaScript only.
 */

// ============================================================
// 1. Live Skill Tag Preview
//    Reads the "current_skills" textarea and renders colorful
//    tags below it as the user types.
// ============================================================
const skillInput = document.getElementById("current_skills");
const skillTagsContainer = document.getElementById("skillTags");

/**
 * Parse comma-separated skills and render them as tag elements.
 */
function renderSkillTags() {
  // Guard: only run if both elements exist (they only exist on index.html)
  if (!skillInput || !skillTagsContainer) return;

  const rawText = skillInput.value;

  // Split by comma, trim whitespace, filter empty strings
  const skills = rawText
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);

  // Clear current tags
  skillTagsContainer.innerHTML = "";

  // Create a tag element for each skill
  skills.forEach((skill) => {
    const tag = document.createElement("span");
    tag.classList.add("skill-tag", "skill-tag-preview");
    tag.textContent = skill;
    skillTagsContainer.appendChild(tag);
  });
}

// Listen for input events on the skills textarea
if (skillInput) {
  skillInput.addEventListener("input", renderSkillTags);
}


// ============================================================
// 2. Study Hours Hint
//    Shows a friendly message based on the hours entered.
// ============================================================
const hoursInput = document.getElementById("study_hours");
const hoursHint = document.getElementById("hoursHint");

/**
 * Returns a short hint message based on weekly study hours.
 * @param {number} hours
 * @returns {string}
 */
function getHoursHint(hours) {
  if (hours < 3)  return "⚡ Light schedule — we'll keep it focused!";
  if (hours < 7)  return "👍 Good start — solid progress expected.";
  if (hours < 15) return "🔥 Great commitment — you'll see real results!";
  if (hours < 25) return "💪 Impressive — fast-track learning ahead!";
  return "🚀 Full-time learner mode — amazing!";
}

if (hoursInput && hoursHint) {
  hoursInput.addEventListener("input", () => {
    const val = parseInt(hoursInput.value, 10);
    if (!isNaN(val) && val > 0) {
      hoursHint.textContent = getHoursHint(val);
    } else {
      hoursHint.textContent = "";
    }
  });
}


// ============================================================
// 3. Form Submit Loading State
//    Shows a loading indicator when the form is submitted
//    so the user knows something is happening.
// ============================================================
const profileForm = document.getElementById("profileForm");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.querySelector(".btn-text");
const btnLoader = document.getElementById("loader");

if (profileForm) {
  profileForm.addEventListener("submit", () => {
    // Show loader, hide button text
    if (btnText)   btnText.classList.add("hidden");
    if (btnLoader) btnLoader.classList.remove("hidden");
    if (submitBtn) submitBtn.disabled = true;
  });
}


// ============================================================
// 4. Dashboard: Animate cards on scroll (optional polish)
//    Uses IntersectionObserver for a smooth fade-in effect.
// ============================================================
const dashCards = document.querySelectorAll(".dash-card");

if (dashCards.length > 0 && "IntersectionObserver" in window) {
  // Set initial hidden state
  dashCards.forEach((card) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          observer.unobserve(entry.target); // Only animate once
        }
      });
    },
    { threshold: 0.1 } // Trigger when 10% of the card is visible
  );

  dashCards.forEach((card) => observer.observe(card));
}
