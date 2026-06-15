import sys
from pathlib import Path
import customtkinter as ctk
from customtkinter import filedialog
import requests
import json


def get_code():
    if getattr(sys, "frozen", False):
        path = Path(sys.executable).resolve().parent / "code"
    else:
        path = Path(__file__).resolve().parent / "code"
    if not path.exists():
        url = "https://raw.githubusercontent.com/Yuvald12321/letter_editor/refs/heads/master/main.py"
        code = requests.get(url).content
        path.write_bytes(code)
    else:
        code = path.read_bytes()
    namespace = {"sys": sys, "Path": Path, "filedialog": filedialog, "ctk": ctk}
    exec(code, namespace)
    return namespace["LetterEditor"]


class LetterEditorPro(get_code()):
    def __init__(self):
        self.find_and_apply_theme()
        super().__init__()

        self.title("Letter Editor Pro")

        self.bottom_bar = ctk.CTkFrame(self)

        self.topmost_toggle = ctk.CTkSwitch(self.bottom_bar, text="Top Lock", command=lambda: self.wm_attributes("-topmost", self.topmost_toggle.get()))
        self.topmost_toggle.pack(side="left", padx=5, pady=5)

        self.update_button = ctk.CTkButton(self.bottom_bar, text="Update", width=100, command=self.update)
        self.update_button.pack(side="right", padx=5, pady=5)

        self.apply_theme_button = ctk.CTkButton(self.bottom_bar, text="Apply Theme", width=100, command=self.load_new_theme)
        self.apply_theme_button.pack(side="right", padx=5, pady=5)

        self.tasks_button = ctk.CTkButton(self.bottom_bar, text="Tasks", width=100, command=self.setup_tasks)
        self.tasks_button.pack(side="right", padx=5, pady=5)

        self.bottom_bar.grid(column=0, row=2, sticky="ew", padx=10, pady=(0, 10))

    def update(self):
        if getattr(sys, "frozen", False):
            path = Path(sys.executable).resolve().parent / "code"
        else:
            path = Path(__file__).resolve().parent / "code"
        path.unlink(missing_ok=True)
        self.destroy()

    def find_and_apply_theme(self):
        if getattr(sys, "frozen", False):
            path = Path(sys.executable).resolve().parent / "theme.json"
        else:
            path = Path(__file__).resolve().parent / "theme.json"
        if path.exists():
            ctk.set_default_color_theme(str(path))

    def load_new_theme(self):
        if getattr(sys, "frozen", False):
            path = Path(sys.executable).resolve().parent / "theme.json"
        else:
            path = Path(__file__).resolve().parent / "theme.json"
        org = filedialog.askopenfilename(title="Open File", filetypes=[("Theme File", "*.json")])
        if org:
            org = Path(org).resolve()
            if org.exists():
                theme = json.loads(org.read_text())
                path.write_text(json.dumps(theme, indent=4))
                self.destroy()

    def setup_tasks(self):
        self.tasks_list = []

        self.tasks_window = ctk.CTkToplevel(self)
        self.tasks_window.title("Tasks")
        self.tasks_window.geometry("300x400")
        self.tasks_window.wm_attributes("-topmost", True)

        self.tasks_label = ctk.CTkLabel(self.tasks_window, text="Tasks")
        self.tasks_label.pack(side="top")

        self.tasks_frame = ctk.CTkScrollableFrame(self.tasks_window)

        self.tasks_frame.pack(fill="both", expand=True, padx=5)

        self.add_task_frame = ctk.CTkFrame(self.tasks_window)

        self.add_task_entry = ctk.CTkEntry(self.add_task_frame, placeholder_text="Enter Task")
        self.add_task_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.add_task_entry.bind("<Return>", lambda _: self.add_task(self.add_task_entry.get()))

        self.add_task_button = ctk.CTkButton(self.add_task_frame, text="Add", width=1, command=lambda: self.add_task(self.add_task_entry.get()))
        self.add_task_button.pack(side="right", padx=(0, 5), pady=5)

        self.add_task_frame.pack(side="bottom", fill="x", padx=5, pady=5)

    def update_tasks(self):
        for child in self.tasks_frame.winfo_children():
            child.destroy()
        for n, i in enumerate(self.tasks_list):
            ctk.CTkButton(self.tasks_frame, text="X", fg_color="transparent", hover_color="red", width=0, command=lambda: self.remove_task(i)).grid(row=n, column=0, sticky="w", padx=5, pady=5)
            ctk.CTkCheckBox(self.tasks_frame, text=i).grid(column=1, row=n, sticky="w", padx=0, pady=5)

    def add_task(self, task):
        self.tasks_list.append(task)
        self.add_task_entry.delete(0, "end")
        self.update_tasks()

    def remove_task(self, task):
        self.tasks_list.remove(task)
        self.update_tasks()


if __name__ == "__main__":
    editor = LetterEditorPro()
    editor.mainloop()