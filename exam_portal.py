import tkinter as tk
from tkinter import messagebox
import time

# DigiCampus-inspired desktop examination demo
# Uses only Python's standard library and Tkinter.

BG = "#1C1C1E"
PANEL = "#252527"
CARD = "#29292C"
RED = "#FF1744"
RED_DARK = "#B51232"
WHITE = "#FFFFFF"
MUTED = "#A7A7AD"
GREEN = "#00B386"
FONT = "Arial"


QUESTIONS = [
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "define", "def", "fun"],
        "answer": 2,
    },
    {
        "question": "Which of the following is a mutable data type in Python?",
        "options": ["Tuple", "List", "String", "Integer"],
        "answer": 1,
    },
    {
        "question": "What is the output of print(3 * 2)?",
        "options": ["5", "6", "32", "Error"],
        "answer": 1,
    },
    {
        "question": "Which Tkinter widget is commonly used to display a clickable button?",
        "options": ["Label", "Entry", "Button", "Frame"],
        "answer": 2,
    },
    {
        "question": "Which symbol is used for a single-line comment in Python?",
        "options": ["//", "#", "/*", "--"],
        "answer": 1,
    },
]


class ExamPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Portal | Student")
        self.root.geometry("1366x768")
        self.root.minsize(1050, 680)
        self.root.configure(bg=BG)

        self.answers = {}
        self.bookmarked = set()
        self.current = 0
        self.duration = 10 * 60
        self.remaining = self.duration
        self.timer_job = None
        self.exam_started = False

        self.show_dashboard()

    def clear_screen(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, bg=RED, fg=WHITE,
                    active_bg=RED_DARK, width=None, font_size=11):
        return tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=active_bg,
            activeforeground=WHITE, relief="flat", bd=0,
            cursor="hand2", font=(FONT, font_size, "bold"),
            padx=18, pady=11, width=width
        )

    def show_dashboard(self):
        self.clear_screen()
        header = tk.Frame(self.root, bg=RED, height=76)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="EXAM PORTAL", bg=RED, fg=WHITE,
                 font=(FONT, 21, "bold")).pack(side="left", padx=34)
        tk.Label(header, text="STUDENT DASHBOARD", bg=RED, fg=WHITE,
                 font=(FONT, 10, "bold")).pack(side="right", padx=36)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=48, pady=34)

        tk.Label(body, text="Welcome, Student!", bg=BG, fg=WHITE,
                 font=(FONT, 27, "bold")).pack(anchor="w")
        tk.Label(body, text="Your examination workspace",
                 bg=BG, fg=MUTED, font=(FONT, 12)).pack(anchor="w", pady=(6, 26))

        stats = tk.Frame(body, bg=BG)
        stats.pack(fill="x", pady=(0, 25))
        self.stat_card(stats, "AVAILABLE EXAMS", "01", "Ready to attempt").pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.stat_card(stats, "COMPLETED EXAMS", "00", "Your completed tests").pack(side="left", fill="x", expand=True, padx=12)
        self.stat_card(stats, "TOTAL QUESTIONS", str(len(QUESTIONS)), "In this demo test").pack(side="left", fill="x", expand=True, padx=(12, 0))

        exam = tk.Frame(body, bg=PANEL, highlightthickness=1, highlightbackground="#3A3A3D")
        exam.pack(fill="x", pady=5)
        top = tk.Frame(exam, bg=PANEL)
        top.pack(fill="x", padx=25, pady=(22, 8))
        tk.Label(top, text="AVAILABLE EXAMINATION", bg=PANEL, fg=RED,
                 font=(FONT, 10, "bold")).pack(anchor="w")
        tk.Label(exam, text="Python Programming – Practice Test",
                 bg=PANEL, fg=WHITE, font=(FONT, 19, "bold")).pack(anchor="w", padx=25, pady=(4, 8))
        tk.Label(exam, text="5 multiple-choice questions  •  10 minutes  •  2 marks per question",
                 bg=PANEL, fg=MUTED, font=(FONT, 11)).pack(anchor="w", padx=25, pady=(0, 22))

        bottom = tk.Frame(exam, bg=PANEL)
        bottom.pack(fill="x", padx=25, pady=(0, 24))
        self.make_button(bottom, "START EXAM  →", self.start_exam).pack(side="left")
        tk.Label(bottom, text="Please read the instructions before starting.",
                 bg=PANEL, fg=MUTED, font=(FONT, 10)).pack(side="left", padx=18)

        tk.Label(body, text="EXAM INSTRUCTIONS", bg=BG, fg=WHITE,
                 font=(FONT, 12, "bold")).pack(anchor="w", pady=(28, 12))
        instructions = [
            "Each question has one correct answer.",
            "Use Previous and Next to move between questions.",
            "You can bookmark questions and return to them later.",
            "Your answers are kept while you move between questions.",
            "Submit the exam when you are finished. The timer submits automatically.",
        ]
        for i, item in enumerate(instructions, 1):
            row = tk.Frame(body, bg=BG)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text=f"{i:02}", bg=RED_DARK, fg=WHITE,
                     font=(FONT, 9, "bold"), padx=8, pady=4).pack(side="left")
            tk.Label(row, text=item, bg=BG, fg=MUTED,
                     font=(FONT, 10)).pack(side="left", padx=10)

    def stat_card(self, parent, heading, value, note):
        card = tk.Frame(parent, bg=PANEL, padx=20, pady=17,
                        highlightthickness=1, highlightbackground="#38383B")
        tk.Label(card, text=heading, bg=PANEL, fg=MUTED,
                 font=(FONT, 9, "bold")).pack(anchor="w")
        tk.Label(card, text=value, bg=PANEL, fg=RED,
                 font=(FONT, 25, "bold")).pack(anchor="w", pady=4)
        tk.Label(card, text=note, bg=PANEL, fg=MUTED,
                 font=(FONT, 9)).pack(anchor="w")
        return card

    def start_exam(self):
        if not messagebox.askyesno("Start examination",
                                   "Are you ready to begin the Python Programming test?"):
            return
        self.answers = {}
        self.bookmarked = set()
        self.current = 0
        self.remaining = self.duration
        self.exam_started = True
        self.show_exam()
        self.tick()

    def show_exam(self):
        self.clear_screen()
        self.exam_started = True

        header = tk.Frame(self.root, bg=RED, height=82)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="‹", bg=RED, fg=WHITE,
                 font=(FONT, 30), cursor="hand2").pack(side="left", padx=(25, 8))
        tk.Label(header, text="EXAMINATION", bg=RED, fg=WHITE,
                 font=(FONT, 15, "bold")).pack(side="left")
        self.timer_label = tk.Label(header, text="◷  10:00", bg=RED_DARK,
                                    fg=WHITE, font=(FONT, 15, "bold"),
                                    padx=18, pady=9)
        self.timer_label.pack(side="left", padx=55)
        tk.Label(header, text="ⓘ  Instructions", bg=RED, fg=WHITE,
                 font=(FONT, 10, "bold")).pack(side="right", padx=30)

        status = tk.Frame(self.root, bg=BG)
        status.pack(fill="x", padx=42, pady=(17, 10))
        tk.Label(status, text="●  Saved", bg=BG, fg="#FF667F",
                 font=(FONT, 10, "bold")).pack(side="left")
        self.progress_label = tk.Label(status, text="", bg=BG, fg=MUTED,
                                        font=(FONT, 10, "bold"))
        self.progress_label.pack(side="right")

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=42, pady=10)

        self.question_panel = tk.Frame(main, bg=BG)
        self.question_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))

        self.side_panel = tk.Frame(main, bg=PANEL, width=245,
                                   highlightthickness=1, highlightbackground="#38383B")
        self.side_panel.pack(side="right", fill="y")
        self.side_panel.pack_propagate(False)

        self.q_number = tk.Label(self.question_panel, text="", bg=RED_DARK,
                                 fg=WHITE, font=(FONT, 11, "bold"),
                                 padx=14, pady=8)
        self.q_number.pack(anchor="w", pady=(5, 14))

        badges = tk.Frame(self.question_panel, bg=BG)
        badges.pack(anchor="w", pady=(0, 24))
        tk.Label(badges, text="Single correct", bg="#343438", fg="#D1D1D5",
                 font=(FONT, 9, "bold"), padx=10, pady=6).pack(side="left")
        tk.Label(badges, text="Max Marks: 2", bg="#063D32", fg=GREEN,
                 font=(FONT, 9, "bold"), padx=10, pady=6).pack(side="left", padx=9)

        self.question_text = tk.Label(self.question_panel, text="", bg=BG,
                                      fg=WHITE, font=(FONT, 17),
                                      justify="left", anchor="w",
                                      wraplength=850)
        self.question_text.pack(fill="x", anchor="w", pady=(0, 25))

        tk.Label(self.question_panel, text="◯  Select one answer",
                 bg=BG, fg=MUTED, font=(FONT, 10, "bold")).pack(anchor="w", pady=(0, 12))

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.question_panel, text="", anchor="w",
                            command=lambda index=i: self.select_answer(index),
                            bg=CARD, fg="#E7E7E9", activebackground="#3A252A",
                            activeforeground=WHITE, relief="flat",
                            highlightthickness=1, highlightbackground="#583038",
                            highlightcolor=RED, font=(FONT, 12),
                            padx=18, pady=17, cursor="hand2")
            btn.pack(fill="x", pady=6)
            self.option_buttons.append(btn)

        # Right-side question palette
        tk.Label(self.side_panel, text="QUESTION PALETTE", bg=PANEL,
                 fg=WHITE, font=(FONT, 11, "bold")).pack(anchor="w", padx=17, pady=(20, 6))
        tk.Label(self.side_panel, text="Select a question to visit it",
                 bg=PANEL, fg=MUTED, font=(FONT, 9)).pack(anchor="w", padx=17, pady=(0, 14))
        self.palette = tk.Frame(self.side_panel, bg=PANEL)
        self.palette.pack(fill="x", padx=13)
        self.palette_buttons = []
        for i in range(len(QUESTIONS)):
            b = tk.Button(self.palette, text=str(i + 1),
                          command=lambda index=i: self.go_to_question(index),
                          width=4, bg=CARD, fg=WHITE, relief="flat",
                          font=(FONT, 10, "bold"), pady=8, cursor="hand2")
            b.grid(row=i // 4, column=i % 4, padx=4, pady=5)
            self.palette_buttons.append(b)

        tk.Frame(self.side_panel, bg="#3A3A3D", height=1).pack(fill="x", padx=15, pady=17)
        self.bookmark_button = self.make_button(
            self.side_panel, "☆  Bookmark question", self.toggle_bookmark,
            bg="#39393D", active_bg="#4A4A50", font_size=9
        )
        self.bookmark_button.pack(fill="x", padx=14)
        self.clear_button = self.make_button(
            self.side_panel, "Clear response", self.clear_answer,
            bg="#39393D", active_bg="#4A4A50", font_size=9
        )
        self.clear_button.pack(fill="x", padx=14, pady=9)

        footer = tk.Frame(self.root, bg="#242426", height=78)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        self.previous_button = self.make_button(
            footer, "‹  Previous", self.previous_question,
            bg="#171719", active_bg="#333337"
        )
        self.previous_button.pack(side="left", padx=35, pady=15)
        self.footer_progress = tk.Label(footer, text="", bg="#242426",
                                        fg=MUTED, font=(FONT, 10, "bold"))
        self.footer_progress.pack(side="left", expand=True)
        self.make_button(footer, "Submit exam  →", self.submit_exam,
                         bg=RED, active_bg=RED_DARK).pack(side="right", padx=35, pady=15)
        self.next_button = self.make_button(
            footer, "Next  ›", self.next_question,
            bg="#171719", active_bg="#333337"
        )
        self.next_button.pack(side="right", padx=8, pady=15)

        self.render_question()

    def render_question(self):
        q = QUESTIONS[self.current]
        self.q_number.config(text=f"Q{self.current + 1}")
        self.question_text.config(text=q["question"])
        self.progress_label.config(text=f"QUESTION {self.current + 1} OF {len(QUESTIONS)}")
        self.footer_progress.config(text=f"Q {self.current + 1} of {len(QUESTIONS)}")

        selected = self.answers.get(self.current)
        for i, option in enumerate(q["options"]):
            letter = "ABCD"[i]
            if selected == i:
                bg, outline, marker_bg = "#3B2026", RED, RED
                fg = WHITE
            else:
                bg, outline, marker_bg = CARD, "#583038", CARD
                fg = "#E7E7E9"
            self.option_buttons[i].config(
                text=f"   {letter}       {option}",
                bg=bg, fg=fg, activebackground="#3B2026",
                highlightbackground=outline
            )
        for i, b in enumerate(self.palette_buttons):
            if i == self.current:
                b.config(bg=RED, fg=WHITE)
            elif i in self.answers:
                b.config(bg="#07523F", fg=WHITE)
            elif i in self.bookmarked:
                b.config(bg="#694A18", fg=WHITE)
            else:
                b.config(bg=CARD, fg=WHITE)

        self.bookmark_button.config(
            text="★  Bookmarked" if self.current in self.bookmarked else "☆  Bookmark question"
        )
        self.previous_button.config(state="normal" if self.current > 0 else "disabled")
        self.next_button.config(state="normal" if self.current < len(QUESTIONS) - 1 else "disabled")

    def select_answer(self, index):
        self.answers[self.current] = index
        self.render_question()

    def clear_answer(self):
        self.answers.pop(self.current, None)
        self.render_question()

    def toggle_bookmark(self):
        if self.current in self.bookmarked:
            self.bookmarked.remove(self.current)
        else:
            self.bookmarked.add(self.current)
        self.render_question()

    def go_to_question(self, index):
        self.current = index
        self.render_question()

    def previous_question(self):
        if self.current > 0:
            self.current -= 1
            self.render_question()

    def next_question(self):
        if self.current < len(QUESTIONS) - 1:
            self.current += 1
            self.render_question()

    def tick(self):
        mins, secs = divmod(max(0, self.remaining), 60)
        self.timer_label.config(text=f"◷  {mins:02d}:{secs:02d}")
        if self.remaining <= 0:
            messagebox.showinfo("Time is up", "The examination time has ended. Your answers will be submitted.")
            self.finish_exam()
            return
        self.remaining -= 1
        self.timer_job = self.root.after(1000, self.tick)

    def submit_exam(self):
        unanswered = len(QUESTIONS) - len(self.answers)
        prompt = "Submit your examination now?"
        if unanswered:
            prompt += f"\n\nYou have {unanswered} unanswered question(s)."
        if messagebox.askyesno("Confirm submission", prompt):
            self.finish_exam()

    def finish_exam(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.exam_started = False
        score = sum(1 for i, q in enumerate(QUESTIONS)
                    if self.answers.get(i) == q["answer"]) * 2
        total = len(QUESTIONS) * 2
        percentage = (score / total) * 100
        self.show_result(score, total, percentage)

    def show_result(self, score, total, percentage):
        self.clear_screen()
        header = tk.Frame(self.root, bg=RED, height=76)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="EXAM PORTAL", bg=RED, fg=WHITE,
                 font=(FONT, 21, "bold")).pack(side="left", padx=34)
        tk.Label(header, text="EXAMINATION RESULT", bg=RED, fg=WHITE,
                 font=(FONT, 10, "bold")).pack(side="right", padx=36)

        body = tk.Frame(self.root, bg=BG)
        body.pack(expand=True, fill="both", padx=60, pady=35)
        tk.Label(body, text="Examination submitted!", bg=BG, fg=WHITE,
                 font=(FONT, 27, "bold")).pack(pady=(12, 8))
        tk.Label(body, text="Here is your performance summary.",
                 bg=BG, fg=MUTED, font=(FONT, 12)).pack(pady=(0, 25))

        card = tk.Frame(body, bg=PANEL, padx=45, pady=28,
                        highlightthickness=1, highlightbackground="#3A3A3D")
        card.pack()
        tk.Label(card, text="YOUR SCORE", bg=PANEL, fg=MUTED,
                 font=(FONT, 10, "bold")).pack()
        tk.Label(card, text=f"{score} / {total}", bg=PANEL, fg=RED,
                 font=(FONT, 39, "bold")).pack(pady=7)
        tk.Label(card, text=f"{percentage:.1f}%  •  {'PASS' if percentage >= 40 else 'NEEDS IMPROVEMENT'}",
                 bg=PANEL, fg=GREEN if percentage >= 40 else RED,
                 font=(FONT, 12, "bold")).pack(pady=(0, 16))

        correct = sum(1 for i, q in enumerate(QUESTIONS)
                      if self.answers.get(i) == q["answer"])
        wrong = sum(1 for i in self.answers
                    if self.answers[i] != QUESTIONS[i]["answer"])
        unanswered = len(QUESTIONS) - len(self.answers)
        summary = tk.Frame(card, bg=PANEL)
        summary.pack()
        for label, value in [("Correct", correct), ("Incorrect", wrong), ("Unanswered", unanswered)]:
            item = tk.Frame(summary, bg=CARD, padx=20, pady=13)
            item.pack(side="left", padx=6)
            tk.Label(item, text=str(value), bg=CARD, fg=WHITE,
                     font=(FONT, 20, "bold")).pack()
            tk.Label(item, text=label, bg=CARD, fg=MUTED,
                     font=(FONT, 9)).pack()

        self.make_button(body, "Back to dashboard", self.show_dashboard).pack(pady=25)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExamPortal(root)
    root.mainloop()
