
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


DATABASE = "school.json"


def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE, "r") as f:
            content = f.read()
            if content:
                return json.loads(content)
    return {"student": [], "teacher": []}


def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)


def validate_email(email):
    return "@" in email and "." in email


# ----------------------------------------------------------------------
# Visual theme
# ----------------------------------------------------------------------

COLORS = {
    "bg": "#F3F5FA",
    "sidebar": "#1F2440",
    "sidebar_hover": "#2E3560",
    "sidebar_active": "#5B6CFF",
    "card": "#FFFFFF",
    "accent": "#5B6CFF",
    "accent_dark": "#4453DB",
    "text": "#1F2440",
    "muted": "#7B7F9E",
    "success": "#22A06B",
    "danger": "#E5484D",
    "danger_dark": "#C93F43",
    "border": "#E4E7F2",
}

FONT_TITLE = ("Segoe UI Semibold", 20)
FONT_SUB = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_BTN = ("Segoe UI Semibold", 11)
FONT_NAV = ("Segoe UI", 11)
FONT_STAT = ("Segoe UI Semibold", 26)


class Card(tk.Frame):
    """A simple white rounded-looking card container."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=COLORS["card"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            **kwargs,
        )


class RoundedButton(tk.Button):
    """A flat, accent-colored button with hover feedback."""

    def __init__(self, parent, text, command, bg=COLORS["accent"],
                 fg="white", hover=COLORS["accent_dark"], **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            font=FONT_BTN,
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=8,
            **kwargs,
        )
        self._bg = bg
        self._hover = hover
        self.bind("<Enter>", lambda e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg))


class DangerButton(RoundedButton):
    """A flat, red 'destructive action' button with hover feedback."""

    def __init__(self, parent, text, command, **kwargs):
        super().__init__(
            parent, text, command,
            bg=COLORS["danger"], fg="white", hover=COLORS["danger_dark"],
            **kwargs,
        )


def labeled_entry(parent, label_text, show=None):
    """Creates a label + entry pair stacked vertically, returns the Entry."""
    wrap = tk.Frame(parent, bg=COLORS["card"])
    wrap.pack(fill="x", pady=(0, 12))
    tk.Label(wrap, text=label_text, font=FONT_LABEL, bg=COLORS["card"],
              fg=COLORS["muted"], anchor="w").pack(fill="x")
    entry = tk.Entry(wrap, font=FONT_SUB, relief="flat", bg="#F7F8FC",
                      fg=COLORS["text"], insertbackground=COLORS["text"],
                      highlightthickness=1, highlightbackground=COLORS["border"],
                      highlightcolor=COLORS["accent"], show=show)
    entry.pack(fill="x", ipady=8, ipadx=6)
    return entry


# ----------------------------------------------------------------------
# Main Application
# ----------------------------------------------------------------------

class SchoolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management System")
        self.geometry("1100x680")
        self.minsize(980, 600)
        self.configure(bg=COLORS["bg"])

        self.data = load_data()

        self._build_layout()
        self.show_page("dashboard")

    # ------------------------------------------------------------------
    # Layout scaffolding: sidebar + content area
    # ------------------------------------------------------------------
    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        logo.pack(fill="x", pady=(28, 20), padx=20)
        tk.Label(logo, text="🎓", font=("Segoe UI", 26), bg=COLORS["sidebar"],
                  fg="white").pack(side="left")
        tk.Label(logo, text="  Edu Manager", font=("Segoe UI Semibold", 15),
                  bg=COLORS["sidebar"], fg="white").pack(side="left")

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "🏠  Dashboard"),
            ("reg_student", "📝  Register Student"),
            ("reg_teacher", "🧑‍🏫  Register Teacher"),
            ("add_grades", "📊  Add Grades"),
            ("student_details", "🔍  Student Lookup"),
            ("teacher_details", "🔎  Teacher Lookup"),
            ("all_students", "👩‍🎓  All Students"),
            ("all_teachers", "👨‍🏫  All Teachers"),
        ]
        for key, label in nav_items:
            self._add_nav_button(key, label)

        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.pack(side="right", fill="both", expand=True)

        self.pages = {}
        for key in [i[0] for i in nav_items]:
            frame = tk.Frame(self.content, bg=COLORS["bg"])
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages[key] = frame

        self._build_dashboard(self.pages["dashboard"])
        self._build_register_student(self.pages["reg_student"])
        self._build_register_teacher(self.pages["reg_teacher"])
        self._build_add_grades(self.pages["add_grades"])
        self._build_student_details(self.pages["student_details"])
        self._build_teacher_details(self.pages["teacher_details"])
        self._build_all_students(self.pages["all_students"])
        self._build_all_teachers(self.pages["all_teachers"])

    def _add_nav_button(self, key, label):
        btn = tk.Label(
            self.sidebar, text=label, font=FONT_NAV, bg=COLORS["sidebar"],
            fg="#C7CAE8", anchor="w", padx=20, pady=12, cursor="hand2",
        )
        btn.pack(fill="x")
        btn.bind("<Button-1>", lambda e, k=key: self.show_page(k))
        btn.bind("<Enter>", lambda e, b=btn, k=key: self._nav_hover(b, k, True))
        btn.bind("<Leave>", lambda e, b=btn, k=key: self._nav_hover(b, k, False))
        self.nav_buttons[key] = btn

    def _nav_hover(self, btn, key, entering):
        if getattr(self, "_active_page", None) == key:
            return
        btn.config(bg=COLORS["sidebar_hover"] if entering else COLORS["sidebar"])

    def show_page(self, key):
        self._active_page = key
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.config(bg=COLORS["sidebar_active"], fg="white")
            else:
                btn.config(bg=COLORS["sidebar"], fg="#C7CAE8")
        self.pages[key].tkraise()
        if key == "dashboard":
            self._refresh_dashboard()
        elif key == "all_students":
            self._refresh_all_students()
        elif key == "all_teachers":
            self._refresh_all_teachers()

    # ------------------------------------------------------------------
    # Page header helper
    # ------------------------------------------------------------------
    def _page_header(self, parent, title, subtitle):
        wrap = tk.Frame(parent, bg=COLORS["bg"])
        wrap.pack(fill="x", padx=40, pady=(32, 10))
        tk.Label(wrap, text=title, font=FONT_TITLE, bg=COLORS["bg"],
                  fg=COLORS["text"]).pack(anchor="w")
        tk.Label(wrap, text=subtitle, font=FONT_SUB, bg=COLORS["bg"],
                  fg=COLORS["muted"]).pack(anchor="w", pady=(2, 0))

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------
    def _build_dashboard(self, page):
        self._page_header(page, "Dashboard", "A quick overview of your school.")

        self.stat_cards_frame = tk.Frame(page, bg=COLORS["bg"])
        self.stat_cards_frame.pack(fill="x", padx=40, pady=10)

        self.stat_labels = {}
        for i, (key, icon, text) in enumerate([
            ("students", "👩‍🎓", "Total Students"),
            ("teachers", "🧑‍🏫", "Total Teachers"),
            ("avg", "📈", "Average Grade"),
        ]):
            card = Card(self.stat_cards_frame)
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            self.stat_cards_frame.grid_columnconfigure(i, weight=1)
            tk.Label(card, text=icon, font=("Segoe UI", 22), bg=COLORS["card"]
                      ).pack(anchor="w", padx=20, pady=(18, 0))
            val = tk.Label(card, text="0", font=FONT_STAT, bg=COLORS["card"],
                             fg=COLORS["accent"])
            val.pack(anchor="w", padx=20)
            tk.Label(card, text=text, font=FONT_LABEL, bg=COLORS["card"],
                      fg=COLORS["muted"]).pack(anchor="w", padx=20, pady=(0, 18))
            self.stat_labels[key] = val

        tip = Card(page)
        tip.pack(fill="x", padx=40, pady=(20, 10))
        tk.Label(
            tip,
            text="💡  Use the sidebar to register students & teachers, "
                 "record grades, or look up existing records. You can also "
                 "delete a record from its lookup page or from the All "
                 "Students / All Teachers list.",
            font=FONT_SUB, bg=COLORS["card"], fg=COLORS["muted"],
            justify="left", wraplength=900,
        ).pack(anchor="w", padx=20, pady=16)

    def _refresh_dashboard(self):
        students = self.data["student"]
        teachers = self.data["teacher"]
        all_grades = [g for s in students for g in s["grades"].values()]
        avg = round(sum(all_grades) / len(all_grades), 2) if all_grades else "—"
        self.stat_labels["students"].config(text=str(len(students)))
        self.stat_labels["teachers"].config(text=str(len(teachers)))
        self.stat_labels["avg"].config(text=str(avg))

    # ------------------------------------------------------------------
    # Register Student
    # ------------------------------------------------------------------
    def _build_register_student(self, page):
        self._page_header(page, "Register Student", "Add a new student to the system.")
        card = Card(page)
        card.pack(padx=40, pady=10, fill="x")
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=30, pady=25, fill="x")

        name_e = labeled_entry(inner, "Full Name")
        rollno_e = labeled_entry(inner, "Roll No")
        email_e = labeled_entry(inner, "Email")

        def submit():
            name = name_e.get().strip()
            rollno = rollno_e.get().strip()
            email = email_e.get().strip()

            if not name or not rollno or not email:
                messagebox.showwarning("Missing info", "Please fill in every field.")
                return
            if not validate_email(email):
                messagebox.showerror("Invalid email", "Please enter a valid email address.")
                return
            for s in self.data["student"]:
                if s["rollno"] == rollno:
                    messagebox.showerror("Duplicate", "A student with this roll no already exists.")
                    return

            self.data["student"].append({
                "name": name, "rollno": rollno, "email": email, "grades": {}
            })
            save_data(self.data)
            messagebox.showinfo("Success", f"Student '{name}' registered successfully!")
            name_e.delete(0, "end")
            rollno_e.delete(0, "end")
            email_e.delete(0, "end")

        RoundedButton(inner, "Register Student", submit).pack(anchor="w", pady=(6, 0))

    def _build_register_teacher(self, page):
        self._page_header(page, "Register Teacher", "Add a new teacher to the system.")
        card = Card(page)
        card.pack(padx=40, pady=10, fill="x")
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=30, pady=25, fill="x")

        name_e = labeled_entry(inner, "Full Name")
        email_e = labeled_entry(inner, "Email")
        subject_e = labeled_entry(inner, "Subject")
        empid_e = labeled_entry(inner, "Employee ID")

        def submit():
            name = name_e.get().strip()
            email = email_e.get().strip()
            subject = subject_e.get().strip()
            empid = empid_e.get().strip()

            if not name or not email or not subject or not empid:
                messagebox.showwarning("Missing info", "Please fill in every field.")
                return
            if not validate_email(email):
                messagebox.showerror("Invalid email", "Please enter a valid email address.")
                return
            for t in self.data["teacher"]:
                if t["empid"] == empid:
                    messagebox.showerror("Duplicate", "A teacher with this employee id already exists.")
                    return

            self.data["teacher"].append({
                "name": name, "email": email, "subject": subject, "empid": empid
            })
            save_data(self.data)
            messagebox.showinfo("Success", f"Teacher '{name}' registered successfully!")
            name_e.delete(0, "end")
            email_e.delete(0, "end")
            subject_e.delete(0, "end")
            empid_e.delete(0, "end")

        RoundedButton(inner, "Register Teacher", submit).pack(anchor="w", pady=(6, 0))

    # ------------------------------------------------------------------
    # Add Grades
    # ------------------------------------------------------------------
    def _build_add_grades(self, page):
        self._page_header(page, "Add Grades", "Record a grade for a student.")
        card = Card(page)
        card.pack(padx=40, pady=10, fill="x")
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=30, pady=25, fill="x")

        rollno_e = labeled_entry(inner, "Student Roll No")
        subject_e = labeled_entry(inner, "Subject")
        grade_e = labeled_entry(inner, "Grade (numeric)")

        def submit():
            rollno = rollno_e.get().strip()
            subject = subject_e.get().strip()
            grade = grade_e.get().strip()

            if not rollno or not subject or not grade:
                messagebox.showwarning("Missing info", "Please fill in every field.")
                return
            try:
                grade_val = float(grade)
            except ValueError:
                messagebox.showerror("Invalid grade", "Grade must be a number.")
                return

            for s in self.data["student"]:
                if s["rollno"] == rollno:
                    s["grades"][subject] = grade_val
                    save_data(self.data)
                    messagebox.showinfo("Success", f"Grade added for {s['name']}.")
                    rollno_e.delete(0, "end")
                    subject_e.delete(0, "end")
                    grade_e.delete(0, "end")
                    return
            messagebox.showerror("Not found", "No student with this roll no.")

        RoundedButton(inner, "Add Grade", submit).pack(anchor="w", pady=(6, 0))

    # ------------------------------------------------------------------
    # Student Lookup (with delete)
    # ------------------------------------------------------------------
    def _build_student_details(self, page):
        self._page_header(page, "Student Lookup", "Search a student by roll no.")
        card = Card(page)
        card.pack(padx=40, pady=10, fill="x")
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=30, pady=25, fill="x")

        search_row = tk.Frame(inner, bg=COLORS["card"])
        search_row.pack(fill="x")
        rollno_e = tk.Entry(search_row, font=FONT_SUB, relief="flat", bg="#F7F8FC",
                             fg=COLORS["text"], highlightthickness=1,
                             highlightbackground=COLORS["border"],
                             highlightcolor=COLORS["accent"])
        rollno_e.pack(side="left", fill="x", expand=True, ipady=8, ipadx=6)

        result_card = Card(page)
        result_frame = tk.Frame(result_card, bg=COLORS["card"])
        result_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # keep track of the currently displayed student so the delete
        # button knows what to remove
        state = {"current": None}

        def clear_result():
            for w in result_frame.winfo_children():
                w.destroy()

        def search():
            clear_result()
            state["current"] = None
            rollno = rollno_e.get().strip()
            found = None
            for s in self.data["student"]:
                if s["rollno"] == rollno:
                    found = s
                    break
            if not found:
                result_card.pack(padx=40, pady=10, fill="both", expand=True)
                tk.Label(result_frame, text="No student found with that roll no.",
                          font=FONT_SUB, bg=COLORS["card"], fg=COLORS["danger"]).pack(anchor="w")
                return
            state["current"] = found
            result_card.pack(padx=40, pady=10, fill="both", expand=True)

            header_row = tk.Frame(result_frame, bg=COLORS["card"])
            header_row.pack(fill="x")
            tk.Label(header_row, text=found["name"], font=("Segoe UI Semibold", 16),
                      bg=COLORS["card"], fg=COLORS["text"]).pack(side="left")
            DangerButton(header_row, "Delete Student", delete_student
                          ).pack(side="right")

            tk.Label(result_frame, text=f"Roll No: {found['rollno']}   |   Email: {found['email']}",
                      font=FONT_LABEL, bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w", pady=(2, 14))

            grades = found["grades"]
            if grades:
                cols = ("Subject", "Grade")
                tree = ttk.Treeview(result_frame, columns=cols, show="headings", height=min(6, len(grades)))
                for c in cols:
                    tree.heading(c, text=c)
                    tree.column(c, anchor="w")
                for subj, g in grades.items():
                    tree.insert("", "end", values=(subj, g))
                tree.pack(fill="x", pady=(0, 12))
                avg = round(sum(grades.values()) / len(grades), 2)
                tk.Label(result_frame, text=f"Average: {avg}", font=FONT_BTN,
                          bg=COLORS["card"], fg=COLORS["success"]).pack(anchor="w")
            else:
                tk.Label(result_frame, text="No grades recorded yet.", font=FONT_SUB,
                          bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")

        def delete_student():
            found = state["current"]
            if not found:
                return
            confirm = messagebox.askyesno(
                "Confirm delete",
                f"Are you sure you want to permanently delete '{found['name']}' "
                f"(Roll No: {found['rollno']})? This cannot be undone.",
            )
            if not confirm:
                return
            self.data["student"] = [
                s for s in self.data["student"] if s["rollno"] != found["rollno"]
            ]
            save_data(self.data)
            state["current"] = None
            clear_result()
            result_card.pack_forget()
            rollno_e.delete(0, "end")
            messagebox.showinfo("Deleted", f"Student '{found['name']}' has been deleted.")

        RoundedButton(search_row, "Search", search).pack(side="left", padx=(10, 0))
        rollno_e.bind("<Return>", lambda e: search())

    # ------------------------------------------------------------------
    # Teacher Lookup (with delete)
    # ------------------------------------------------------------------
    def _build_teacher_details(self, page):
        self._page_header(page, "Teacher Lookup", "Search a teacher by employee id.")
        card = Card(page)
        card.pack(padx=40, pady=10, fill="x")
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=30, pady=25, fill="x")

        search_row = tk.Frame(inner, bg=COLORS["card"])
        search_row.pack(fill="x")
        empid_e = tk.Entry(search_row, font=FONT_SUB, relief="flat", bg="#F7F8FC",
                            fg=COLORS["text"], highlightthickness=1,
                            highlightbackground=COLORS["border"],
                            highlightcolor=COLORS["accent"])
        empid_e.pack(side="left", fill="x", expand=True, ipady=8, ipadx=6)

        result_card = Card(page)
        result_frame = tk.Frame(result_card, bg=COLORS["card"])
        result_frame.pack(padx=20, pady=20, fill="both", expand=True)

        state = {"current": None}

        def clear_result():
            for w in result_frame.winfo_children():
                w.destroy()

        def search():
            clear_result()
            state["current"] = None
            empid = empid_e.get().strip()
            found = None
            for t in self.data["teacher"]:
                if t["empid"] == empid:
                    found = t
                    break
            if not found:
                result_card.pack(padx=40, pady=10, fill="both", expand=True)
                tk.Label(result_frame, text="No teacher found with that employee id.",
                          font=FONT_SUB, bg=COLORS["card"], fg=COLORS["danger"]).pack(anchor="w")
                return
            state["current"] = found
            result_card.pack(padx=40, pady=10, fill="both", expand=True)

            header_row = tk.Frame(result_frame, bg=COLORS["card"])
            header_row.pack(fill="x")
            tk.Label(header_row, text=found["name"], font=("Segoe UI Semibold", 16),
                      bg=COLORS["card"], fg=COLORS["text"]).pack(side="left")
            DangerButton(header_row, "Delete Teacher", delete_teacher
                          ).pack(side="right")

            tk.Label(result_frame,
                      text=f"Employee ID: {found['empid']}   |   Subject: {found['subject']}",
                      font=FONT_LABEL, bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w", pady=(2, 4))
            tk.Label(result_frame, text=f"Email: {found['email']}", font=FONT_LABEL,
                      bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")

        def delete_teacher():
            found = state["current"]
            if not found:
                return
            confirm = messagebox.askyesno(
                "Confirm delete",
                f"Are you sure you want to permanently delete '{found['name']}' "
                f"(Employee ID: {found['empid']})? This cannot be undone.",
            )
            if not confirm:
                return
            self.data["teacher"] = [
                t for t in self.data["teacher"] if t["empid"] != found["empid"]
            ]
            save_data(self.data)
            state["current"] = None
            clear_result()
            result_card.pack_forget()
            empid_e.delete(0, "end")
            messagebox.showinfo("Deleted", f"Teacher '{found['name']}' has been deleted.")

        RoundedButton(search_row, "Search", search).pack(side="left", padx=(10, 0))
        empid_e.bind("<Return>", lambda e: search())

    # ------------------------------------------------------------------
    # All Students / All Teachers (Treeview lists, with delete-selected)
    # ------------------------------------------------------------------
    def _build_all_students(self, page):
        self._page_header(page, "All Students", "Every student currently registered.")
        card = Card(page)
        card.pack(padx=40, pady=10, fill="both", expand=True)
        wrap = tk.Frame(card, bg=COLORS["card"])
        wrap.pack(fill="both", expand=True, padx=20, pady=20)

        toolbar = tk.Frame(wrap, bg=COLORS["card"])
        toolbar.pack(fill="x", pady=(0, 10))
        tk.Label(toolbar, text="Select a row, then delete it.", font=FONT_LABEL,
                  bg=COLORS["card"], fg=COLORS["muted"]).pack(side="left")
        DangerButton(toolbar, "Delete Selected", self._delete_selected_student
                      ).pack(side="right")

        cols = ("Name", "Roll No", "Email", "Average Grade")
        tree = ttk.Treeview(wrap, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="w")
        tree.pack(fill="both", expand=True)
        tree.bind("<Delete>", lambda e: self._delete_selected_student())
        self.student_tree = tree

    def _refresh_all_students(self):
        tree = self.student_tree
        tree.delete(*tree.get_children())
        for s in self.data["student"]:
            grades = s["grades"]
            avg = round(sum(grades.values()) / len(grades), 2) if grades else "—"
            # use rollno (a stable unique key) as the row's iid
            tree.insert("", "end", iid=s["rollno"],
                        values=(s["name"], s["rollno"], s["email"], avg))

    def _delete_selected_student(self):
        tree = self.student_tree
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Nothing selected", "Please select a student row to delete.")
            return
        rollnos = list(selected)
        names = [tree.item(iid, "values")[0] for iid in rollnos]
        if len(rollnos) == 1:
            msg = f"Are you sure you want to permanently delete '{names[0]}'? This cannot be undone."
        else:
            msg = (f"Are you sure you want to permanently delete {len(rollnos)} students "
                   f"({', '.join(names)})? This cannot be undone.")
        if not messagebox.askyesno("Confirm delete", msg):
            return
        self.data["student"] = [
            s for s in self.data["student"] if s["rollno"] not in rollnos
        ]
        save_data(self.data)
        self._refresh_all_students()
        messagebox.showinfo("Deleted", "Selected student(s) deleted.")

    def _build_all_teachers(self, page):
        self._page_header(page, "All Teachers", "Every teacher currently registered.")
        card = Card(page)
        card.pack(padx=40, pady=10, fill="both", expand=True)
        wrap = tk.Frame(card, bg=COLORS["card"])
        wrap.pack(fill="both", expand=True, padx=20, pady=20)

        toolbar = tk.Frame(wrap, bg=COLORS["card"])
        toolbar.pack(fill="x", pady=(0, 10))
        tk.Label(toolbar, text="Select a row, then delete it.", font=FONT_LABEL,
                  bg=COLORS["card"], fg=COLORS["muted"]).pack(side="left")
        DangerButton(toolbar, "Delete Selected", self._delete_selected_teacher
                      ).pack(side="right")

        cols = ("Name", "Employee ID", "Subject", "Email")
        tree = ttk.Treeview(wrap, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="w")
        tree.pack(fill="both", expand=True)
        tree.bind("<Delete>", lambda e: self._delete_selected_teacher())
        self.teacher_tree = tree

    def _refresh_all_teachers(self):
        tree = self.teacher_tree
        tree.delete(*tree.get_children())
        for t in self.data["teacher"]:
            # use empid (a stable unique key) as the row's iid
            tree.insert("", "end", iid=t["empid"],
                        values=(t["name"], t["empid"], t["subject"], t["email"]))

    def _delete_selected_teacher(self):
        tree = self.teacher_tree
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Nothing selected", "Please select a teacher row to delete.")
            return
        empids = list(selected)
        names = [tree.item(iid, "values")[0] for iid in empids]
        if len(empids) == 1:
            msg = f"Are you sure you want to permanently delete '{names[0]}'? This cannot be undone."
        else:
            msg = (f"Are you sure you want to permanently delete {len(empids)} teachers "
                   f"({', '.join(names)})? This cannot be undone.")
        if not messagebox.askyesno("Confirm delete", msg):
            return
        self.data["teacher"] = [
            t for t in self.data["teacher"] if t["empid"] not in empids
        ]
        save_data(self.data)
        self._refresh_all_teachers()
        messagebox.showinfo("Deleted", "Selected teacher(s) deleted.")


def apply_ttk_style():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "Treeview",
        background=COLORS["card"],
        fieldbackground=COLORS["card"],
        foreground=COLORS["text"],
        rowheight=30,
        font=FONT_LABEL,
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["bg"],
        foreground=COLORS["muted"],
        font=FONT_BTN,
        relief="flat",
    )
    style.map("Treeview", background=[("selected", COLORS["accent"])],
              foreground=[("selected", "white")])


if __name__ == "__main__":
    app = SchoolApp()
    apply_ttk_style()
    app.mainloop()