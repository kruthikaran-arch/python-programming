"""
AI Based Resume Screening and Review System
Standalone Tkinter application for Python IDLE.

No external packages are required. This capstone version uses transparent
keyword matching and scoring so it works offline.
"""

import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


ROLE_KEYWORDS = {
    "Software Engineer": [
        "python", "java", "javascript", "sql", "api", "git", "database",
        "testing", "cloud", "docker", "machine learning",
    ],
    "Data Scientist": [
        "python", "statistics", "pandas", "numpy", "sql", "machine learning",
        "data analysis", "visualization", "tensorflow", "scikit-learn",
    ],
    "Product Manager": [
        "product strategy", "roadmap", "agile", "scrum", "user research",
        "stakeholder", "analytics", "requirements", "launch", "jira",
    ],
    "Product Designer": [
        "figma", "user research", "wireframe", "prototype", " ux ",
        "ui design", "design system", "usability", "adobe", "user experience",
    ],
    "Marketing Manager": [
        "marketing", "seo", "content", "social media", "campaign",
        "analytics", "branding", "email marketing", "google ads", "crm",
    ],
    "HR Specialist": [
        "recruitment", "talent acquisition", "onboarding", "payroll",
        "employee relations", "hris", "compliance", "interview", "training",
    ],
    "Custom Role": [],
}


class ResumeScreeningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Screening and Review System")
        self.root.geometry("1100x720")
        self.root.minsize(850, 600)
        self.resume_name = tk.StringVar(value="No resume selected")
        self.role = tk.StringVar(value="Software Engineer")
        self.experience = tk.StringVar(value="Any experience")
        self.status = tk.StringVar(value="Ready to screen a resume")
        self._build_interface()

    def _build_interface(self):
        self.root.configure(bg="#f4f6fb")
        header = tk.Frame(self.root, bg="#3949ab", height=80)
        header.pack(fill="x")
        tk.Label(
            header, text="✦  Screenly AI", bg="#3949ab", fg="white",
            font=("Arial", 22, "bold"), padx=25, pady=20,
        ).pack(side="left")
        tk.Label(
            header, text="AI Based Resume Screening & Review System",
            bg="#3949ab", fg="#dfe3ff", font=("Arial", 11),
        ).pack(side="right", padx=25)

        body = tk.Frame(self.root, bg="#f4f6fb", padx=24, pady=20)
        body.pack(fill="both", expand=True)
        left = tk.Frame(body, bg="white", padx=22, pady=18,
                        highlightbackground="#dfe3ed", highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = tk.Frame(body, bg="white", padx=22, pady=18,
                         highlightbackground="#dfe3ed", highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, padx=(12, 0))

        tk.Label(left, text="1. Add resume", bg="white", fg="#17213b",
                 font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Label(left, text="Paste resume text or load a TXT file.",
                 bg="white", fg="#6d7890", font=("Arial", 10)).pack(anchor="w", pady=(4, 14))
        tk.Button(left, text="Open TXT resume", command=self.open_resume,
                  bg="#e8eaff", fg="#3949ab", relief="flat",
                  font=("Arial", 10, "bold"), padx=10, pady=8).pack(anchor="w")
        tk.Label(left, textvariable=self.resume_name, bg="white", fg="#15936f",
                 font=("Arial", 9)).pack(anchor="w", pady=(7, 7))
        self.resume_text = tk.Text(left, height=18, wrap="word", relief="solid",
                                   borderwidth=1, font=("Arial", 10), padx=8, pady=8)
        self.resume_text.pack(fill="both", expand=True)
        self.resume_text.insert("1.0", "Paste the candidate resume here...\n\n")

        tk.Label(right, text="2. Screening setup", bg="white", fg="#17213b",
                 font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Label(right, text="Choose the role and review focus.",
                 bg="white", fg="#6d7890", font=("Arial", 10)).pack(anchor="w", pady=(4, 14))
        self._field(right, "Job role", self.role, list(ROLE_KEYWORDS))
        self._field(right, "Experience level", self.experience,
                    ["Any experience", "Entry level", "Mid level",
                     "Senior level", "Lead / Manager"])
        tk.Label(right, text="Additional job requirements", bg="white",
                 fg="#5d6980", font=("Arial", 10, "bold")).pack(anchor="w", pady=(14, 5))
        self.requirements = tk.Text(right, height=4, wrap="word", relief="solid",
                                    borderwidth=1, font=("Arial", 10), padx=7, pady=6)
        self.requirements.pack(fill="x")

        tk.Label(right, text="Review criteria", bg="white", fg="#5d6980",
                 font=("Arial", 10, "bold")).pack(anchor="w", pady=(14, 5))
        criteria_frame = tk.Frame(right, bg="white")
        criteria_frame.pack(anchor="w")
        self.criteria = {}
        for criterion in ("Skills", "Experience", "Education", "Achievements"):
            value = tk.BooleanVar(value=True)
            self.criteria[criterion] = value
            tk.Checkbutton(criteria_frame, text=criterion, variable=value,
                           bg="white", activebackground="white").pack(side="left", padx=(0, 10))
        tk.Button(right, text="SCREEN RESUME", command=self.screen_resume,
                  bg="#4f5ee8", fg="white", relief="flat",
                  font=("Arial", 11, "bold"), padx=15, pady=11).pack(fill="x", pady=(20, 0))
        tk.Label(right, textvariable=self.status, bg="white", fg="#778299",
                 font=("Arial", 9)).pack(anchor="w", pady=(8, 0))

        results = tk.Frame(self.root, bg="#17213b", padx=24, pady=14)
        results.pack(fill="both", expand=False, padx=24, pady=(0, 20))
        tk.Label(results, text="3. AI review summary", bg="#17213b", fg="white",
                 font=("Arial", 16, "bold")).pack(anchor="w")
        self.result = tk.Text(results, height=8, wrap="word", bg="#202d4d",
                              fg="#eef1ff", relief="flat", font=("Arial", 10),
                              padx=10, pady=8)
        self.result.pack(fill="both", expand=True, pady=(8, 0))
        self.result.insert("1.0", "Your screening results will appear here.")

    @staticmethod
    def _field(parent, label, variable, values):
        tk.Label(parent, text=label, bg="white", fg="#5d6980",
                 font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 5))
        ttk.Combobox(parent, textvariable=variable, values=values,
                     state="readonly", font=("Arial", 10)).pack(fill="x")

    def open_resume(self):
        filename = filedialog.askopenfilename(
            title="Select resume text file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filename:
            return
        try:
            text = Path(filename).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            messagebox.showerror("Cannot open file", "Please choose a UTF-8 text file.")
            return
        self.resume_text.delete("1.0", "end")
        self.resume_text.insert("1.0", text)
        self.resume_name.set(Path(filename).name)
        self.status.set("Resume loaded and ready for screening")

    def screen_resume(self):
        resume = self.resume_text.get("1.0", "end").strip()
        if not resume or resume == "Paste the candidate resume here...":
            messagebox.showwarning("Resume required", "Paste resume text or open a TXT resume first.")
            return

        role = self.role.get()
        keywords = ROLE_KEYWORDS[role]
        custom = self.requirements.get("1.0", "end").strip().lower()
        custom_words = [word for word in re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", custom)]
        all_keywords = list(dict.fromkeys(keywords + custom_words))
        normalized = " " + re.sub(r"\s+", " ", resume.lower()) + " "
        matched = [word.strip() for word in all_keywords if f" {word.strip()} " in normalized or word.strip() in normalized]
        score = min(98, round(35 + (len(matched) / max(len(all_keywords), 1)) * 63))
        missing = [word for word in all_keywords if word.strip() not in matched][:5]
        years = re.findall(r"(\d+)\+?\s*(?:years|yrs)", resume.lower())
        strengths = [
            f"{len(matched)} relevant skills or requirements detected",
            "Resume text was successfully analyzed",
            "Role selected: " + role,
        ]
        if years:
            strengths.append(f"Approximately {years[0]} years of experience mentioned")

        if score >= 80:
            verdict = "STRONG MATCH"
        elif score >= 60:
            verdict = "POTENTIAL MATCH"
        else:
            verdict = "NEEDS REVIEW"

        lines = [
            f"Candidate: {self.resume_name.get()}",
            f"Role: {role}  |  Experience: {self.experience.get()}",
            f"Overall fit score: {score}%  |  {verdict}",
            "",
            "Key strengths:",
            *[f"  • {item}" for item in strengths],
            "",
            "Missing or unconfirmed keywords:",
            *[f"  • {item}" for item in (missing or ["No major gaps detected"])],
            "",
            "Recommendation: Use this score as decision support and complete a human review.",
        ]
        self.result.delete("1.0", "end")
        self.result.insert("1.0", "\n".join(lines))
        self.status.set("Screening complete")


if __name__ == "__main__":
    window = tk.Tk()
    ResumeScreeningApp(window)
    window.mainloop()
